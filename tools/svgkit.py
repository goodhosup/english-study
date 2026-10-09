"""강의 그림(SVG)을 같은 스타일로 그리기 위한 작은 도우미.

쓰는 법:
    from svgkit import *
    save("images/x.svg", "제목", [box(...), arrow(...)], height=420, track="beginner")
그 다음 `ffmpeg -i x.svg x.png` 로 PNG를 만든다.
"""

FONT = 'font-family="NanumBarunGothic, NanumGothic, sans-serif"'

# 트랙별 대표 색 (PLAN.md 6.2): 진한 글자색, 대표색, 배경색
TRACK = {
    "beginner": ("#1F5F3A", "#2E9E5B", "#F4FBF6"),
    "intermediate": ("#1C4189", "#2F6FDB", "#F3F7FE"),
    "advanced": ("#4B2A86", "#7B4FC9", "#F7F3FD"),
    "conversation": ("#7A4A22", "#E8833A", "#FFF6EE"),
}
GREEN, BLUE, ORANGE, PURPLE, RED, GRAY = "#2E9E5B", "#3D7BD9", "#E8833A", "#7B4FC9", "#E05252", "#5B6B7A"


def save(path, title, body, height=420, track="beginner", width=800):
    dark, _, bg = TRACK[track]
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" {FONT}>\n'
        '<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" '
        'markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#555"/></marker></defs>\n'
        f'<rect width="{width}" height="{height}" fill="{bg}"/>\n'
        f'<text x="{width / 2}" y="48" text-anchor="middle" font-size="30" font-weight="bold" fill="{dark}">{title}</text>\n'
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(body) + "\n</svg>\n")


def text(x, y, s, size=20, fill="#333", anchor="middle", bold=False):
    b = ' font-weight="bold"' if bold else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}"{b}>{s}</text>'


def box(x, y, w, h, fill, label="", color="#FFF", size=22, stroke=None, bold=True, rx=12):
    """둥근 사각형. label에 '|'를 넣으면 여러 줄."""
    st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>']
    lines = label.split("|") if label else []
    for i, line in enumerate(lines):
        dy = (i - (len(lines) - 1) / 2) * (size + 6)
        out.append(text(x + w / 2, y + h / 2 + size * 0.36 + dy, line, size, color, bold=bold))
    return "".join(out)


def arrow(x1, y1, x2, y2, color="#555", width=3):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{width}" marker-end="url(#a)"/>')
