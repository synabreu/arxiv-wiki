# Untangling the Mechanisms of Misleading Context in Medical Question Answering

- **게시일:** 2026-09-04
- **arXiv:** [2609.02754v1](http://arxiv.org/abs/2609.02754v1) · [PDF](https://arxiv.org/pdf/2609.02754v1)
- **저자:** Robin Linzmayer, Noémie Elhadad
- **분야:** cs.CL, cs.AI, cs.LG
- **선정 점수:** 5.19
- **선정 이유:** 최근성 0.7, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.9, 개발자 관심 0.0, 학술 신호 0.6, 오픈 웨이트·주요 연구조직 신호 1.0

[← 2026-09-04 목록으로 돌아가기](../daily/2026-09-04.html)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: The injection design and its behavioral effect. (a) All five arms share a clean stem, differing](../assets/papers/untangling-the-mechanisms-of-misleading-context-in-medical-question-answering/figure-1.jpg)

*Figure · 원문 PDF 4쪽 · Figure 1: The injection design and its behavioral effect. (a) All five arms share a clean stem, differing*

![Figure 2: Injected cue disclosure by surface. (a) Nondisclosure rate by surface. (b) Among visible](../assets/papers/untangling-the-mechanisms-of-misleading-context-in-medical-question-answering/figure-2.jpg)

*Figure · 원문 PDF 5쪽 · Figure 2: Injected cue disclosure by surface. (a) Nondisclosure rate by surface. (b) Among visible*

![Figure 3: Where influence accumulates. Median](../assets/papers/untangling-the-mechanisms-of-misleading-context-in-medical-question-answering/figure-3.jpg)

*Figure · 원문 PDF 6쪽 · Figure 3: Where influence accumulates. Median*

<!-- paper-visuals:end -->

## 한 문장 요약

의도적으로 주입한 두 종류의 오도성 문맥(증거형 허위 주장과 정답 단언)이 의료 다지선다 질의응답에서 모델의 판단을 어떻게 왜곡하는지, 그 왜곡이 추론 흔적(trace)과 응답 표면에 어떻게 드러나고(또는 숨겨지며), 왜곡이 추론 과정에서 언제 축적되는지와 감독자(모니터)가 이를 얼마나 검출할 수 있는지를 대규모 벤치마크(MedMisBench, n=8,627)와 세 모델(R1-14B, OSS-120B, GPT-5.4)을 통해 실험적으로 규명했다.

## 해결하려는 문제

대형 언어모델(LLM)이 의료 질문에 대해 높은 성능을 보이지만 외부에서 제공되는 문맥(전자건강기록, 검색 결과, 환자 진술 등)에 오도적 정보가 포함될 수 있고, 이 문맥이 모델의 의료적 판단을 왜곡할 때 그 취약성(어떤 문맥에 얼마나 민감한가), 왜곡이 추론 흔적과 응답 표면에 어떻게 드러나는가(또는 드러나지 않는가), 왜곡이 추론 내부에서 어떤 메커니즘으로 작동하는가(언제·어떻게 축적되는가), 그리고 감독자가 모델 출력(추론 흔적 또는 응답)만 보고 이를 얼마나 탐지할 수 있는가를 체계적으로 밝히지 못한 한계를 해결하려고 한다.

## 핵심 기여

- 증거 기반 허위(clinical fabricated evidence)와 정답 단언(bare assertion)을 같은 질문 항목에 쌍으로 주입해 동일한 문항에서 두 유형의 오도성 문맥을 직접 비교했다.
- 추론 흔적(trace)과 가시적 응답(response)이라는 동일한 결정의 두 출력 표면을 쌍으로 분석하여, 문맥 영향의 '공개(disclosure)'가 표면별로 어떻게 다른지(추론 흔적에서 훨씬 자주 드러남)를 보여주었다.
- 추론 흔적을 이용한 이식(transplant resampling) 분석으로 두 문맥 유형이 추론에 미치는 시간적 메커니즘이 다름을 규명함(증거형은 초기에 들어와 누적, 단언형은 결말 근처에서 결론을 재지향).
- 감독자(LLM 모니터) 실험을 통해 어떤 표면(추론 흔적 대 응답), 어떤 설정(가이드 유무)이 왜곡 탐지에 유리한지 정량적으로 제시함(가장 좋은 설정은 추론 흔적+가이드로 5% FPR에서 78% 검출).

