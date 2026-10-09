#!/usr/bin/env python3
"""content/의 강의를 위키독스에 붙여넣기 좋은 형태로 내보낸다.

- 트랙(책)마다 build/wikidocs/<트랙>/ 폴더를 만들고, 목차 순서대로 번호를 붙인 페이지 파일을 쓴다.
- front matter를 지운다.
- 음성(audio/...)과 그림(images/...) 경로를 공개된 사이트 주소로 바꾼다 (--base-url).
  주소를 주지 않으면 그림·음성 파일을 media/ 에 모아 두므로 위키독스에 직접 올리면 된다.
- 목차.md에 위키독스에서 만들 페이지 순서와 깊이를 적는다.

사용법: python3 tools/export-wikidocs.py [--base-url https://.../]
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "build" / "wikidocs"
TRACKS = ["beginner", "intermediate", "advanced", "conversation"]

FRONT = re.compile(r"\A---\n(.*?)\n---\n+", re.S)
MEDIA = re.compile(r"\]\(((?:audio|images)/[^)\s]+)\)")


def split_front(text):
    m = FRONT.match(text)
    if not m:
        return {}, text
    meta = dict(
        line.split(":", 1) for line in m.group(1).splitlines() if ":" in line
    )
    return {k.strip(): v.strip() for k, v in meta.items()}, text[m.end():]


def pages(track_dir):
    """(파일, 깊이) 를 목차 순서대로 돌려준다. 책 소개 → 장 소개 → 강의."""
    yield track_dir / "index.md", 0
    for chapter in sorted(p for p in track_dir.iterdir() if p.is_dir()):
        if (chapter / "index.md").exists():
            yield chapter / "index.md", 1
        for lesson in sorted(chapter.glob("*.md")):
            if lesson.name != "index.md":
                yield lesson, 2


def export(base_url):
    if OUT.exists():
        shutil.rmtree(OUT)
    for track in TRACKS:
        track_dir = CONTENT / track
        if not (track_dir / "index.md").exists():
            continue
        out_dir = OUT / track
        out_dir.mkdir(parents=True)
        toc = []
        for n, (src, depth) in enumerate(pages(track_dir)):
            meta, body = split_front(src.read_text(encoding="utf-8"))
            title = meta.get("title") or src.stem
            rel_dir = src.parent.relative_to(CONTENT).as_posix()

            def fix(m):
                path = m.group(1)
                if base_url:
                    return f"]({base_url}{rel_dir}/{path})"
                dst = out_dir / "media" / Path(path).name
                dst.parent.mkdir(exist_ok=True)
                shutil.copy2(src.parent / path, dst)
                return m.group(0)

            body = MEDIA.sub(fix, body)
            name = f"{n:02d}-{src.parent.name if src.name == 'index.md' else src.stem}.md"
            (out_dir / name).write_text(body, encoding="utf-8")
            toc.append(f"{'  ' * depth}- {title}  ({name})")

        book = split_front((track_dir / "index.md").read_text(encoding="utf-8"))[0]
        (out_dir / "목차.md").write_text(
            f"# {book.get('title', track)} 위키독스 목차\n\n"
            "들여쓰기가 위키독스의 페이지 깊이입니다. 위에서부터 순서대로 페이지를 만들고 파일 내용을 붙여넣으세요.\n\n"
            + "\n".join(toc) + "\n",
            encoding="utf-8",
        )
        print(f"{track}: 페이지 {len(toc)}개 -> {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    base = args[args.index("--base-url") + 1] if "--base-url" in args else ""
    if base and not base.endswith("/"):
        base += "/"
    export(base)
