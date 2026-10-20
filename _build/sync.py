"""Finds public repos that have no page yet and writes _build/auto.json for build.py.

Hand-written entries in projects.json always win. A repo gets an automatic page when it is
public, not a fork, has a description, and is not listed in projects.json "ignore" or "more".
Runs daily from .github/workflows/sync.yml; locally: python _build/sync.py
"""
import json
import os
import re
import urllib.request
from pathlib import Path

USER = "SanTiwari07"
BUILD = Path(__file__).resolve().parent
API = "https://api.github.com"
MAX_IMAGE_BYTES = 2_500_000
BADGE_HOSTS = ("shields.io", "capsule-render", "badge", "komarev", "github-readme-stats", "skillicons", "vercel.app/api")

CATEGORY_WORDS = [
    ("security", ["security", "malware", "fraud", "fintech", "finance", "payment", "threat", "phishing", "crypto"]),
    ("agri", ["agri", "agro", "crop", "farm", "plant", "satellite", "climate", "village", "soil", "kisan", "krishi"]),
    ("vision", ["yolo", "opencv", "vision", "detection", "pose", "tracking", "image", "camera"]),
    ("hardware", ["arduino", "esp32", "iot", "sensor", "embedded", "raspberry", "pcb", "microcontroller"]),
    ("ai", ["llm", "agent", "gemini", "rag", "openai", "langchain", "ml", "machine-learning", "neural", "ai"]),
]
NICE = {"ai": "AI", "ml": "ML", "llm": "LLM", "iot": "IoT", "esp32": "ESP32", "yolov8": "YOLOv8", "yolo": "YOLO",
        "opencv": "OpenCV", "fastapi": "FastAPI", "react": "React", "typescript": "TypeScript", "javascript": "JavaScript",
        "python": "Python", "gemini": "Gemini", "aws": "AWS", "api": "API", "rag": "RAG", "nodejs": "Node.js",
        "tensorflow": "TensorFlow", "pytorch": "PyTorch", "arduino": "Arduino", "android": "Android", "kotlin": "Kotlin"}


def get(url, raw=False):
    req = urllib.request.Request(url, headers={"User-Agent": "santiwari07-site-sync"})
    if raw:
        req.add_header("Accept", "application/vnd.github.raw")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith(API):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data.decode("utf8", "ignore") if raw else json.loads(data)


def slugify(name):
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def pretty_name(name):
    return re.sub(r"(?<=[a-z])(?=[A-Z])|[-_]+", " ", name).strip()


def nice(word):
    return NICE.get(word.lower(), word.replace("-", " ").capitalize())


def first_sentence(text, limit=95):
    s = re.split(r"(?<=[.!?])\s", text.strip())[0].rstrip(".")
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


def clean_md(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"[*_`]{1,3}", "", t)
    return re.sub(r"\s+", " ", t).strip()


def readme_parts(text):
    """First two prose paragraphs and up to five feature bullets."""
    paras, bullets, in_code, in_features = [], [], False, False
    for block in re.split(r"\n\s*\n", text):
        if block.strip().startswith("```"):
            in_code = not in_code if block.count("```") % 2 else in_code
            continue
        if in_code:
            continue
        lines = [ln for ln in block.strip().splitlines() if ln.strip()]
        if not lines:
            continue
        head = lines[0].strip()
        if head.startswith("#"):
            in_features = bool(re.search(r"feature|highlight|what it does|key", head, re.I))
            lines = lines[1:]
            if not lines:
                continue
        items = [clean_md(re.sub(r"^\s*[-*+]\s+|^\s*\d+\.\s+", "", ln)) for ln in lines
                 if re.match(r"^\s*([-*+]|\d+\.)\s+", ln)]
        if items:
            if (in_features or not bullets) and len(bullets) < 5:
                bullets += [i for i in items if 12 < len(i) < 220][: 5 - len(bullets)]
            continue
        prose = clean_md(" ".join(lines))
        if (len(paras) < 2 and len(prose) > 60 and not prose.startswith(("|", ">", "-"))
                and "http" not in prose[:30] and "•" not in prose and prose.count("|") < 2
                and not prose.endswith(":")):
            paras.append(prose[:600])
    return paras, bullets


