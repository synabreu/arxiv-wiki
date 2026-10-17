# MLExpert: Towards a Generalist Agentic Model for Autonomous Machine Learning Engineering

- **게시일:** 2026-10-17
- **arXiv:** [2610.22344v1](http://arxiv.org/abs/2610.22344v1) · [PDF](https://arxiv.org/pdf/2610.22344v1)
- **저자:** Shangheng Du, Jinxin Shi, Shuaiyu Zhang, Yiming Wu, Junpeng Zhao, Shiyang Feng, Xin Li, Liang He, Xiangchao Yan, Bo Zhang
- **분야:** cs.AI, cs.CL, cs.LG
- **선정 점수:** 6.91
- **선정 이유:** 최근성 0.8, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.6, 개발자 관심 0.6, 학술 신호 0.5, 오픈 웨이트·주요 연구조직 신호 2.5

[← 2026-10-17 목록으로 돌아가기](../daily/2026-10-17.html)

## 한 문장 요약

실제 Kaggle 기반 실행 환경에서 장기 상호작용을 통해 자동화된 기계학습 엔지니어링 정책을 학습하기 위해 Kaggle-MLE Factory와 상호작용 하니스, 계층적 agentic SFT 및 Windowed Interaction RL(WIRL)을 결합해 35B MoE 모델 MLExpert를 후속 훈련한 연구이다.

## 해결하려는 문제

기존 MLE(머신러닝 엔지니어링) 자동화 시스템은 외부의 수작업으로 설계된 워크플로우나 지역적(단계별) 의사결정에 의존해 장기 최적화(장시간 실험·피드백 반복)를 모델이 스스로 조직·수행하도록 훈련하기 어렵다. 특히 1) 실행 가능한 장기 상호작용 환경 구축의 어려움, 2) 이질적이고 긴 상호작용 궤적에서 고품질 감독(유용한 부분)만 선별해 학습하기 어려움, 3) 각 실험 결과가 여러 이전 결정에 의존하고 실험이 비용이 큰 상황에서 중간 피드백을 RL에 유효하게 활용하기 어렵다는 문제가 있다.

## 핵심 기여

- 35B Mixture-of-Experts(MoE) agentic 모델 MLExpert 제안 및 후속(post-)훈련 파이프라인 설계.
- Kaggle-MLE Factory로 역사적 Kaggle 경진대회를 실행 가능한 MLE 태스크로 변환하고 Interaction Harness로 모델 주도 장기 상호작용을 지원하는 실행 환경 구축.
- 계층적 agentic SFT(일반 도구·코드 사용 SFT → MLE 도메인 SFT)로 일반적 도구 사용성과 MLE 특유의 최적화 행동을 전이하도록 한 훈련 전략.
- Windowed Interaction RL(WIRL) 제안: 연속된 실험 결과 사이의 여러 결정들을 실행 윈도우로 묶어 공통의 결과 기반 보상을 부여하고 비동기 수집과 토큰 수준 정책 보정(token-level correction)을 적용해 중간 피드백으로 온라인 정책 최적화.
- 광범위한 평가( MLE-Bench Lite, NatureBench Lite, AIME scaffold, MLS-Bench-Lite )에서 SFT+WIRL의 효과 검증 및 동일 규모 베이스라인 대비 유의미한 성능 향상 보고.

## 접근 방법

