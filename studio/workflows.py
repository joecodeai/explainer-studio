"""Convert ComfyUI editor workflows (incl. nested subgraphs) into API-format prompts, then patch inputs by node class/name."""
import copy, json, os

SKIP = {"MarkdownNote", "Note", "PreviewAny", "Reroute", "ImageCompare", "PreviewImage"}
LINK_TYPES = {"MODEL", "CLIP", "VAE", "CONDITIONING", "LATENT", "IMAGE", "MASK", "AUDIO", "VIDEO", "SIGMAS", "NOISE",
              "SAMPLER", "GUIDER", "LATENT_UPSCALE_MODEL", "UPSCALE_MODEL", "CLIP_VISION", "CONTROL_NET", "*"}


def widget_names(info, cls):
    """Ordered widget input names for a node class (+ True if followed by a control_after_generate value)."""
    spec = info[cls]["input"]
    out = []
    for sect in ("required", "optional"):
        for name, v in spec.get(sect, {}).items():
            t = v[0]
            opts = v[1] if len(v) > 1 and isinstance(v[1], dict) else {}
            is_widget = isinstance(t, list) or t in ("INT", "FLOAT", "STRING", "BOOLEAN", "COMBO") or opts.get("forceInput") is False
            if (isinstance(t, str) and t in LINK_TYPES) or opts.get("forceInput"):
                is_widget = False
            if is_widget:
                out.append((name, bool(opts.get("control_after_generate")) or (t == "INT" and name in ("seed", "noise_seed"))))
    return out