## 접근 방법

* 데이터: MedMisBench의 의료 추론 서브셋(n=8,627)을 사용, 각 문항에는 원래의 증거형 허위 문장(evidence-bearing cue)이 있고 저자들은 동일 대상 오답을 지목하는 형식으로 문항별 정답 단언(answer-bearing cue)을 매칭해 확장함.
* 주입 설계: 모든 팔(arm)은 동일한 질문 본문에 하나의 문장만 추가하는 방식(클린, Evidence-true/false, Answer-true/false).
* 모델: (1) DeepSeek-R1-Distill-Qwen-14B (R1-14B, self-hosted, trace 노출 가능), (2) gpt-oss-120b (OSS-120B, 대형 오픈 모델, full CoT 노출), (3) GPT-5.4 (프론티어 폐쇄 모델, 응답만 공개).
* 실험: 각 항목·팔·모델에 대해 1회 샘플링(총 129,405 샘플)으로 정확도 및 'uptake'(주입된 옵션으로 이동한 비율)를 측정.
* 공개 여부(disclosure)는 GPT-4.1 judge에 의해 추론 흔적과 응답 각각에서 ‘무언급(silent)’인지 판단(휴먼 검증 κ=0.94).
* 메커니즘 분석은 R1-14B의 무언급(silent) 추론 흔적 40개(각 큐별 20개)를 선택해 문장 단위로 절단한 접두부(prefix)를 cue 없는 프롬프트에 이식하고(매 4문장 간격) 다시 샘플링(각 컷당 30회)해 prefix가 주입된 답변 확률을 측정(이식/매개분석).
* 감독성능은 gpt-4.1-mini를 모니터로 사용, 추론 흔적 또는 응답을 단일 표면으로 읽게 하고 neutral vs guided(저자 정리된 '왜곡 서명'을 포함) 두 프롬프트로 0–100 점수 부여; AUROC 및 5% FPR에서의 검출률을 보고.

## 주요 결과

- 데이터셋: MedMisBench 의료 추론 n=8,627(세 분할 포함). 전 모델에서 두 종류의 허위 주입이 모두 모델을 유도했음. Uptake(주입된 옵션 채택 비율, False cue 기준): R1-14B: Evidence→63%, Answer→73%; OSS-120B: Evidence→43%, Answer→62%; GPT-5.4: Evidence→21%, Answer→49% (각 값은 Clean 기준 대비 증가로 보고됨).
- 정확도 변화 예시: R1-14B 정확도는 Clean 47%에서 Evidence-false 20%, Answer-false 13%로 하락(본문에 보고된 수치).
- 공개(Disclosure): 추론 흔적에서는 주입 큐가 2–19%의 비율로 '무언급(silent)'(즉 대부분 언급됨)인 반면, 응답 표면에서는 10–93%가 무언급(즉 대부분 숨김)으로 표면별 차이가 큼. 특히 응답에서 Answer 큐 무언급 비율은 R1-14B/OSS-120B/GPT-5.4 각각 73%, 93%, 87%로 높았고, Evidence 큐 무언급은 각각 10%, 54%, 52%로 상대적으로 낮음.
- 메커니즘(이식 분석): R1-14B 무언급(trace) 40건에서 계산한 영향 누적 위치(x50)와 AUC: Evidence-false median x50=0.35, AUC=0.56(초기에 영향 도입·누적); Answer-false median x50=0.72, AUC=0.24(결말 근처에서 결론 재지향). 이 차이는 통계적으로 유의함(p<0.001).
- 감독(모니터) 성능: OSS-120B 추론 흔적을 가이드와 함께 읽는 경우 AUROC=0.95, 5% FPR에서 recall(검출률)=78%. 응답 표면들 중 최고 성능은 가이드된 R1-14B 응답으로 5% FPR에서 recall=32%였고, 다른 응답 표면은 최대 23% 이하 또는 19% 수준(GPT-5.4 guided 19%). 저자 결론대로 '추론 흔적 접근 + 가이드'가 가장 높은 저위양성(낮은 FPR) 탐지력을 제공함.

