# WRDO: Weighted Refusal Direction Optimization in Aligned Language Models

- **게시일:** 2026-10-22
- **arXiv:** [2610.29555v1](http://arxiv.org/abs/2610.29555v1) · [PDF](https://arxiv.org/pdf/2610.29555v1)
- **저자:** Grigoriy Evseev, Vladimir Solodkin, Dmitry Bylinkin, Daniil Medyakov, Vladimir Aletov, Aleksandr Beznosikov
- **분야:** cs.LG, cs.CL
- **선정 점수:** 5.12
- **선정 이유:** 최근성 1.1, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 1.5, 개발자 관심 0.0, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 2.2

[← 2026-10-22 목록으로 돌아가기](../daily/2026-10-22.html)

## 한 문장 요약

악성 요청에 대한 거부(refusal)를 단일 평균 방향 대신 유해 프롬프트별 방향들을 가중합하여 학습된 계수로 조합함으로써 거부 개입의 효과성과 유연성을 높이는 WRDO(Weighted Refusal Direction Optimization)를 제안한다.

## 해결하려는 문제

기존 작업은 거부 행동이 잔여 스트림(residual stream)의 단일 방향(유해/무해 활성화 차이의 평균 벡터)으로 매개된다고 보고하여 그 방향을 제거·직교화하면 거부가 무력화된다고 보였으나, 단일 방향 계산은 서로 이질적인 유해 프롬프트(예: 허위정보, 악성코드, 개인정보 침해)를 균일 평균으로 합쳐서 서로 다른 거부 관련 현상을 혼합할 위험이 있다. 논문은 프롬프트별 거부 방향을 가중 조합하면 단일 평균보다 더 강력하고 유연한 개입을 얻을 수 있는지를 묻는다.

## 핵심 기여

- 프롬프트별로 계산한 후보 은닉-방향 은행(candidate bank)을 학습된 가중치로 결합해 합성 거부 방향을 만드는 절차 WRDO를 제안했다.
- WRDO의 두 구현을 제안·실험했다: separable CMA-ES를 적응한 WRD-CMAES와 중요도표집을 포함한 GRPO 변형인 WRD-GRPO-IS.
- 세 개의 공개 가중치 모델과 세 개의 guard 판정기(및 외부 평가자 HarmBench)를 대상으로 WRDO가 기존 단일-방향 기법들을 일관되게 능가함을 보였다.
- WRD-GRPO-IS가 다른 방법들보다 일반 성능(utility)을 더 잘 보존함을 실험적으로 보였다(ARC, MMLU, GSM8K, WikiText PPL 등).
- 동일한 최적화 기법을 역으로 적용하여 제3자에 의해 거부가 제거된(abliterated) 체크포인트에서 거부를 복원하는 방어 실험을 제시했다.

## 접근 방법

* 핵심 구성 요소는 다음과 같다.
* (1) 후보 은닉-방향 은행: 각 유해 훈련 프롬프트 xi에 대해 모든 transformer 블록에서 마지막 토큰 위치의 잔여 스트림 활성화 h(l)(xi)에서 무해(benign) 평균 µ(l)_benign을 빼고 각 레이어별로 L2 정규화하여 ri ∈ R^{(L+1)×d}를 만든다.
* (논문에서 사용한 후보 수 N = 128, 샘플 시드 42.) (2) 가중 합성 방향: 계수벡터 w ∈ R^N를 통해 각 레이어별로 r(l)(w) = normalize(∑_i w_i r_i^{(l)})로 합성하고 레이어별로 L2 정규화한다.
* (3) 개입 연산자: Heretic과 동일한 weight-space orthogonalization을 사용하여 각 블록의 attention output projection W_O^{(l)}와 FFN down-projection W_down^{(l)}에 대해 W' = W - α^{(l)} r(l)(w) r(l)(w)^T W를 적용한다.
* 레이어별 강도 스케줄 α^{(l)}은 Heretic의 고정 스케줄을 사용하며 전역 강도 α는 {1.0,1.5,2.0,3.0}으로 실험.
* (4) 목표: 개입된 모델의 공격 성공률(ASR, guard 판정기 J에 대한 평균 위험 응답 비율)을 최소화하는 LJ(w) = -ASR_J(w).
* (5) 최적화: WRD-CMAES는 Optuna의 separable CmaEsSampler로 w를 박스 제약 [w_min,w_max]^N (논문: w_min=-2,w_max=2) 하에서 탐색(초기화는 균등 평균 wi=1/N, trials=50).
* WRD-GRPO-IS는 GRPO(그룹 상대 정책 최적화)를 변형하여 여러 행동 정책(각각 w+ε_m, ε_m ~ N(0,σ^2 I), M=8)을 stratified sampling하고 시퀀스 수준 중요도비(ev_m)를 도입해 off-policy 보정을 수행하는 surrogate(식 10)를 AdamW로 최적화한다.
* WRD-GRPO-IS는 무해 배치에 대한 KL(π_{intervened} \|\| π_{clean}) 정규화 항을 추가해 eLJ = LJ + β KL_w를 최적화(논문 기본 β=1000, 학습률 1e-3, epochs=50, σ=1).

## 주요 결과

- 공격 성능(ASR): 세 모델(Qwen3-8B-Base, allenai/OLMo-3-1025-7B, Olmo-3-7B-Instruct)과 세 판정기(WildGuard(WG), Q3G, LG3)에서 WRD-CMAES와 WRD-GRPO-IS가 대체로 기존 단일-방향 기법(Basic RD, Heretic, RDO, RDO-CONE)보다 높은 ASR를 달성했다(예: Qwen3-8B-Base, α=1.0에서 WRD-GRPO-IS의 ASR는 WG=0.91, Q3G=0.94, LG3=0.87; WRD-CMAES도 유사하게 높음; Table 1).
- 유틸리티 보존: WRD-GRPO-IS는 KL 정규화 덕분에 일반 능력 손실이 가장 작았다. 예를 들어 Qwen3-8B-Base에서 α=3.0일 때 WRD-GRPO-IS는 ARC-e 0.64, ARC-c 0.38, MMLU 0.62, GSM8K 0.83, WikiText PPL 11.35로 원모델(ARC-e 0.63 등)과 거의 유사한 성능을 보였다(표 2). 반면 Basic RD나 WRD-CMAES(ASR만 최적화)는 높은 α에서 MMLU·GSM8K 정확도 붕괴 및 PPL 폭등을 보였다.
- 외부 평가(HarmBench): HarmBench 분류기를 사용한 독립적 평가에서도 WRDO 방법이 우수했다. 예컨대 Qwen 계열에서 WRD-GRPO-IS는 α=1.0에서 HarmBench ASR 0.95를 기록해 다른 방법들을 능가했다(Table 3), 이는 과적합이 아니라 일반화된 취약성 증거임.
- 방어 실험: 제3자가 거부를 제거한(abliterated) 체크포인트(Llama-3.1-8B-Lexi-Uncensored-V2)에 대해 WRDO를 역으로 적용(α 부호 반전)하여 거부를 복원할 수 있었다. 예: α=-1.5에서 WRD-CMAES는 WG=0.011±0.004, Q3G=0.023±0.005, LG3=0.073±0.004로 큰 개선을 보였고 WRD-GRPO-IS도 유사한 방어 성능을 보였다(Table 4).
- 교차-판정기 전이성: 부호화된 교차-판정기 분석에서 WildGuard로 최적화한 w⋆는 다른 판정기로의 전이가 비교적 안정적이었으나, 일부 경우 판정기 특이적 성능 편향이 관찰되어 판정기별 신호 차이가 존재함(Table 9).

## 한계

- 저자가 명시한 한계: 실험은 7–8B 규모의 공개 체크포인트 세 개로 국한되어 있어 더 큰/다른 아키텍처에 대한 일반화가 확인되지 않았다.
- 저자가 명시한 한계: WRD-CMAES 구현은 본 논문에서 사용된 기본 버전이 ASR만을 목표로 하며 WRD-GRPO-IS에 사용된 KL 정규화를 아직 지원하지 않음(저자들은 Optuna 인터페이스 확장을 계획 중이라고 밝힘).
- 본문 근거로 확인되는 추가 제약: 후보 은행 구성은 N=128 고정 샘플(시드 42)과 무해 베이스(Alpaca 하위샘플 400개)에 의존하므로 은행 크기·구성이나 베이스 선택에 따른 민감도가 실험 범위에서 충분히 탐색되지 않음.
- 교차-판정기 전이성 한계: 판정기(guard)별로 학습된 w가 판정기 특이적 편향을 가질 수 있어, 하나의 판정기에 대한 최적화가 다른 판정기에서 항상 동일하게 잘 작동하지 않음(특히 Llama-Guard-3의 민감도 차이 관찰).

## 개발자 관점

- 실험적 추천 구성: 감사·공격·방어 용도로는 WRD-GRPO-IS(β=1000, AdamW lr=1e-3, epochs=50, M=8, noise σ=1)를 기본 구성으로 권장하며, WildGuard를 최적화 신호로 사용하는 것이 전이성과 안정성 측면에서 실용적이다.
- 재현성 주의사항: 후보 은닉-방향 은행은 N=128(시드 42)으로 구축하고 각 레이어별로 L2 정규화하여 저장해 재사용하라. 초기 w는 균등 평균(w_i=1/N)으로 설정한다.
- 구현·연산 비용: 논문 실험은 단일 NVIDIA H100(80GB)에서 수행되었고, WRD-GRPO-IS는 상대적으로 비용이 높아 약 11시간(attack-setup 기준)이 소요되는 반면 WRD-CMAES는 약 4시간 수준이었다(Table 8). 대규모 모델이나 대량의 평가 배치에서는 비용이 크게 늘어남을 고려하라.
- 배포·안전성: WRDO는 (논문 자체가 지적하듯) 이중 사용성(dual-use)이 있으므로 악의적 사용을 억제하기 위해 공개 코드·모델을 취급할 때 접근 통제, 감사 기록, 오프라인·제한적 평가 및 다층 안전 장치(외부 분류기·정책 엔진 병행)를 고려해야 한다.
- 방어 활용: 동일한 절차를 음수 강도로 적용하면 제3자에 의해 거부가 제거된 모델에서 거부를 복원할 수 있으므로 검증·포렌식 도구로서의 활용 가능성이 있다.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문 전체(본문 및 부록 표/수치 포함)를 근거로 작성되었다. 표와 부록의 수치(예: 표 1–6, 표 9–13, 하이퍼파라미터 표 7, 후보 은행 N=128, 시드 42, KL β=1000 등)는 PDF에 명시된 값에서 직접 인용했다. 코드·추가 실행 로그는 확인하지 못했으며, RDO-CONE과 gpt-oss-20b 관련 일부 비교는 단일 실행으로 보고되어 표준편차 정보가 없는 점은 원문에 명시된 그대로 반영했다.
