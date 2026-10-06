# Contributing to agentic-demo

`agentic-demo` 레포지토리에 기여해 주셔서 감사합니다! 이 레포는 코딩 에이전트(opencode)가 약 1분 안에 `memfit`을 완성하는 모습을 보여주기 위한 **라이브 데모 템플릿**입니다. 이 문서는 템플릿을 안전하고 일관되게 개선할 수 있도록 작성되었습니다. 기여를 시작하기 전에 아래 지침을 반드시 확인해 주세요.

---

## ⚠️ 가장 중요한 원칙: 템플릿은 의도적으로 미완성입니다

아래 두 파일은 데모 중에 에이전트가 완성합니다. **구현을 채운 채로 커밋하지 마세요.**

| 파일 | 시작 상태 |
|---|---|
| `src/memfit/capacity.py` | 함수 3개가 `NotImplementedError` 상태 (공식은 docstring에 있음) |
| `tests/test_capacity.py` | 시나리오 표(S1~S6)만 있고 테스트 함수는 없음 |

따라서 시작 상태에서 아래 결과는 버그가 아닙니다.

- `uv run --no-sync pytest` → `no tests ran`
- `uv run --no-sync memfit` → `NotImplementedError`

데모를 리허설한 뒤에는 `git restore src tests`로 시작 상태로 되돌립니다.

---

## 🛠 권장 환경

