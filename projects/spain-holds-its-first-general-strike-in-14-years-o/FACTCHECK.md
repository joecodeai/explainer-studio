# Fact-check flags

- s05 | Spain needs 750,000 new homes just to close the gap. | Not supported by sources; specific housing deficit number is not cited. | cut
- s08 | Activists demanded rent caps, lease renewals, and a crackdown on speculation. | Rent caps are not mentioned as a demand; only automatic lease renewals and speculation crackdowns are cited. | cut
- s11 | A snap election was announced for late October, later set for November 29. | Sources state the election was called on Oct. 5 for Nov. 29; no initial late-October date is mentioned. | cut
- s14 | But the opposition calls it an electoral strike against the incoming government. | Not supported by sources; no mention of this specific framing from the opposition. | cut
- s16 | If the walkout turns violent, traditional conservative groups could gain ground. | Not supported by sources; no analysis links strike violence to conservative electoral gains. | cut
- s17 | Regional governments already controlled by opposition parties blocked rent caps. | Not supported; sources only mention national parliamentary blockage by right-wing parties and Junts. | cut
- s17 | They argued price limits would destroy market supply entirely. | Not supported; opponents cited a potential flight of rental properties, not total destruction of supply. | cut
- s21 | Polling shows voters leaning toward the right, fearing austerity. | Not supported by sources; no polling data or voter fears regarding austerity are cited. | cut
- s21 | But housing remains the dominant issue since 2025. | Not supported; sources indicate housing crisis built over years with major protests erupting in autumn 2026. | cut
- s24 | Radical groups could exploit peaceful marches to clash with police. | Not supported by sources; no mention of radical groups planning clashes at this specific strike. | cut
- s25 | Public opinion heavily supports government intervention to lower rents. | Not directly supported; sources cite protests and left-party sympathy, but do not quantify broad public polling on intervention. | cut

## Resolved by Claude 2026-11-12
All 11 flags fixed in script.json (backup: script.before_factfix.json). Lines the sources do support (Bank of Spain 750,000 homes, polling leaning right, PP's "electoral strike" quote, analyst's violence warning, radical groups at marches) were kept but attributed; the rest were rewritten to match the sources (Oct 5 election call, lease renewals not rent caps, parliament (PP, Vox, Junts) voted down the decrees over "flight of properties", unions want intervention).
- 2026-11-12: s18 Pedro Sánchez line was an invented direct quote → replaced with his reported argument (AP: right-wing parties "would bring austerity and underfunded social services").
