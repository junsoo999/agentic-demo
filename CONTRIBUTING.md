# Contributing to agentic-demo

`agentic-demo`는 코딩 에이전트(opencode)가 약 1분 안에 `memfit`을 완성하는 모습을 보여주기 위한 **라이브 데모 템플릿**입니다. 기여를 시작하기 전에 아래 지침을 확인해 주세요.

---

## ⚠️ 가장 중요한 원칙: 템플릿은 의도적으로 미완성입니다

아래 두 파일은 데모 중에 에이전트가 완성합니다. **구현을 채운 채로 커밋하지 마세요.**

| 파일 | 시작 상태 |
|---|---|
| `src/memfit/capacity.py` | 함수 4개가 `NotImplementedError` 상태 (공식은 `AGENTS.md`에 있음) |
| `tests/test_capacity.py` | 시나리오 표(S1~S7)와 예시 테스트 S1만 있고 S2~S7은 없음 |

따라서 시작 상태에서 `uv run --no-sync pytest` → `1 failed`, `uv run --no-sync memfit` → `NotImplementedError`는 버그가 아닙니다. 리허설 후에는 `git restore src tests`로 되돌립니다.

데모 에이전트는 `AGENTS.md`와 위 두 파일만 읽습니다. 성능이 낮은 모델이 1분 안에 끝내야 하므로 **이 세 파일은 최대한 짧고 문자 그대로 따라 할 수 있게** 유지합니다.

---

## 🛠 환경

- Python 3.10+, 표준 라이브러리만 사용 (런타임 의존성 없음). 개발 의존성은 pytest 하나입니다. 린터는 없습니다.
- 패키지 관리는 [uv](https://github.com/astral-sh/uv). 항상 `uv run --no-sync <command>`로 실행하고, `pip`, 직접 `python` / `pytest` 실행은 하지 않습니다.
- 초기 셋업: `uv sync`

---

## 📁 디렉토리 구조

```text
agentic-demo/
├── AGENTS.md                 # 데모 중 opencode가 따르는 지침
├── src/memfit/
│   ├── capacity.py           # dataclass, 상수, 에이전트가 구현할 함수 4개
│   ├── catalog.py            # CLI가 사용하는 모델 / 디바이스 목록
│   └── cli.py                # argparse 진입점, 결과 표 출력
├── tests/test_capacity.py    # 시나리오 표 + TINY 모델 + 예시 테스트 S1
├── .claude/rules/            # 템플릿 유지보수용 Claude Code 규칙
└── README.md                 # 데모 진행 순서, 메모리 모델
```

### 함께 바뀌어야 하는 것들

`AGENTS.md`의 공식 표, `tests/test_capacity.py`의 시나리오 표, `README.md`의 메모리 모델 표는 항상 서로 일치해야 합니다. 하나를 바꾸면 나머지도 같이 갱신합니다. `capacity.py`의 docstring에는 동작 설명만 두고 공식이나 정답 코드를 넣지 않습니다.

### 변경 검증 방법

레포 안에서 함수를 구현하지 말고, 임시 복사본으로 확인합니다.

1. `src/`와 `tests/`를 레포 밖 임시 디렉토리에 복사합니다.
2. 복사본에서 함수 본문 4개와 테스트 S2~S7을 채웁니다.
3. `PYTHONPATH=<복사본>/src uv run --no-sync pytest <복사본>/tests` → `7 passed`
4. `git status`로 `src/`, `tests/`에 의도하지 않은 변경이 없는지 확인합니다.

`AGENTS.md`를 바꿨다면 실제 데모 에이전트로 여러 번 돌려 시간과 성공률을 확인해 주세요.

---

## 🌿 브랜치 / 커밋 / PR 규칙

- **브랜치**: `<TAG>-<description>` (TAG는 아래 표의 대문자, 설명은 소문자 kebab-case). 예: `FEAT-add-memfit-template`
- **커밋 제목**: `[TAG] <요약>` (영문, 50자 이내, 명령형). 본문은 "무엇을", "왜"를 설명합니다.
- **PR 제목**: `[TAG] <요약>` (영문, 1~150자, 태그와 본문 사이 공백 한 칸)

| 태그 | 의미 |
|---|---|
| `FEAT` | 새로운 기능 추가 |
| `FIX` | 버그 수정 |
| `DOCS` | 문서 변경 |
| `STYLE` | 코드 포맷팅 등 |
| `REFACTOR` | 동작 변화 없는 리팩토링 |
| `PERF` | 성능 개선 |
| `TEST` | 테스트 추가/수정 |
| `BUILD` | 빌드 시스템 또는 외부 종속성 변경 |
| `CI` | CI 설정 변경 |
| `CHORE` | 그 외 기타 변경 |
| `REVERT` | 이전 커밋 되돌리기 |
| `HOTFIX` | 긴급 수정 |
| `BOT` | 자동화 작업 |

**PR 본문**에는 타입, 요약, 관련 이슈(`Closes SOFT-XXXX`, 있을 때만), 상세 설명, 검증 방법, 리뷰어 참고 사항을 적습니다.

### PR 체크리스트

- [ ] `src/memfit/capacity.py`와 `tests/test_capacity.py`가 미완성 시작 상태 그대로인가?
- [ ] `AGENTS.md`의 공식 표, 시나리오 표, `README.md`가 서로 일치하는가?
- [ ] 시나리오 기대값을 임시 복사본 구현으로 검증했는가?
- [ ] `AGENTS.md`를 바꿨다면 실제 데모 에이전트로 리허설했는가?

---

## 🔍 코드 리뷰 기준

- **데모 안정성**: 성능이 낮은 모델이 `AGENTS.md`를 문자 그대로 따라 해도 약 1분 안에 끝나는가?
- **데모 무결성**: 템플릿에 정답 구현이 포함되거나 새어 나가지 않았는가?
- **일관성**: 공식, 시나리오 기대값, 문서가 서로 일치하는가?
- **단순함**: 표준 라이브러리만 사용하고, 데모에서 보여주지 않는 기능이나 파일을 추가하지 않았는가?