- **언어**: Python 3.10+ (표준 라이브러리만 사용, 런타임 의존성 없음)
- **패키지 관리**: [uv](https://github.com/astral-sh/uv)
- **품질 검증**: pre-commit (Ruff, ty, markdownlint), pytest
- **데모 에이전트**: [opencode](https://opencode.ai) (`AGENTS.md`를 읽음)

초기 셋업:

```bash
uv sync
uv run --no-sync pre-commit install
```

`pip install`, `source .venv/bin/activate`, `python` / `pytest` 직접 실행은 사용하지 않습니다. 항상 `uv run --no-sync <command>`로 실행합니다.

---

## 📁 디렉토리 구조와 역할

```text
agentic-demo/
├── AGENTS.md                 # 데모 중 opencode가 따르는 지침
├── src/memfit/
│   ├── capacity.py           # dataclass, 상수, 에이전트가 구현할 함수 3개
│   ├── catalog.py            # CLI가 사용하는 모델 / 디바이스 목록
│   └── cli.py                # argparse 진입점, 결과 표 출력
├── tests/
│   └── test_capacity.py      # 시나리오 표 + TINY 모델
├── .claude/rules/            # 템플릿 유지보수용 Claude Code 규칙
├── .pre-commit-config.yaml   # 커밋 시점 검증 (Ruff, ty, markdownlint 등)
└── README.md                 # 데모 진행 순서, 메모리 모델
```

### 함께 바뀌어야 하는 것들

데모 에이전트는 docstring의 공식과 시나리오 표만 보고 구현하므로, 아래 항목은 항상 서로 일치해야 합니다.

- `src/memfit/capacity.py`의 docstring `Formula:` 블록
- `tests/test_capacity.py`의 시나리오 표 (입력, 기대값)
- `AGENTS.md`의 단계와 명령
- `README.md`의 메모리 모델 표

함수 시그니처, 상수, dataclass 필드, 공식 중 하나라도 바꾸면 나머지도 같이 갱신합니다.

### 변경 유형별 가이드

- **데모 흐름 조정**: `AGENTS.md`를 수정합니다. 성능이 낮은 모델이 문자 그대로 따라 하므로 짧고, 단계별이고, 구체적으로 유지합니다.
- **모델 / 디바이스 변경**: `src/memfit/catalog.py`의 `MODELS`, `DEVICES`를 수정합니다. 모델 수치는 공개된 아키텍처 값을 사용하고, 디바이스는 예시용 메모리 크기임을 유지합니다.
- **메모리 모델 변경**: docstring 공식을 먼저 고치고, 시나리오 기대값을 다시 계산한 뒤 `README.md`를 갱신합니다.

### 변경 검증 방법

레포 안에서 함수를 구현하지 말고, 임시 복사본으로 확인합니다.

1. `src/`와 `tests/`를 레포 밖 임시 디렉토리에 복사합니다.
2. 복사본에서 함수 3개와 테스트 6개를 채웁니다.
3. `PYTHONPATH=<복사본>/src uv run --no-sync pytest <복사본>/tests`로 실행합니다.
4. `git status`로 `src/`, `tests/`에 의도하지 않은 변경이 없는지 확인합니다.

`AGENTS.md`나 docstring을 바꿨다면 실제 데모 에이전트로 여러 번 돌려 시간과 성공률을 확인해 주세요.

---

## 🌿 브랜치 네이밍 규칙

브랜치 이름은 PR 타입 태그를 **대문자 prefix**로 사용하고, 그 뒤 설명은 **소문자 kebab-case**로 작성합니다.

- **형식**: `<TAG>-<description>` (`<TAG>`는 아래 PR 제목 태그 목록에서 UPPER_CASE로, 설명은 소문자 kebab-case)
- **예시**:
  - `FEAT-add-memfit-template`
  - `FIX-kv-cache-formula`
  - `DOCS-update-demo-runbook`
  - `BOT-uv-lock-update`

---

## ✍️ 커밋 메시지 컨벤션

### 제목 형식

`[TAG] <요약 내용>` (영문 작성 권장, 50자 이내) — `TAG`는 아래 PR 제목 규칙에 명시된 태그 중 하나.

### 본문 규칙

- 제목과 본문 사이에 빈 줄을 추가합니다.
- "어떻게" 보다는 **"무엇을"**, **"왜"** 변경했는지 설명합니다.
- 명령형(Imperative) 어조를 사용합니다. (예: "Add capacity stubs" (O), "Added stubs" (X))

---

## 🚀 풀 리퀘스트 (PR) 절차

### 1. PR 제목 규칙

PR 제목은 `[TAG] <요약 내용>` 형식을 따릅니다.

#### 태그 종류

| 태그 | 의미 |
|---|---|
| `[FEAT]` | 새로운 기능 추가 |
| `[FIX]` | 버그 수정 |
| `[DOCS]` | 문서 변경 |
| `[STYLE]` | 코드 포맷팅, 세미콜론 누락 등 |
| `[REFACTOR]` | 동작 변화 없는 리팩토링 |
| `[PERF]` | 성능 개선 |
| `[TEST]` | 테스트 추가/수정 |
| `[BUILD]` | 빌드 시스템 또는 외부 종속성 변경 |
| `[CI]` | CI 설정 파일 및 스크립트 변경 |
| `[CHORE]` | 그 외 기타 변경 |
| `[REVERT]` | 이전 커밋 되돌리기 |
| `[HOTFIX]` | 긴급 수정 |
| `[BOT]` | 자동화 작업 (dependabot, uv-lock-update 등) |

- 본문은 **영문**, 1–150자, 영숫자와 `` _-.,&*[]:/`<>=#+ `` 만 허용.
- 태그와 본문 사이는 공백 한 칸.

#### 예시

- `[FEAT] Add memfit demo template`
- `[FIX] Correct KV cache formula in capacity docstring`
- `[DOCS] Update demo runbook`
- `[CHORE] Tune AGENTS.md for faster demo runs`
- `[BOT] Automated uv.lock update`

### 2. PR 타입 명시

PR 본문에 아래 중 하나 이상의 타입을 명시합니다.

- `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

### 3. PR 체크리스트

제출 전 다음 사항을 확인하세요.

- [ ] `src/memfit/capacity.py`와 `tests/test_capacity.py`가 미완성 시작 상태 그대로인가?
- [ ] docstring 공식, 시나리오 표, `AGENTS.md`, `README.md`가 서로 일치하는가?
- [ ] 시나리오 기대값을 임시 복사본 구현으로 검증했는가?
- [ ] `uv run --no-sync pre-commit run --all-files`가 통과하는가?
- [ ] `AGENTS.md`나 docstring을 바꿨다면 실제 데모 에이전트로 리허설했는가?
- [ ] 모든 public 함수에 type hint와 Google 스타일 docstring이 있는가?

---

## 🔍 코드 리뷰 기준

리뷰어는 다음 사항을 중점적으로 검토합니다.

- **데모 안정성**: 성능이 낮은 모델이 `AGENTS.md`와 docstring을 문자 그대로 따라 해도 약 1분 안에 끝나는가?
- **데모 무결성**: 템플릿에 정답 구현이 포함되거나 새어 나가지 않았는가?
- **일관성**: 공식, 시나리오 기대값, 문서가 서로 일치하는가?
- **단순함**: 표준 라이브러리만 사용하고, 데모에서 보여주지 않는 기능이나 파일을 추가하지 않았는가?
- **정확성**: 공식과 단위(bytes, GiB = 1024³), 모델 수치가 맞는가?

---

## 🤝 기여 방법 (Step-by-Step)

1. **Repository Clone**: `git clone git@github.com:junsoo999/agentic-demo.git`
2. **환경 설정**: `uv sync && uv run --no-sync pre-commit install`
3. **Branch Out**: 규칙에 맞는 이름으로 새 브랜치 생성
4. **변경 작성**: 위 "변경 유형별 가이드"에 따라 수정
5. **Local 검증**: `uv run --no-sync pre-commit run --all-files` 실행 후, 임시 복사본으로 시나리오 검증
6. **Submit PR**: 요약, 상세 설명, 검증 방법을 상세히 작성하여 제출

---

궁금한 점이 있다면 언제든 이슈를 통해 문의해 주세요!
