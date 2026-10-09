# 영어공부

성인 학습자를 위한 단계별 영어 학습 사이트 (초급, 중급, 고급, 회화). 기획은 [PLAN.md](PLAN.md)를 보세요.

## 준비 (처음 한 번)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## 자주 쓰는 명령

| 하는 일 | 명령 |
|---|---|
| 사이트 미리보기 (http://127.0.0.1:8000) | `.venv/bin/mkdocs serve` |
| 새 예문 음성 만들기 (있는 파일은 건너뜀) | `.venv/bin/python tools/make-audio.py` |
| 음성 전부 다시 만들기 | `.venv/bin/python tools/make-audio.py --force` |
| 사이트 빌드 (build/site) | `.venv/bin/mkdocs build` |
| 위키독스용 내보내기 (build/wikidocs) | `python3 tools/export-wikidocs.py --base-url https://<공개 사이트 주소>/` |

## 강의 쓰는 법

1. 장 폴더에 `NN-영문이름.md`를 만들고 PLAN.md 4절의 템플릿을 따릅니다.
2. 예문 옆에 `[🔊](audio/<강의파일명>-NN.mp3)`를 적습니다. 느린 버전은 `-slow.mp3`, 영국식은 `-uk.mp3`로 끝내고, 대화문은 `- **A:** 문장 [🔊](...)` 형태로 쓰면 A·B 목소리가 달라집니다.
3. 그림은 `images/`에 PNG(가로 800px 이하)로 두고 `![한국어 설명](images/파일.png)`로 넣습니다.
4. `make-audio.py`를 실행하면 음성이 생깁니다.