* 아키텍처 및 학습 절차 요약: - 모델: 35B MoE(MLExpert), 초기화는 Qwen3.6-35B-A3B.
* - 실행 환경: Kaggle-MLE Factory는 역사적 Kaggle 대회를 자동 변환해 공개 워크스페이스, 숨겨진 테스트 라벨, 통일된 평가 인터페이스를 제공한다(160→154 유효 태스크).
* Interaction Harness는(solution nodes, 실험 트리, 도구 집합) 모델이 execute_code, update_answer, invalidate_node, analyze 등 도구를 호출해 실험을 조직·실행·관리하도록 설계된다.
* - 계층적 agentic SFT: 1단계 일반 도구/코드 사용 SFT(외부 StepFun 데이터)로 기본 능력 학습, 2단계 MLE 도메인 SFT로 MLE 초기화·장기 최적화·분석 행동 학습.
* 교사 궤적은 Kaggle-MLE Factory(154 tasks), MLE-Dojo(134 tasks), Nature 계열 논문 유도 과제에서 수집한 교사 궤적(총 보유 636 source trajectories, 5,539 input records).
* 실행 결과에 기반한 outcome-guided supervision으로 궤적의 유용한 prefix만 보존(품질 임계 η=0.4, 사후-peak 열화 임계 δ=0.05).
* 손실은 새로 생성한 추론/응답/툴콜 토큰에만 적용.
* - WIRL: 연속된 실험 결과(실행된 execute_code 호출들 사이)에 해당하는 여러 모델 출력 토큰을 하나의 실행 윈도우(um)로 묶고 윈도우 수준 보상 Rm을 부여(식(2)): 실행오류 -1.0, 제출 없음 -0.6, 유효 제출(메달 미달) -0.4+Tm, bronze/silver 1.0+Tm, gold 2.0+Tm; 여기서 Tm은 국지적 성능 추세(개선 +0.2, 동일 0, 악화 -0.2).
* 윈도우 단위로 공유된 보상 bAm=Rm을 모든 출력 토큰에 적용한 PPO 스타일 토큰-레벨 정책 손실(LB(θ), 식(4)).
* 비동기 수집을 사용하며 롤아웃 시 기록한 로그확률과 사전-업데이트 정책 로그확률로 토큰 수준 정책 보정을 수행(수정비 q_mjt = exp(l_old - l_roll); 보정구간 [qmin,qmax]=[0.2,4.0]; 영역 밖 토큰은 업데이트에서 제외).
* KL 정규화(λ_KL=1e-3)와 엔트로피 항(λ_H=1e-4) 적용, 윈도우당 출력 토큰 수로 정규화.
* 하이퍼파라미터 예: WIRL 배치 윈도우 B=32, 시퀀스 길이 최대 131,072 토큰, 샘플링 T=0.6,p=0.95,top-k=20.

## 주요 결과

- MLE-Bench Lite(22 tasks): MLExpert이 기반 모델(Qwen3.6-35B-A3B)의 Any Medal(=medal coverage) 비율을 37.9%에서 72.7%로 향상(표에서 MLExpert Any Medal 72.7% ± 2.62%). 같은 규모 비교군 중 최고 성능 달성, GLM-5.3·Kimi-K3 등 더 큰 모델과 유사 수준 성능.
- 후속 단계별 성능: Base 37.9% → General Agent SFT 47.0% → MLE SFT 62.1% → WIRL 72.7% (Table 3).
- WIRL 설계 비교(동일 MLE-SFT 초기화): GRPO 56.1% ±5.46, PPO-style 60.6% ±4.01, WIRL w/o trend reward 66.7% ±3.03, WIRL w/o policy correction 65.15% ±5.46, 전체 WIRL 72.73% ±2.62 (Table 4/10).
- NatureBench Lite(10 scientific tasks): Match-SOTA(M, g≥0) 비율 MLExpert 70.0% vs base 40.0%; Surpass-SOTA(S, g>0.1) MLExpert 50.0% vs base 0.0% (Table 2).
- AIME scaffold optimization(고정 GPT-4.1-nano solver): MLExpert가 생성한 scaffold의 held-out 정확도 43.7%(세 연도 평균)로 base 23.3% 대비 상승; MLExpert-SFT는 held-out 38.1% with 3.51 calls/problem, MLExpert (WIRL)는 43.7% with 8.40 calls/problem (Table 5/11).」「MLS-Bench-Lite(12 algorithm-component tasks): 평균 정규화 verifier reward가 Base 0.321543 → MLExpert 0.425198로 향상(MLExpert가 10개 과제에서 우수, 1개 동률, 1개 열세) (Table 12).

## 한계

