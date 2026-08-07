# arXiv AI Wiki

![새로 등록된 AI 논문에서 관심도가 높은 5편을 선별하는 과정](assets/arxiv-ai-top-five-hero.jpg)

매일 arXiv에 새로 등록된 AI 논문 가운데 관심도가 높은 5편을 선별해 한국어로 정리한다.

- [최신 요약](latest.html)
- [일별 아카이브](daily/index.html)

> 순위는 최근성, 인용 영향, 저자 영향력, AI 주제 적합성, 개발자 관심, 초록 기반 학술 신호에 더해 **NVIDIA, OpenAI, Alibaba/Qwen, DeepSeek, Moonshot AI/Kimi 등 주요 AI 연구조직·모델 계열과 오픈 웨이트·공개 체크포인트 신호를 우선 반영**한 자동 선별 결과이며 학술적 품질의 절대 평가가 아니다.

## 버전 및 최근 변경 사항

- **현재 버전: v0.2.0** · 2026-08-07
  - 논문 선별 로직을 **오픈 웨이트 중심**으로 강화했다. NVIDIA/Nemotron, OpenAI/GPT-OSS, Alibaba/Qwen, DeepSeek, Moonshot AI/Kimi를 비롯해 Llama, Mistral, GLM 계열을 우선 신호로 반영한다.
  - `open-weight`, `open weights`, `model weights`, `checkpoint`, `Hugging Face`, 공개 라이선스 등 실제 가중치·체크포인트 공개 신호에 별도 가중치를 부여한다.
  - 기존 최근성, 인용 영향, 저자 영향력, AI 주제 적합성, 개발자 관심, 학술 신호는 유지하면서 오픈 웨이트·주요 연구조직 점수를 추가해 Top 5를 선정한다.
  - 최신 arXiv AI 논문 후보 가운데 핵심 논문 5편을 자동 선별하도록 구성했다.
  - 논문 상세 분석을 초록 중심에서 **원문 PDF 본문 전체 기반 분석**으로 확장했다.
  - 상세 페이지에 연구 문제, 핵심 기여, 접근 방법, 주요 결과, 한계, 개발자 관점의 시사점을 한국어로 제공한다.
  - 접근 방법 섹션의 Markdown 표를 제거하고 본문 또는 `*` 불릿 형식으로 표시하도록 개선했다.
  - 논문 PDF에서 실제 **Figure**로 확인되는 그림만 추출해 상세 페이지에 표시하도록 개선했다.
  - 기존에 등록된 논문을 중복 선별하지 않도록 arXiv ID 기반 중복 제거 기능을 추가했다.
  - arXiv API의 Timeout, 429 Rate Limit, 일시적인 서버 오류에 대응하기 위해 요청 제한, 재시도와 backoff 처리를 강화했다.
  - GitHub Pages의 논문·일별 목록 링크를 `.html` 경로로 통일해 모바일 환경에서 발생하던 404 오류를 수정했다.
  - 일별 아카이브에서 논문 제목을 검색할 수 있는 검색 기능을 추가했다.
