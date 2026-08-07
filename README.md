# arXiv AI Wiki

arXiv의 신규 AI 논문을 매일 수집하고 Top 5를 선별한 뒤, 일반 사용자와 개발자가 읽을 수 있는 한국어 Markdown 문서로 생성하는 프로젝트다.

## 제공 기능

- `cs.AI`, `cs.CL`, `cs.LG`, `cs.CV`, `cs.SE`, `cs.DC` 신규 논문 수집
- 최근성, 인용 영향, 저자 영향력, AI 적합성, 개발자 관심, 학술 신호 기반 Top 5 선별
- OpenAI Responses API의 구조화 출력으로 초록 기반 분석
- 한 문장 요약, 연구 문제, 핵심 기여, 접근 방법, 결과, 한계, 개발자 시사점 생성
- `docs/daily/YYYY-MM-DD.md` 및 `docs/latest.md` 생성
- GitHub Actions를 이용해 매일 오전 8시 10분(KST) 자동 실행

## 빠른 시작

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
export OPENAI_API_KEY="..."
arxiv-wiki --limit 5
```

OpenAI API 없이 수집과 순위, 초록만 확인하려면 다음을 실행한다.

```bash
arxiv-wiki --limit 5 --no-llm
```

## GitHub Actions 설정

저장소의 **Settings → Secrets and variables → Actions**에서 다음 값을 설정한다.

- Secret `OPENAI_API_KEY`: OpenAI API 키
- Secret `SEMANTIC_SCHOLAR_API_KEY`: 선택 사항. 인용·저자 지표의 안정적인 조회에 사용
- Variable `OPENAI_MODEL`: 선택 사항. 기본값은 `gpt-5-mini`

워크플로에는 `contents: write` 권한이 포함되어 있어 생성된 Markdown을 기본 브랜치에 자동 커밋한다. 조직 정책상 쓰기가 차단되면 **Settings → Actions → General → Workflow permissions**에서 Read and write permissions를 허용해야 한다.

## 생성 결과

```text
docs/
├── index.md
├── latest.md
└── daily/
    └── YYYY-MM-DD.md
```

GitHub Pages를 사용하려면 Pages의 배포 소스를 `main` 브랜치의 `/docs` 폴더로 지정한다.

## 선별 방식

현재 Top 5는 다음 신호를 각각 상한이 있는 점수로 환산해 결정한다.

- 등록 시점의 최근성
- Semantic Scholar의 논문 인용 수와 영향력 있는 인용 수
- 저자별 h-index와 누적 인용 수 중 최고값
- AI 카테고리와 LLM, agent, reasoning, multimodal 등 주제 적합성
- 코드 공개, 도구 사용, 효율, 지연 시간, 배포 등 개발자 관심 신호
- 벤치마크, 베이스라인, 어블레이션, 데이터셋, 증명, 재현성 등 초록 기반 학술 신호

Semantic Scholar 조회에 실패하거나 새 논문이 아직 색인되지 않았으면 외부 지표는 0점으로 두고 나머지 신호로 계속 선별한다. 이 점수는 학술적 품질의 절대 평가가 아니라 일일 큐레이션을 위한 비교 지표다.

## 정확성 원칙

분석은 기본적으로 arXiv 제목과 초록에 근거한다. 초록에서 확인할 수 없는 구현 세부사항이나 실험 수치는 생성하지 않으며, 불확실한 항목은 확인이 어렵다고 표시한다. PDF 전체 분석은 향후 확장 대상으로 분리한다.

## 테스트

```bash
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## 라이선스

프로젝트 코드는 MIT 라이선스를 따른다. 논문 PDF의 저작권과 라이선스는 각 arXiv 논문에 귀속되며, 이 프로젝트는 PDF를 재배포하지 않고 원문 링크만 제공한다.
