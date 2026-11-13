"""Research: turn a topic or URL into a source pack (article text + Wikipedia background + links)."""
import json, re, urllib.parse
import feedparser, requests, trafilatura

UA = {"User-Agent": "ExplainerStudio/1.0 (local research script)"}


def _article(url):
    try:
        html = trafilatura.fetch_url(url)
        return trafilatura.extract(html, include_comments=False, include_tables=False) or ""
    except Exception:
        return ""


def _wiki(q, n=2):
    out = []
    try:
        s = requests.get("https://en.wikipedia.org/w/api.php", headers=UA, timeout=20, params={
            "action": "query", "list": "search", "srsearch": q, "srlimit": n, "format": "json"}).json()
        for hit in s["query"]["search"]:
            t = hit["title"]
            ex = requests.get("https://en.wikipedia.org/w/api.php", headers=UA, timeout=20, params={
                "action": "query", "prop": "extracts", "explaintext": 1, "titles": t, "format": "json"}).json()
            page = next(iter(ex["query"]["pages"].values()))
            out.append({"title": t, "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_")),
                        "text": page.get("extract", "")[:12000]})
    except Exception:
        pass
    return out


def research(topic, max_articles=5, search=None):
    sources = []
    if re.match(r"https?://", topic):
        sources.append({"title": topic, "url": topic, "text": _article(topic)[:15000]})
        query = sources[0]["text"][:200] or topic
    else:
        query = topic
        seen = set()
        # long headline-style topics return nothing from news search, so also try short keyword versions
        stop = set("a an the to of in on and or as its it is are for with into from by at what why how means mean new over after "
                   "ahead this that their his her them they be been will would can could than then up down out about".split())
        words = [w for w in re.findall(r"[A-Za-z0-9'-]+", topic) if w.lower() not in stop]
        queries = ([search] if search else []) + [topic, " ".join(words[:7]), " ".join(words[:4])]
        feeds = []
        for q in dict.fromkeys(queries):
            feeds += ["https://www.bing.com/news/search?" + urllib.parse.urlencode({"q": q, "format": "rss"}),
                      "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, "hl": "en-US", "gl": "US", "ceid": "US:en"})]
        # Bing News RSS links straight to publishers (Google News RSS links are opaque redirects)
        for feed_url in feeds:
            if len(sources) >= max_articles: break
            for e in feedparser.parse(feed_url).entries[:max_articles * 3]:
                if len(sources) >= max_articles:
                    break
                url = e.link
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
                if "url" in qs:
                    url = qs["url"][0]
                if url in seen or "news.google.com" in url:
                    continue
                seen.add(url)
                txt = _article(url)
                if len(txt) < 600:          # paywalls / consent pages / headline-only
                    continue
                sources.append({"title": e.title, "url": url, "published": e.get("published", ""), "text": txt[:8000]})
    n_news = len(sources)
    if n_news < 3:                  # background pages only when news is thin (keyword wiki hits are often off-topic)
        sources += _wiki(" ".join(words[:5]) if not re.match(r"https?://", topic) else query[:120])
    if n_news < 2:
        raise RuntimeError(f"research found only {n_news} news article(s) for {topic!r}; refusing to script from background pages alone")
    return {"topic": topic, "sources": [s for s in sources if s["text"].strip()]}


if __name__ == "__main__":
    import sys
    print(json.dumps(research(sys.argv[1]), indent=1)[:3000])
