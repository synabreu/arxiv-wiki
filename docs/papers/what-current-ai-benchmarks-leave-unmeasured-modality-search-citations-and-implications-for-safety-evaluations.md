# What Current AI Benchmarks Leave Unmeasured: Modality, Search, Citations, and Implications (for Safety Evaluations)

- **게시일:** 2026-08-07
- **arXiv:** [2608.06202v1](http://arxiv.org/abs/2608.06202v1) · [PDF](https://arxiv.org/pdf/2608.06202v1)
- **저자:** Ro Encarnación, Tina Behzad, Emma Lurie, Danaé Metaxa
- **분야:** cs.HC, cs.AI
- **선정 점수:** 10.52
- **선정 이유:** 최근성 1.4, 핵심어: large language model, 핵심어: llm, 핵심어: benchmark, 분야 가중치 2.0

[← 2026-08-07 목록으로 돌아가기](../daily/2026-08-07.md)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: Average per-run accuracy across modalities](../assets/papers/what-current-ai-benchmarks-leave-unmeasured-modality-search-citations-and-implications-for-safety-evaluations/figure-1.jpg)

*Figure · 원문 PDF 5쪽 · Figure 1: Average per-run accuracy across modalities*

![Figure 2: Within-modality and between-modality re-](../assets/papers/what-current-ai-benchmarks-leave-unmeasured-modality-search-citations-and-implications-for-safety-evaluations/figure-2.jpg)

*Figure · 원문 PDF 6쪽 · Figure 2: Within-modality and between-modality re-*

![Figure 3: Example benchmark prompt and responses. In this example from our data, the same SafetyBench prompt (A)](../assets/papers/what-current-ai-benchmarks-leave-unmeasured-modality-search-citations-and-implications-for-safety-evaluations/figure-3.jpg)

*Figure · 원문 PDF 7쪽 · Figure 3: Example benchmark prompt and responses. In this example from our data, the same SafetyBench prompt (A)*

<!-- paper-visuals:end -->

## 한 문장 요약

모달리티(채팅 UI vs API)와 웹 검색 유무를 2×2 조건으로 둔 대규모 감사(audit)를 통해 단일-런·단일-모달리티·정확도 중심 평가가 놓치는 응답 일관성, 문장 유사성, 인용 근거, 기권(abstention) 등 안전 관련 거동 변이를 정량적으로 측정했다 (401문항·4,812응답, 각 조건 3회 반복).

## 해결하려는 문제

기존 LLM 벤치마크 관행은 (1) 단일 접근 모달리티(API)로 평가해 실제 소비자용 채팅 인터페이스에서의 동작 차이를 무시하고, (2) 각 프롬프트에 대해 단일 실행만 수행해 반복 실행에 따른 불안정성을 측정하지 않으며, (3) 정확도 같은 단일 집계 지표만 보고하여 응답의 근거(citation), 재현성(consistency), 기권 동작 등 안전에 중요한 출력 특성을 놓친다는 가정들에서 출발한다. 이 논문은 이러한 가정들이 실제로 평가 결과를 얼마나 가릴 수 있는지를 검증한다.

## 핵심 기여

- 모달리티(채팅 UI vs API)와 웹 검색(검색-활성/비활성)을 교차한 2×2 감사 설계를 제시·실행하여 동일 모델 계열 내에서 모달리티·검색이 성능과 출력 거동에 미치는 영향을 실증적으로 보였다.
- 정확도 외에 응답 일관성(consistency), 응답 텍스트 유사성(lexical/semantic similarity), 인용(grounding) 행태, 기권(abstention) 등 출력 수준의 추가 지표를 체계적으로 측정·보고했다.
- API 기반 단일-런 평가가 놓치는 행동 변이를 드러내고, 모달리티·검색을 고려한 평가 방법론(modality- and search-aware evaluation)을 제안했다.

## 접근 방법

