# Can Large Language Models Explain Flight Safety Events? A Prior-Guided Semantic LLM-based Approach

- **게시일:** 2026-08-19
- **arXiv:** [2608.18017v1](http://arxiv.org/abs/2608.18017v1) · [PDF](https://arxiv.org/pdf/2608.18017v1)
- **저자:** Lu Xu, Xu Li, Linjiang Zheng, Fan Li, Riquan Zhang, Jiaxing Shang
- **분야:** cs.AI
- **선정 점수:** 6.01
- **선정 이유:** 최근성 0.8, 인용 영향 0.0 (인용 0회), 저자 영향 1.3 (최고 h-index 6), AI 주제 적합성 3.0, 개발자 관심 0.2, 학술 신호 0.7, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-08-19 목록으로 돌아가기](../daily/2026-08-19.html)

## 한 문장 요약

QAR 시계열을 통계·물리 특성으로 압축하고 양적 값을 의미 단위로 이산화한 뒤 CatBoost의 예측을 프롬프트로 주입해 LLM에게 대비적 few-shot 맥락과 구조화된 지식프롬프트로 하드랜딩 분류와 원인 설명을 수행하는 FlightLLM을 제안한다.

## 해결하려는 문제

목표는 QAR(Quick Access Recorder) 다변량 시계열에서 단순 탐지 수준을 넘어 조종사의 조종행동 수준에서 비행 안전사건(본 논문에서는 하드랜딩)의 원인을 일관되게 설명하는 것이다. 기존 기계학습·딥러닝 기반 방법들은 높은 분류 성능을 보이나 내부 가중치·어텐션 시각화는 도메인 전문가의 해석을 필요로 하며 인간이 이해 가능한 인과 서사를 직접 생성하지 못한다. LLM을 활용할 수 있으나 다음의 핵심 문제들이 존재한다: (1) QAR의 수치적·다중주파수 시계열과 LLM의 언어 토크나이저 사이의 모달 불일치(숫자 처리 및 연속성 손실), (2) LLM의 본질적 분류능력 한계, (3) 희귀 사건으로 인한 태스크 특화 데이터 부족(미세조정 곤란), (4) 일반 목적 LLM의 항공 도메인 지식 부족과 환각 위험.

## 핵심 기여

- 항공 QAR 기반 하드랜딩 분석을 위해 LLM을 활용한 FlightLLM 프레임워크 제시(모달 불일치·분류 한계·데이터 부족·도메인 지식 부족을 통합적으로 해결).
- TSFresh로 추출한 통계적 기술자(Fstat)와 도메인 설계 물리 지표(Fphy)를 결합한 하이브리드 피쳐 엔지니어링 및 이를 양적→질적 레이블(5-분위 기반)로 변환하는 Semantic Discretization 모듈 제안.
- CatBoost를 통계적 ‘전문가’로 도입해 예측 레이블과 확률을 프롬프트에 prior로 주입하는 Statistical Expert Hinting 메커니즘 도입으로 LLM의 불안정한 분류 보완.
- 유사도 기반 동적 문맥 검색(Dynamic Context Retrieval)으로 가장 유사한 정상·하드샘플을 대조적 few-shot 예제로 프롬프트에 포함해 LLM의 in-context contrastive reasoning 유도.
- 구조화된 프롬프트(특성 사전, CatBoost 보조 리포트, 대조적 few-shot, CoT 유도, 엄격한 출력 스키마)를 설계해 항공 지식을 주입하고 설명 가능한 원인 진단 및 반사실(counterfactual) 권고를 생성함. (실험은 A320 QAR 704 샘플에서 수행)

## 접근 방법