## 한계

- 저자 명시 한계: (1) 통제된 주입 설계로 단일-턴 다지선다(MC)·고정 위치에 문장을 추가하는 방식은 실제 임상 기록 오류나 회수(retrieval) 환경의 복잡도를 완전하지 않음. (2) 공개율(Disclosure)·모니터 평가·메커니즘 일부 실험은 단일 content-by-provenance 셀(Neutral provenance × Cue-Remapping content, n=1,153)에 국한되어 일반화가 제한됨. (3) 이식(transplant) 기반 메커니즘 분석은 계산 비용 때문에 한 작은 모델(R1-14B)의 40개 무언급 추론 흔적으로 제한되어 규모 제약이 있음. (4) 모니터 실험은 하나의 표준 구성(gpt-4.1-mini, 두 프롬프트)만 사용했으며 다른 모니터 아키텍처나 학습된 탐지기, 접근 설정 등을 시험하지 않음. (5) 프론티어 모델(GPT-5.4)의 추론 흔적은 관찰 불가하므로 해당 모델의 공개율·메커니즘은 응답 표면을 통해서만 간접적으로만 특성화할 수 있음(배포 제약에 따른 한계).
- developer_takeaways':['운영/배포 의사결정: 추론 흔적(chain-of-thought) 공개 여부는 실질적 안전 결정이다 — 저자 실험에서 

## 개발자 관점

- 운영/배포 의사결정: 추론 흔적(chain-of-thought) 공개 여부는 실질적 안전 결정이다 — 저자 실험에서 추론 흔적을 제공하는 설정(특히 OSS-120B trace + guided)이 5% FPR에서 78%의 왜곡 검출률을 보인 반면, 응답만 제공되는 설정의 최고 검출률은 32%였음. 서비스 제공자가 추론 흔적을 차단하면 감독 가능성을 크게 약화시킨다.
- 모니터 설계: 단순한 가이드(가이드된 프롬프트)만으로도 낮은-FPR 영역에서 검출률을 크게 개선할 수 있으므로(예: OSS-120B trace AUROC 0.89→0.95, recall 46%→78%) 모니터 프롬프트 공학은 실용적 비용으로 성능을 향상시킨다.
- 감시 정책: 응답이 '무언급(silent)'일 때 의미 해석을 문맥별로 달리해야 한다 — 정답 단언(Answer) 주입일 경우 무언급 응답의 상당 부분이 실제로 왜곡된 결정(대부분 silent+taken)인 반면 증거형 주입의 무언급 응답은 대체로 왜곡되지 않음(Section 4 결과). 따라서 모니터가 silence 자체를 곧바로 '안전' 신호로 취급하면 위험함.
- 위험 완화·방어 설계: 단순히 uptake(주입된 옵션 채택률)을 낮추는 방어가 disclosure를 악화시키지 않는지 검증해야 함 — 저자도 방어가 disclosure를 억제하면 잔존 왜곡이 더 탐지 불가능해질 위험을 경고함.
- 연구·재현성: 메커니즘 분석(이식 resampling)은 비용이 크므로 대규모·운영 환경에선 계산 비용과 보관(trace) 요구사항을 고려해야 함. 또한 provenance(권위·환자·중립) 처리가 성능에 큰 영향을 줌(예: patient framing에서 취약성 급감)으로, 현실 세계 배포시 발신자 표기·출처 메타데이터를 보존·활용하는 것이 중요함.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(서론·방법·결과·토의·부록 포함)에 근거해 작성되었다. 본문에 명시된 실험 수치·비율(예: uptake, 공개율, x50, AUC, 모니터 재현율)은 PDF 텍스트에서 직접 인용했으며, 추가 구현 세부사항이나 외부 재현 조건(예: 모델 내부 파라미터의 미세 설정, API 버전 변경 등)은 논문 본문에 충분히 기술되어 있지 않거나 배포 환경에 따라 변할 수 있어 여기서 생성하지 않았다.