대상 모델은 GPT-5.3 Instant(gpt-5.3-chat-latest)을 채팅 UI(로그아웃 상태의 ChatGPT 웹 인터페이스)와 API에서 동일 버전으로 접근하였다. 요인은 모달리티(채팅 UI vs API)와 웹 검색(활성 vs 비활성)의 2×2 교차설계이며, 각 프롬프트 당 네 조건 모두에서 3회 반복 실행하여 응답 일관성을 측정했다. 데이터셋은 BBQ(198문항, 11개 카테고리에서 범주별 층화표본 18문항)와 SafetyBench(203문항, 7개 카테고리에서 범주별 층화표본 29문항)로 총 401문항을 표본화하였다(총 응답 4,812 = 401×4조건×3회). 프롬프트는 제로샷 포맷을 사용했고(시스템 프롬프트 동기화 없음), API 쿼리는 기본 설정(temperature=1.0)으로 수집했다. 채팅 UI 수집은 자동화된 브라우저 세션, 회전 프록시, 세션 격리로 수행했다. 평가지표로는 (1) 정확도(기권 제외), (2) 응답 일관성(동일 조건 내 3회가 모두 같은 답 선택 비율), (3) 텍스트 유사성(렉시컬 Jaccard, 의미적 코사인 유사도(text-embedding-3-small)), (4) 인용률 및 인용 출처 중복(도메인/URL 수준), (5) 기권률을 사용했다. 통계적으로는 GLMM/LME를 사용해 프롬프트 수준 무작위절편을 포함한 검정을 수행하고 Benjamini–Hochberg 보정(주요 검정에 적용)을 사용했다.

## 주요 결과

- 샘플·집계: 401문항( BBQ 198, SafetyBench 203), 응답 4,812개(각 조건 3회 반복).
- 정확도(표 1): BBQ API: no-search 81.9% → search 77.8% (−4.1pp); BBQ chat UI: no-search 79.1% → search 75.9% (−3.2pp). SafetyBench API: no-search 88.5% → search 80.6% (−7.9pp); SafetyBench chat UI: no-search 85.9% → search 84.4% (−1.5pp). 전반적으로 검색 활성화는 정확도를 감소시켰고(예: SafetyBench/API에서 최대 −7.9 pp), 검색에 따라 모달리티 간 우위가 역전되기도 함(SafetyBench에서 검색 시 chat UI가 더 정확).
- 응답 일관성: 반복 실행 내에서 동일 답을 선택하지 않는 불일치가 조건에 따라 달라졌고, 검색은 일반적으로 불일치를 증가시켰다. 예: BBQ에서 chat UI/search 불일치 21.2% (CI [15.5,26.9]); API/search 19.2% 등. SafetyBench에서는 no-search에서 chat UI 불일치 12.3% vs API 6.4%였으나, search에서는 API 불일치 증가(12.8%)로 방향이 바뀜.
- 모달리티 간 분쟁성: 동일 프롬프트에 대해 API와 채팅 UI 응답 간 불일치(정답 선택 차이)는 항상 동일-모달리티(런-투-런) 불일치보다 높았고, 배수는 대략 1.14–1.30배 범위였다. 쌍별 불일치에 대한 GLMM에서 between-modality 쌍의 불일치 오즈비는 OR=1.51 (CI[1.19,1.92], p=0.002).
- 텍스트 유사성(표 3·5·4·6): Jaccard(렉시컬)에서는 between-modality가 현저히 낮음(예: BBQ no-search between 0.151 vs within-API 0.593, within-chat 0.404). 의미적 코사인 유사도(embeddings)에서도 between-modality 평균 0.626 (CI [0.617,0.635])에 비해 within-API 0.802, within-chat 0.863로 모달리티가 의미 수준에서도 큰 차이를 만듦(코사인 기반 LME의 cross-modality 효과 Cohen’s d ≈ −1.47, p<0.001). 채팅 UI는 단어 선택은 더 다양하되(낮은 Jaccard), 의미적으로는 반복간 더 일관되는 경향을 보임(높은 within-chat 코사인). 또한 API 응답은 종종 선택지 표기만 반환하는 경우가 있었음(BBQ API/no-search에서 7.1%가 설명 텍스트 없이 선택지만 제공; SafetyBench API/no-search에서 39.1%가 선택지만 제공), 반면 채팅 UI는 거의 항상 설명을 덧붙였음(99.6%).」「인용·근거화: 검색 활성화 조건에서만 인용이 발생했고, 두 모달리티가 동일 프롬프트에 대해 인용한 페이지(URL) 겹침은 매우 낮음(공유 URL 비율 ≈ 4%, 도메인 수준 공유 ≈ 7%). BBQ에서는 chat UI가 더 많은 고유 URL(총 n=356)·도메인 출처를 사용했고 API는 적음(n=179). SafetyBench에서는 chat UI n=540, API n=473로 비교적 근접하나 여전히 겹침은 낮음. 많은 프롬프트(예: BBQ의 37%)에서 두 모달리티의 URL 겹침이 전혀 없었음.」「기권(abstention): SafetyBench에서는 전혀 발생하지 않았고, BBQ의 no-search에서만 드물게 발생(6건, 4개 프롬프트). 기권은 일관되지 않아 동일 프롬프트에서도 반복 중 일부 실행에서만 관측되는 경우가 많았음(예: 3회 중 1회만 기권).