* 구성 아키텍처: 다섯 모듈로 구성됨 — (i) Data Preprocessing & Feature Engineering, (ii) Semantic Discretization, (iii) Statistical Expert Hinting, (iv) Dynamic Context Retrieval, (v) Prompt Construction & LLM Invocation.
* 주요 절차(본문 기준):
* 데이터 전처리: 각 비행에서 접지 시점(t) 기준으로 touchdown 직전 30초(window) 구간을 사용.
* 원본은 32개 파라미터(다른 샘플링 주파수)를 모두 4Hz로 리샘플링해 통일.
* 피쳐 엔지니어링: TSFresh로 자동 통계량(Fstat)을 추출한 후 센서별로 그룹화·유의성 테스트를 거쳐 top-k 선택.
* 도메인 기반 물리 지표(Fphy)는 수동으로 설계(예: 50→TD 최소 수직속도, 20→TD 시간 등).
* 두 벡터를 연결해 V = Fstat ⊕ Fphy를 생성.
* Semantic Discretization: 각 피쳐의 전역 분포에서 5th,25th,75th,95th 백분위(τ=[τ1,τ2,τ3,τ4])를 정의하고 연속값 f를 {Extremely Low, Slightly Low, Normal, Slightly High, Extremely High}의 5단계 토큰으로 매핑(Φ 함수).
* 출력은 (물리적 의미, 의미 라벨, 원숫자값)으로 구성된 서술형 디스크립터.
* Statistical Expert Hinting: CatBoost(gradient boosting decision tree)를 통계적 전문 모델로 학습하여 예측 레이블과 확률을 생성.
* 이 결과를 프롬프트에 보조 리포트로 포함시켜 LLM의 추론을 안내(동의/불일치 시 재검토 유도).
* Dynamic Context Retrieval: 훈련/참조 DB D에서 코사인 유사도로 쿼리 샘플과 가장 유사한 정상 샘플 및 가장 유사한 하드샘플을 각각 검색(xnorm, xhard)해 contrastive few-shot 예제로 프롬프트에 삽입.
* Prompt 및 LLM 호출: 시스템 페르소나(항공 전문가), 피쳐 사전(도메인 매핑), CatBoost 보조 리포트, 대조적 예시, 테스트 샘플(의미 이산화된 토큰), 엄격한 출력 JSON 스키마(분류, reasoning_steps, explanation, counterfactual)를 포함.
* Chain-of-Thought 유도와 '근거에만 기반' 제약을 통해 LLM(실험에선 GPT-3.5, DeepSeek-V1, GLM-4.7-flash)을 호출해 분류와 텍스트 기반 원인 진단을 생성.
* 학습·추론 특징: LLM 자체는 미세조정하지 않고 in-context learning(contrastive few-shot)으로 동작.
* CatBoost는 별도 학습기로 학습되어 확률·중요도 정보를 제공.
* Semantic Discretization은 LLM의 숫자 취급 약점을 완화하여 언어적 추론 활성화.

## 주요 결과

- 데이터셋: A320 실비행 QAR 37,929편 중 규정 기준(수직가속도 VRTG[altitude≤0] ≥ θ, θ=1.5g)을 따라 282개의 하드랜딩 샘플을 식별하고, 실험을 위해 무작위로 선택한 422개의 정상 샘플과 합쳐 총 704 샘플(282 hard, 422 normal)을 사용함. 각 샘플은 32개 파라미터를 포함하고 관찰 윈도우는 touchdown 전 30초이며 모든 파라미터를 4Hz로 통일.
- 정량 성능(표 IV): 비교 모델들과의 주요 지표(Accuracy, Precision, Recall, F1)에서 다음을 보고함:
- FlightLLM-GPT: Accuracy 81.56%, Precision 82.61%, Recall 67.86%, F1 74.51.
- FlightLLM-Deepseek: Accuracy 81.56%, Precision 85.71% (최고 Precision), Recall 64.29%, F1 73.47.
- FlightLLM-GLM: Accuracy 78.01%, Precision 71.19%, Recall 75.00%, F1 73.04.
기준 모델 성능(선택): CNN Accuracy 77.30%, Precision 67.14%, Recall 83.93%, F1 74.60; SDTAN Accuracy 80.14%, Precision 73.33%, Recall 78.57%, F1 75.86.
- 해석 가능성(사례 분석): FlightLLM은 개별 하드랜딩 사례에서 늦은 플레어(Δt20→TD=2.25s), 급격한 피치 조작(max ṖITCH = 2.8 deg/s), 매우 큰 피치 명령 변화(max ṖITCH_cmd = 41.84), 수직속도 변동성(VarΔIVV0.4–1.0 = 832.02) 등 주요 물리 증거를 식별하고, 이를 근거로 'Hard Landing'을 예측하며 원인 설명과 조치(예: 플레어 조기 개시, 부드러운 피치 유지)형의 반사실 권고를 생성함. 이 텍스트 설명은 원시 QAR 곡선과 정량분포(정상군 대비 백분위)를 기반으로 일관되게 정렬됨.
- 소거 실험(ablations, 표 V): 핵심 모듈 제거 시 성능 저하 관찰 —
- w/o Semanticization: Accuracy 76.60%, Precision 67.16%, Recall 80.36%, F1 73.17 (Precision 크게 감소).
- w/o Expert Hint: Accuracy 75.18%, Precision 75.61%, Recall 55.36%, F1 63.92 (F1 최저).
- w/o Context Retrieval (Zero-Shot): Accuracy 73.76%, Precision 63.01%, Recall 82.14%, F1 71.32.
이를 통해 Semantic Discretization, Expert Hinting, Dynamic Retrieval 각 모듈의 분류 안정성·정확성 기여를 입증함.

## 한계

