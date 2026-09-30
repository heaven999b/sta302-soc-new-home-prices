"""Verify DOIs via the Crossref REST API (https://api.crossref.org/works/<DOI>) and save metadata."""
import sys, json, time, urllib.request, urllib.parse, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}
for doi in sys.argv[1:]:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()")
    req = urllib.request.Request(url, headers={"User-Agent": "STA302-citation-check (student project)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            m = json.load(r)["message"]
        rec = {"status": "found", "title": (m.get("title") or [""])[0], "journal": (m.get("container-title") or [""])[0],
               "year": (m.get("issued", {}).get("date-parts") or [[None]])[0][0], "volume": m.get("volume"), "issue": m.get("issue"),
               "page": m.get("page"), "authors": [f"{a.get('family','')}, {a.get('given','')}" for a in m.get("author", [])],
               "type": m.get("type")}
    except Exception as e:
        rec = {"status": f"error: {e}"}
    out[doi] = rec
    print(doi, "|", rec.get("status"), "|", rec.get("year"), "|", rec.get("title"), "|", rec.get("journal"), rec.get("volume"), rec.get("issue"), rec.get("page"), "|", "; ".join(rec.get("authors", [])[:5]))
    time.sleep(0.5)
path = f"{BASE}/results/crossref_verification.json"
old = json.load(open(path)) if os.path.exists(path) else {}
old.update(out)
json.dump(old, open(path, "w"), indent=2, ensure_ascii=False)