## 한계

- 저자 명시 한계: (1) 단일 모델 계열 및 단일 버전(GPT-5.3 Instant)만 검사했으며 결과가 다른 모델/버전·제공사에 일반화될지 불확실하다고 저자 스스로 언급함. (2) 두 벤치마크(BBQ, SafetyBench)와 단일 수집 기간(1주 이내 스냅샷)에 기반한 분석으로, 장기적 시간 변화(서비스 업데이트 등)는 반영되지 않음. (3) 인용의 품질·신뢰성·적합성 평가는 수행하지 않았고, 의미적 유사도는 단일 임베딩 모델(OpenAI text-embedding-3-small)에 의존한다는 점을 저자도 지적함.
- 추가 확인 가능한 제약(본문에서 합리적으로 확인되는 한계): (4) 채팅 UI는 로그아웃 상태의 소비자 인터페이스만 조사했고 계정·개인화·컨텍스트 보존 효과는 배제됨. (5) 반복 횟수는 3회로 제한되어 불안정성 추정의 분산이 여전히 클 수 있음. (6) 일부 평가(예: SafetyBench의 파싱 불가 응답 처리)는 무작위 대체(랜덤 선택)를 사용하여 점수화해 결과에 영향을 줄 가능성이 있음(32/2436 runs, 1.3%). (7) 브라우저 수집 구현 세부(자동화 프레임워크·프록시 구성·지연 스케줄링 등)는 설명되어 있으나 플랫폼 차단·네트워크 요인 등 외부 제약이 결과에 미칠 영향은 통제 어려움.

## 개발자 관점

- 벤치마크 설계 시 API만이 아니라 실제 배포되는 채팅 UI도 함께 측정해야 함(모달리티별 시스템 프롬프트·중재·검색 파이프라인 차이가 출력에 실질적 영향).
- 단일-런 정확도 보고는 불충분: 동일 프롬프트에 대해 다회 실행(권장 ≥3회 이상)으로 응답 일관성, 모달리티 간 불일치률, 기권 빈도 등을 추가로 보고하라.
- 검색(외부 도구) 활성화 여부를 명시·통제하고, 검색이 정확도를 악화시킬 수 있음을 염두에 두어야 함 — 검색 호출 정책(calibration)과 검색결과 선택·정렬 방식이 중요함.
- 채팅 UI 수집은 자동화·세션 격리·회전 프록시·속도 조절 등 추가 공학 비용이 들고 플랫폼 제한을 마주하므로 재현성 확보를 위해 관련 인프라(테스트베드, 검증된 수집 파이프라인)를 마련해야 함.
- 인용·근거화 평가가 중요: 인용 URL/도메인 수준의 비교뿐 아니라 출처 신뢰성·관련성 평가, 검색 결과 질(검색이 답변을 왜곡하는 경우 존재)을 함께 측정하라. 또한 개발·배포시 기권 행동(그레이존 거부/허용 일관성)을 강력히 테스트해야 함.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문 전 내용을 기반으로 작성되었으며(본문 텍스트, 표, 부록 포함), 본문에 명시된 수치(문항수 401, 응답수 4,812, 정확도·유사도·인용 겹침 수치 등)를 그대로 인용했다. 브라우저 자동화·프록시 구성 등의 구현 세부사항은 본문에 요약되어 있으나 내부 코드·환경(예: 정확한 자동화 도구명, 프록시 공급자)의 세부 구현은 PDF에서 직접 확인되지 않아 재현시 추가 구현 세부가 필요할 수 있다.