- 저자가 명시한 한계: (1) LLM들을 항공 특화 데이터로 미세조정하지 않았음(모든 실험은 공개 사전학습 모델 사용). 저자는 항공 특화 파인튜닝이 추후 성능·일관성 향상에 기여할 수 있음을 명시함. (2) 본 연구의 방법을 다른 비행 안전 사건으로 확장하려면 각 사건 특성에 맞는 프롬프트 수정을 요구하므로 프롬프트별 수작업 비용이 존재함.
- 본문에서 합리적으로 확인되는 제약(실험 범위에서 드러나는 제약): (3) 데이터 샘플링 편향 가능성 — 원시 데이터에서 282 hard를 유지하되 정상은 37,647개 중 422개만 무작위 추출하여 총 704 샘플로 실험을 수행했음(대표성·일반화에 영향 가능). (4) LLM 자체의 환각 위험을 완화하기 위한 프롬프트 제약을 사용했으나 여전히 LLM 출력은 프롬프트와 prior에 민감하며 설명의 정확성은 프롬프트 설계에 크게 의존함. (5) CatBoost 및 TSFresh 관련 세부 하이퍼파라미터(예: CatBoost 트리 수, learning rate, TSFresh에서의 top-k 값)는 본문에 구체 수치로 제시되어 있지 않아 재현 시 추가 조정 필요. (6) Semantic Discretization의 분위수 경계로 인한 경계 사례 처리(경계 바로 아래/위의 샘플이 다른 범주로 나뉘어 검출·재현성에 영향)와, 이로 인한 Precision/Recall trade-off(논문에서 의도적으로 정밀도에 무게)를 저자가 인정함.

## 개발자 관점

- 재현(데이터): 원문 실험은 A320 QAR 원시 로그(32개 파라미터)를 필요로 하며 관찰 윈도우는 touchdown 직전 30초. 대규모 정상군(論문은 37,929편)을 통계 기준(분위수 산출)에 사용하면 의미 토큰의 글로벌 τ 계산에 유리함.
- 재현(전처리·특징): 모든 채널을 4Hz로 리샘플링하고 TSFresh로 통계 특성(Fstat)을 추출한 뒤 센서별 그룹화·유의성 테스트로 top-k를 선별. 또한 Table I의 Fphy 항목(예: Δt50→TD, IVV50→TD_min, PITCHTD 등)을 수동 구현해야 LLM 프롬프트의 물리적 해석이 가능함.
- 카테부스트 및 LLM 연동: CatBoost를 별도 모델로 학습해 예측 레이블·확률·중요도(Feature importance)를 프롬프트에 포함시키는 것이 핵심. 다만 CatBoost의 구체적 하이퍼파라미터는 논문에 기재되어 있지 않으므로 교차검증으로 튜닝 필요.
- 프롬프트 및 체인오브소트(운영): 구조화된 프롬프트(시스템 페르소나, 특성사전, CatBoost 보조리포트, 대조적 few-shot 예제, 엄격한 출력 JSON 스키마)를 사전에 템플릿화하면 운영 시 일관성 개선. 하지만 이벤트별(하드랜딩 외) 프롬프트 수정 비용을 고려해야 함.
- 비용·스케일링: 실험은 704샘플에 대해 in-context LLM 호출을 수행함. 대규모 생산 적용 시에는 LLM 호출 비용(토큰·API 비용)과 응답 지연, 프라이버시(온프레미스 또는 프라이빗 LLM 필요성)를 고려해야 함. CatBoost 같은 경량 모델을 엣지에 두고 LLM은 요약·설명용으로만 호출하는 하이브리드 배포가 비용·지연 완화에 유리함. 또한 LLM 미세조정(온프레미스) 가능 시 단가 절감과 일관성 향상 고려 가능하지만 데이터·규제 제약 존재함.  
안전성·검증: LLM 생성 설명은 권고로서 전문가 검증 루프(사후 검토)를 반드시 추가해야 함. 특히 운영 환경에서 환각·잘못된 인과추론으로 인한 잘못된 교육 제안이나 규정 위반을 방지하기 위해 인간-중심 확인 절차가 필요함.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(페이지 1–14)에 기반해 작성되었음. 수치는 본문 표와 본문 기술(데이터셋 크기, 임계값 θ=1.5g, 샘플 수 282/422, 모델별 성능 표 IV, ablation 표 V 등)에서 직접 추출함. 다만 CatBoost·TSFresh의 세부 하이퍼파라미터, TSFresh의 top-k 수치, LLM 프롬프트의 완전 원문(일부는 도식/요약으로 제시됨) 등은 PDF에 구체값이 없어 재현을 위해선 저자 코드·부록이나 추가 정보가 필요함.