def readme_image(text, repo, branch):
    for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)|<img[^>]+src=[\"']([^\"']+)", text):
        src = m.group(1) or m.group(2)
        name = src.rsplit("/", 1)[-1].lower()
        if any(h in src for h in BADGE_HOSTS) or name.endswith(".svg") or re.search(r"logo|icon|favicon|badge", name):
            continue
        if not src.startswith("http"):
            src = f"https://raw.githubusercontent.com/{USER}/{repo}/{branch}/{src.lstrip('./')}"
        elif "github.com" in src and "/blob/" in src:
            src = src.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        try:
            req = urllib.request.Request(src, method="HEAD", headers={"User-Agent": "santiwari07-site-sync"})
            with urllib.request.urlopen(req, timeout=15) as r:
                size = int(r.headers.get("Content-Length") or 0)
                if r.headers.get_content_type().startswith("image/") and 0 < size <= MAX_IMAGE_BYTES:
                    return src
        except Exception:
            continue
    return None


def category(repo):
    hay = " ".join([repo["name"], repo.get("description") or "", " ".join(repo.get("topics") or [])]).lower()
    for cat, words in CATEGORY_WORDS:
        if any(re.search(rf"\b{re.escape(w)}", hay) for w in words):
            return cat
    return "tools"


def main():
    data = json.loads((BUILD / "projects.json").read_text(encoding="utf8"))
    covered = {p["links"].get("github", "").lower().rstrip("/") for p in data["projects"]}
    covered |= {m["url"].lower().rstrip("/") for m in data.get("more", [])}
    ignore = {n.lower() for n in data.get("ignore", [])}

    repos = get(f"{API}/users/{USER}/repos?per_page=100&type=owner&sort=pushed")
    meta, auto, used = {}, [], {p["slug"] for p in data["projects"]}
    for r in repos:
        url = r["html_url"].lower()
        meta[url] = {"pushed": r["pushed_at"][:10], "stars": r["stargazers_count"]}
        pages_url = f"https://{USER.lower()}.github.io/{r['name'].lower()}"
        if (r["fork"] or r["private"] or r["archived"] or not r.get("description") or url in covered
                or r["name"].lower() in ignore or any(c.lower().rstrip("/") == pages_url for c in covered)):
            continue
        try:
            text = get(f"{API}/repos/{USER}/{r['name']}/readme", raw=True)
        except Exception:
            text = ""
        paras, bullets = readme_parts(text)
        desc = r["description"].strip()
        slug = slugify(r["name"])
        while slug in used:
            slug += "-repo"
        used.add(slug)
        topics = r.get("topics") or []
        stack = ([r["language"]] if r.get("language") else []) + [nice(t) for t in topics if nice(t) != r.get("language")]
        links = {"github": r["html_url"]}
        if r.get("homepage") and "santiwari07.github.io/projects/" not in r["homepage"]:
            links["demo"] = r["homepage"]
        entry = {
            "slug": slug, "name": pretty_name(r["name"]), "tagline": first_sentence(desc),
            "category": category(r), "year": int(r["created_at"][:4]), "summary": desc,
            "body": [p for p in paras if p[:80] not in desc][:2], "highlights": bullets,
            "stack": stack[:8] or ["Code"], "links": links, "auto": True,
        }
        img = readme_image(text, r["name"], r["default_branch"]) if text else None
        if img:
            entry["image"], entry["image_alt"] = img, f"{entry['name']} screenshot"
        auto.append(entry)

    out = {"projects": auto, "meta": meta}
    (BUILD / "auto.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(f"{len(auto)} automatic project(s): {', '.join(p['slug'] for p in auto) or 'none'}")


if __name__ == "__main__":
    main()