def ui_to_api(ui, info):
    defs = {sg["id"]: sg for sg in ui.get("definitions", {}).get("subgraphs", [])}
    api = {}

    def flatten(nodes, links, prefix, ext_inputs):
        """ext_inputs: subgraph-input index -> (source ref | ('value', v)). Returns map (node_id, slot) -> api ref for this scope."""
        L = {}
        for l in links:
            if isinstance(l, dict):
                L[l["id"]] = (l["origin_id"], l["origin_slot"], l["target_id"], l["target_slot"])
            else:
                L[l[0]] = (l[1], l[2], l[3], l[4])
        out_ref = {}       # (node_id, slot) -> api ref for outputs produced in this scope
        sub_out = {}       # instance node id -> list of refs per output slot
        prim = {}          # legacy PrimitiveNode values
        order = []
        for n in nodes:
            if n["type"] in SKIP or n.get("mode") == 2:
                continue
            if n["type"] == "PrimitiveNode":
                prim[n["id"]] = (n.get("widgets_values") or [None])[0]; continue
            order.append(n)

        def src(link_id):
            o_id, o_slot, _, _ = L[link_id]
            if o_id == -10:
                return ext_inputs.get(o_slot)
            if o_id in prim:
                return ("value", prim[o_id])
            return ("ref", o_id, o_slot)

        # first: expand subgraph instances (recursively)
        pending = {}
        for n in order:
            if n["type"] in defs:
                sg = defs[n["type"]]
                iv = list(n.get("widgets_values") or [])
                wi = [i for i in n.get("inputs", []) if "widget" in i]
                vals = {i["name"]: (iv[k] if k < len(iv) else None) for k, i in enumerate(wi)}
                ext = {}
                for idx, sin in enumerate(sg["inputs"]):
                    inst = next((i for i in n.get("inputs", []) if i["name"] == sin["name"]), None)
                    if inst and inst.get("link") is not None:
                        ext[idx] = ("lazy", inst["link"])
                pending[n["id"]] = (sg, ext)
        refs = {}

        def resolve(r):
            if r is None: return None
            if r[0] == "lazy": return resolve(src(r[1]))
            if r[0] == "value": return r
            if r[0] == "ref":
                o_id, slot = r[1], r[2]
                if o_id in sub_out: return sub_out[o_id][slot]
                return ("api", f"{prefix}{o_id}", slot)
            return r

        for nid, (sg, ext) in pending.items():
            ext_res = {k: resolve(v) if v[0] != "lazy" else resolve(src(v[1])) for k, v in ext.items()}
            inner_map = flatten(sg["nodes"], sg["links"], f"{prefix}{nid}:", ext_res)
            # subgraph outputs
            outs = []
            for so in sg["outputs"]:
                lid = so["linkIds"][0] if so.get("linkIds") else None
                if lid is None: outs.append(None); continue
                l = next(l for l in sg["links"] if (l["id"] if isinstance(l, dict) else l[0]) == lid)
                o_id, o_slot = (l["origin_id"], l["origin_slot"]) if isinstance(l, dict) else (l[1], l[2])
                outs.append(inner_map.get((o_id, o_slot), ("api", f"{prefix}{nid}:{o_id}", o_slot)))
            sub_out[nid] = outs

        for n in order:
            if n["type"] in defs:
                continue
            cls = n["type"]
            if cls not in info:
                raise KeyError(f"Unknown node type {cls} (install custom node?)")
            inputs = {}
            wv = list(n.get("widgets_values") or []) if isinstance(n.get("widgets_values"), list) else []
            k = 0
            for name, ctl in widget_names(info, cls):
                if k < len(wv):
                    inputs[name] = wv[k]; k += 1
                    if ctl: k += 1
            for i in n.get("inputs", []):
                if i.get("link") is None:
                    continue
                r = resolve(src(i["link"]))
                if r is None: continue
                inputs[i["name"]] = r[1] if r[0] == "value" else [r[1], r[2]]
            if n.get("mode") == 4:   # bypassed: route outputs to first input of same type
                for oi, o in enumerate(n.get("outputs", [])):
                    for i in n.get("inputs", []):
                        if i.get("type") == o.get("type") and i.get("link") is not None:
                            sub_out.setdefault(n["id"], [None] * len(n["outputs"]))[oi] = resolve(src(i["link"]))
                continue
            api[f"{prefix}{n['id']}"] = {"class_type": cls, "inputs": inputs, "_meta": {"title": n.get("title", cls)}}
            for oi in range(len(n.get("outputs", []))):
                refs[(n["id"], oi)] = ("api", f"{prefix}{n['id']}", oi)
        refs.update({(k2, i): v for k2, lst in sub_out.items() for i, v in enumerate(lst) if v})
        return refs

    flatten(ui["nodes"], ui["links"], "", {})
    # drop api refs to nodes that were skipped
    for nid, node in api.items():
        for k, v in list(node["inputs"].items()):
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str) and v[0] not in api:
                del node["inputs"][k]
    return api


def find(api, cls, title=None):
    return [k for k, v in api.items() if v["class_type"] == cls and (title is None or v["_meta"]["title"] == title)]


def set_input(api, cls, name, value, which=None):
    ids = find(api, cls)
    if which is not None: ids = [ids[which]]
    if not ids: raise KeyError(f"{cls} not in workflow")
    for i in ids: api[i]["inputs"][name] = value
    return ids


def load(name):
    p = os.path.join(os.path.dirname(__file__), "workflows", name + ".json")
    return copy.deepcopy(json.load(open(p)))


def prune(api, outputs=("SaveImageAdvanced", "SaveImage", "SaveVideo", "SaveAudioAdvanced", "SaveAudio")):
    """Keep only nodes that the output nodes depend on."""
    keep, stack = set(), [k for k, v in api.items() if v["class_type"] in outputs]
    while stack:
        k = stack.pop()
        if k in keep or k not in api: continue
        keep.add(k)
        for v in api[k]["inputs"].values():
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str): stack.append(v[0])
    out = {k: v for k, v in api.items() if k in keep}
    for v in out.values():   # dynamic-combo widgets the editor format doesn't store
        if v["class_type"] == "SaveImageAdvanced":
            v["inputs"].update({"format": "png", "format.bit_depth": "8-bit", "format.input_color_space": "sRGB"})
    return out
