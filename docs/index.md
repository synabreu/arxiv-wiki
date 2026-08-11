# arXiv AI Wiki

![새로 등록된 AI 논문에서 관심도가 높은 5편을 선별하는 과정](assets/arxiv-ai-top-five-hero.jpg)

매일 arXiv에 새로 등록된 AI 논문 가운데 관심도가 높은 5편을 선별해 한국어로 정리한다.

- [최신 요약](latest.html)
- [일별 아카이브](daily/index.html)

> 순위는 최근성, 인용 영향, 저자 영향력, AI 주제 적합성, 개발자 관심, 초록 기반 학술 신호에 더해 **NVIDIA, OpenAI, Alibaba/Qwen, DeepSeek, Moonshot AI/Kimi 등 주요 AI 연구조직·모델 계열과 오픈 웨이트·공개 체크포인트 신호를 우선 반영**한 자동 선별 결과이며 학술적 품질의 절대 평가가 아니다.

## 버전 및 최근 변경 사항

- **현재 버전: v0.3.0** · 2026-08-11
  - arXiv 메타데이터 요청을 공식 API 엔드포인트의 단일 통합 쿼리로 유지해 불필요한 호출을 줄였다.
  - 모든 arXiv 요청에 최소 3초 간격을 적용하고, HTTP 429·`Rate exceeded`·일시적인 서버 오류 발생 시 exponential backoff와 jitter를 사용해 최대 5회 재시도한다.
  - 서버가 제공하는 `Retry-After` 값을 우선 반영해 재시도 시점을 조정한다.
  - 논문 분석과 Figure 추출이 동일한 PDF를 공유하도록 캐시해 선정 논문당 중복 다운로드를 제거했다.
  - GitHub Actions의 일일 작업이 동시에 실행되지 않도록 concurrency 제어를 추가했다.
  - PyMuPDF의 deprecated `fitz` import를 권장 API인 `pymupdf`로 전환했다.

- **이전 버전: v0.2.0** · 2026-08-07
  - 논문 선별 로직을 **오픈 웨이트 중심**으로 강화했다.
  - NVIDIA/Nemotron, OpenAI/GPT-OSS, Alibaba/Qwen, DeepSeek, Moonshot AI/Kimi를 비롯해 Llama, Mistral, GLM 계열을 우선 신호로 반영한다.
  - `open-weight`, `open weights`, `model weights`, `checkpoint`, `Hugging Face`, 공개 라이선스 등 실제 가중치·체크포인트 공개 신호에 별도 가중치를 부여한다.
  - 기존 최근성, 인용 영향, 저자 영향력, AI 주제 적합성, 개발자 관심, 학술 신호는 유지하면서 오픈 웨이트·주요 연구조직 점수를 추가해 Top 5를 선정한다.
