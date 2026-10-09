#!/usr/bin/env python3
"""강의 Markdown의 [🔊](audio/....mp3) 링크를 찾아 예문 음성을 TTS로 만든다.

읽을 문장 찾는 규칙
- 표 안의 링크: 머리글이 '영어' 또는 '예문'인 칸의 문장 (없으면 첫 칸)
- 목록/대화문 안의 링크: 같은 줄에서 링크 앞에 있는 문장 ('**A:**' 같은 화자 표시는 빼고 읽음)

목소리 규칙
- 기본, 화자 A: 미국 여성 / 화자 B: 미국 남성
- 파일명이 '-uk.mp3'로 끝나면 영국 여성
- 파일명이 '-slow.mp3'로 끝나면 느린 속도

사용법: python3 tools/make-audio.py [content 폴더 또는 .md 파일 ...] [--force]
"""
import asyncio
import re
import sys
from pathlib import Path

import edge_tts

VOICE_A = "en-US-JennyNeural"
VOICE_B = "en-US-GuyNeural"
VOICE_UK = "en-GB-SoniaNeural"
SLOW_RATE = "-15%"

LINK = re.compile(r"\[(?:🔊|🐢)\]\((audio/[^)\s]+\.mp3)\)")
SPEAKER = re.compile(r"^\s*[-*]?\s*\*\*([AB])\s*:\*\*\s*")


def plain(text):
    text = re.sub(r"\*\*|__|`", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.strip()


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def jobs_for(md_path):
    """(출력 경로, 문장, 목소리, 속도) 목록을 돌려준다."""
    jobs = []
    header = None
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("|"):
            row = cells(line)
            if header is None:
                header = row
                continue
            if all(set(c) <= set("-: ") for c in row):
                continue
        else:
            header = None
        links = LINK.findall(line)
        if not links:
            continue

        voice = VOICE_A
        if header is not None:
            col = next((i for i, h in enumerate(header) if h in ("영어", "예문")), 0)
            text = plain(row[col])
        else:
            m = SPEAKER.match(line)
            if m and m.group(1) == "B":
                voice = VOICE_B
            text = plain(LINK.sub("", line[m.end():] if m else line).lstrip("-* "))

        for rel in links:
            v, rate = voice, "+0%"
            if rel.endswith("-uk.mp3"):
                v = VOICE_UK
            if rel.endswith("-slow.mp3"):
                rate = SLOW_RATE
            jobs.append((md_path.parent / rel, text, v, rate))
    return jobs


async def main(args):
    force = "--force" in args
    targets = [Path(a) for a in args if a != "--force"] or [Path("content")]
    files = []
    for t in targets:
        files += sorted(t.rglob("*.md")) if t.is_dir() else [t]

    made = skipped = 0
    for md in files:
        for out, text, voice, rate in jobs_for(md):
            if out.exists() and not force:
                skipped += 1
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            await edge_tts.Communicate(text, voice, rate=rate).save(str(out))
            print(f"{out}  <-  {text}  [{voice} {rate}]")
            made += 1
    print(f"만듦 {made}개, 건너뜀 {skipped}개")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