- 저자가 명시한/논문에서 직접 언급된 제약: 긴 MLE 상호작용 훈련의 도전(환경 구축, 고품질 감독 선별, 중간 피드백 활용의 어려움)을 연구가 해결하려고 시도했지만, 본문에서는 여전히 '교사 궤적 필터링·수동 검토' 등 전처리·검증 단계가 필요함을 기록(예: 최종 수동 검토로 레이블/스코어 문제 있는 태스크 제외).
- 본문 실험·평가 범위에서 드러나는 제약(분석적 한계): MLExpert는 Qwen3.6-35B-A3B로 초기화된 후 동일한 하니스와 환경에서 평가되었으나 실험은 제한된 벤치셋(ML E-Bench Lite 22 tasks, NatureBench Lite 10 tasks 등) 및 특정 하드웨어·리소스 설정(작업당 최대 12시간, 20 vCPU, 220 GB RAM, NVIDIA H200)에서 수행되었음. 또한 WIRL의 보상 설계(메달 기반)와 outcome-guided supervision의 임계값(η=0.4, δ=0.05)은 벤치·환경에 특화되어 있으며 다른 도메인·스케일에서의 일반화 가능성은 본문 실험으로는 완전히 입증되지 않음.

## 개발자 관점

- 재현성·데이터 준비: Kaggle-MLE Factory 설계(대회 발견→스크래핑→분석→테스트 분할 생성→검증·수정→수동 리뷰)는 실험 기반 평가에 필수적이며, 교사 궤적 수집 시 중복·데이터 누수·레이블 문제를 적극 제거해야 한다(논문은 154개의 최종 태스크 보유).
- 훈련 파이프라인: 두 단계 계층적 SFT(일반 도구/코드 SFT → MLE SFT) 후 WIRL로 미세조정하는 순서를 권장한다. SFT 데이터 구성(총 636 source trajectories, 5,539 input records)과 packing 결과(1,173 sequences ≈ 302.45M tokens, MLE SFT 8 epochs)는 대규모 토큰 예산과 반복 학습 필요를 시사한다.
- 리소스·인프라: 각 태스크 당 상호작용 예산(최대 3,000 상호작용 단계, 최대 12시간 런타임)과 실행환경(20 vCPU, 220 GB RAM, NVIDIA H200) 요구가 높다. RL 단계의 비동기 수집 설계은 GPU/CPU 병목을 낮추지만(문서상 WIRL 평균 learner waiting fraction 39.3% vs GRPO 87.6%) 여전히 대규모 인프라가 필요하다.
- 구현·안정성 팁: outcome-guided supervision(품질 임계 η=0.4, 사후 열화 임계 δ=0.05)으로 '성능 피크 이후 열화'를 제거해 잘못된 꼬리( degraded tails )감지를 권장한다. WIRL에서는 토큰 수준 정책 보정([qmin,qmax]=[0.2,4.0])과 KL/엔트로피 정규화(λ_KL=1e-3, λ_H=1e-4)를 적용해 비동기 수집 시 정책 미스매치와 안정성을 관리한다.
- 배포·비용 고려: 모델 자체(35B MoE)와 장기 실험(수백M 토큰, 수천 상호작용, 여러 GPU/CPU 노드)은 운영·추론·훈련 비용이 높으므로 실제 서비스 전 배포·비용-효용 분석이 필요하다. 또한 WIRL로 더 높은 성능을 얻으려면 RL 추가 훈련 동안 더 많은 실행(예: AIME에서 호출 증가)을 허용해야 하므로 비용·시간-정책 트레이드오프를 고려해야 한다.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(본문과 부록 포함)에 근거해 작성되었다. 결과 수치·하이퍼파라미터·데이터 통계 등은 PDF에 직접 기재된 값을 사용했으며, 표와 부록에서 명시되지 않은 내부 구현 세부사항이나 실험 반복의 미보고 항목은 생성하지 않았다. 일부 추가 세부 구현(예: 구체적인 실행 스크립트, 전체 태스크별 원시 점수 분포)은 PDF에 포함되지 않거나 요약 수준으로만 제공되어 본 분석에선 기술하지 않았다.
