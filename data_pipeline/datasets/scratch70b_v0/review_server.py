"""Local review UI for scratch70b_v0. No GPU. Bind to 43147."""

from __future__ import annotations

import argparse
import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from data_pipeline.datasets.scratch70b_v0.catalog import DATASET_DIR, load_all

HOST = "127.0.0.1"
PORT = 43147
DECISIONS_PATH = DATASET_DIR / "review_decisions.json"
DECISIONS = ("unread", "keep", "drop", "edit")


def _load_decisions() -> dict[str, str]:
    if not DECISIONS_PATH.is_file():
        return {}
    data = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def _save_decision(doc_id: str, decision: str) -> None:
    if decision not in DECISIONS:
        raise ValueError(decision)
    current = _load_decisions()
    current[doc_id] = decision
    DECISIONS_PATH.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")


def _page(title: str, body: str) -> bytes:
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{html.escape(title)}</title>
  <style>
    :root {{ font-family: ui-sans-serif, system-ui, sans-serif; color: #0f172a; background: #f8fafc; }}
    body {{ margin: 0; }}
    header {{ background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; }}
    header a {{ color: #93c5fd; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 1.25rem; }}
    .grid {{ display: grid; gap: 0.6rem; }}
    .card {{ background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.85rem 1rem; }}
    .meta {{ color: #475569; font-size: 0.9rem; }}
    .keep {{ border-left: 4px solid #16a34a; }}
    .drop {{ border-left: 4px solid #dc2626; }}
    .edit {{ border-left: 4px solid #d97706; }}
    .unread {{ border-left: 4px solid #94a3b8; }}
    article {{ white-space: pre-wrap; line-height: 1.5; background: white; padding: 1rem; border-radius: 10px; border: 1px solid #e2e8f0; }}
    nav.actions a {{ display: inline-block; margin-right: 0.5rem; padding: 0.35rem 0.7rem; border-radius: 8px; background: #e2e8f0; color: #0f172a; text-decoration: none; }}
    .filters a {{ margin-right: 0.75rem; }}
  </style>
</head>
<body>
  <header>
    <div>scratch70b_v0 review — 70B from-scratch seed (5,120 ctx)</div>
    <div class="meta">Mark keep / drop / edit. Decisions save to review_decisions.json. No training starts from this page.</div>
  </header>
  <main>{body}</main>
</body>
</html>
"""
    return html_doc.encode("utf-8")


def _index(category: str | None, decision: str | None) -> bytes:
    docs = load_all()
    decisions = _load_decisions()
    rows = []
    keep = drop = edit = unread = 0
    for doc in docs:
        mark = decisions.get(doc.id, "unread")
        if mark == "keep":
            keep += 1
        elif mark == "drop":
            drop += 1
        elif mark == "edit":
            edit += 1
        else:
            unread += 1
        if category and doc.category != category:
            continue
        if decision and mark != decision:
            continue
        rows.append(
            f'<div class="card {html.escape(mark)}">'
            f'<a href="/doc/{html.escape(doc.id)}"><strong>{html.escape(doc.title)}</strong></a>'
            f'<div class="meta">{html.escape(doc.id)} · {html.escape(doc.category)} / '
            f'{html.escape(doc.subcategory)} · {html.escape(doc.difficulty)} · '
            f'{html.escape(doc.source_model)} · {len(doc.body.split())} words · {html.escape(mark)}</div>'
            f"</div>"
        )
    filters = ['<a href="/">all</a>']
    for cat in sorted({d.category for d in docs}):
        filters.append(f'<a href="/?category={html.escape(cat)}">{html.escape(cat)}</a>')
    filters.append('<a href="/?decision=unread">unread</a>')
    filters.append('<a href="/?decision=keep">keep</a>')
    filters.append('<a href="/?decision=drop">drop</a>')
    filters.append('<a href="/?decision=edit">edit</a>')
    body = (
        f"<p><strong>{len(docs)}</strong> docs · keep {keep} · drop {drop} · "
        f"edit {edit} · unread {unread}</p>"
        f'<p class="filters">{"".join(filters)}</p>'
        f'<div class="grid">{"".join(rows) if rows else "<p>No documents match.</p>"}</div>'
    )
    return _page("scratch70b_v0 review", body)


def _detail(doc_id: str) -> bytes:
    docs = {d.id: d for d in load_all()}
    if doc_id not in docs:
        return _page("not found", "<p>Unknown id.</p>")
    doc = docs[doc_id]
    mark = _load_decisions().get(doc.id, "unread")
    actions = " ".join(
        f'<a href="/decide/{html.escape(doc.id)}?d={d}">{d}</a>' for d in ("keep", "drop", "edit")
    )
    body = (
        f'<p><a href="/">← catalog</a></p>'
        f"<h1>{html.escape(doc.title)}</h1>"
        f'<p class="meta">{html.escape(doc.id)} · {html.escape(doc.category)} / '
        f"{html.escape(doc.subcategory)} · {html.escape(doc.difficulty)} · "
        f"{html.escape(doc.source_model)} · currently {html.escape(mark)}</p>"
        f'<nav class="actions">{actions}</nav>'
        f"<article>{html.escape(doc.body)}</article>"
    )
    return _page(doc.title, body)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path == "/" or parsed.path == "/index":
            payload = _index(
                (qs.get("category") or [None])[0],
                (qs.get("decision") or [None])[0],
            )
        elif parsed.path.startswith("/doc/"):
            payload = _detail(parsed.path.removeprefix("/doc/"))
        elif parsed.path.startswith("/decide/"):
            doc_id = parsed.path.removeprefix("/decide/")
            decision = (qs.get("d") or ["unread"])[0]
            _save_decision(doc_id, decision)
            self.send_response(302)
            self.send_header("Location", f"/doc/{doc_id}")
            self.end_headers()
            return
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def serve(host: str = HOST, port: int = PORT) -> None:
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"Review scratch70b_v0 at http://{host}:{port}/")
    httpd.serve_forever()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args(argv)
    serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
