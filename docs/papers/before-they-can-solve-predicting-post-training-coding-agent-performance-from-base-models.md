# Before They Can Solve: Predicting Post-Training Coding-Agent Performance from Base Models

- **게시일:** 2026-10-08
- **arXiv:** [2610.10478v1](http://arxiv.org/abs/2610.10478v1) · [PDF](https://arxiv.org/pdf/2610.10478v1)
- **저자:** Tan Yu, Alexander Bukharin, Khushi Bhardwaj, Jennifer Williams, Zirui Liu, Jonathan Lingjie Li, Soumye Singhal, Joseph Jennings, Sanjeev Satheesh, Yash Jain, Ashish Vaswani, Venkat Krishna Srinivasan, Matthew Papakipos, Hyunwoo Kim, Jian Zhang, Oleksii Kuchaiev, Markus Kliegl, Mostofa Patwary, Mohammad Shoeybi, Bryan Catanzaro, Jonathan Cohen, Jiantao Jiao
- **분야:** cs.AI, cs.SE
- **선정 점수:** 6.10
- **선정 이유:** 최근성 1.3, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.2, 개발자 관심 0.8, 학술 신호 0.6, 오픈 웨이트·주요 연구조직 신호 1.2

[← 2026-10-08 목록으로 돌아가기](../daily/2026-10-08.html)

## 한 문장 요약

성공한 에이전트 궤적을 되돌려 '결정적 단계'를 찾아 그 단계에서의 베이스 체크포인트 행동 확률·판별·샘플링 성능으로 포스트-트레이닝된 코딩 에이전트 성능을 높은 상관으로 예측하는 방법을 제안한다.

## 해결하려는 문제

포스트-트레이닝(에이전트화) 전에 어떤 베이스 체크포인트를 골라야 할지 예측하는 문제를 다룬다. 기존 방식은 두 가지로 실패한다: (1) 엔드투엔드 pass@K는 베이스 모델이 도구 호출·에이전트 인터페이스를 신뢰성 있게 다루지 못해 대부분 0에 묶여 실용적 분별력을 잃음(특히 장기 에이전트 작업), (2) 단일-샷/제한된 호라이즌 평가(기능 합성 벤치)는 반복적 도구 사용·저장소 상태 변화에 따른 장기 연속성 능력을 테스트하지 못해 포스트-트레이닝 성능과의 상관이 일관되지 않음. 연구 질문: 베이스 체크포인트가 향후 에이전트 성능으로 이어질 '잠재력'을, 에이전트 궤적과 작업 검증기(verifier)를 이용해 어떻게 선(先)예측할 수 있는가?

## 핵심 기여

- 에이전트 궤적 재생(replay)과 검증기 실행을 통해 '결정적 단계(T*)'를 발견하고 그 단계의 행동(y*)을 golden action으로 규정하는 일반적 프로토콜을 제안함(임의의 에이전트-코딩 벤치로 확장 가능).
- 결정적 단계에서의 정적·비교적 스크린: Decisive-Action BPB(행동의 byte-normalized 음(負)로그우도), Patch MCQ(검증기에서 합격된 golden action과 실패 distractor들을 공동 문맥에서 답지(답글자) 우도 비교) 를 설계·제안함.
- 동적(샘플링) 스크린: prefix-conditioned pass@K(결정적 단계 직전(prefix)에서 베이스 체크포인트로 K개의 연속 생성(rollouts)을 수행하고 검증기로 합격하는 샘플이 있는지 측정) 를 제안함.
- 대규모 실험에서 제안된 세 스크린이 포스트-트레이닝 SWE-bench Verified pass@1 순위와 높은 순위 상관을 보이며(여러 소스 궤적을 사용해 교차 검증), 기존의 바운디드 코드 벤치마크들이 일관된 신호를 주지 못함을 실험적으로 보였음.
- 실용적 인프라·절차 세부사항(템플릿 마스킹, 결정적 단계 탐색을 위한 이분법(bisection)으로 검증 실행 횟수 절감, base->agent 브리징 프롬프트 설계, MCQ 회전(cyclic rotation)집계 등)을 제시하고 주요 설계 선택을 평가(ablations).

## 접근 방법

* 전체 절차 요약: (1) 성공한 에이전트 궤적(프론티어 포스트-트레이닝 모델로 수집)을 기록(proxied capture)하고, 궤적의 코드 변경 단계 집합 C를 재생(replay)하면서 각 누적 패치 P_{≤T}에 대해 작업 검증기 V를 실행해 결정적 단계 T* = 최소 T∈C s.t.
* V(P_{≤T})=1을 찾는다.
* 이때 궤적 직전의 컨텍스트 x*와 결정적 단계의 모델 응답 y*를 golden action으로 정의한다.
* (2) 세 가지 프로브를 T*에서 적용: Decisive-Action BPB — prefix x*‖y*에 대해 y* 토큰의 음의 로그우도 L(θ)를 바이트 길이로 정규화한 BPB(단, 채팅 템플릿의 고정 포맷 토큰은 마스킹)로 점수화(낮을수록 좋음).
* Patch MCQ — 같은 prefix에서 포스트-트레이닝 모델들로 후보 행동 집합 Y를 샘플해 검증기에서 실패하는 distractor들 Y^-을 구성하고, 베이스 체크포인트에 4지선다(옵션을 cyclic rotation) 맥락을 제시해 답지(문자) 우도를 읽어 정답 선택률을 계산(조합적 비교이므로 정적 판별 평가).
* Prefix-conditioned pass@K — 결정적 단계 직전의 누적 패치 P_{≤T*-1}을 복원한 컨테이너 상태에서 베이스 체크포인트로 K회의 연속 포워드(각 시도는 최대 3 생성 단계 예산)를 실행해 각 롤아웃의 패치를 검증기로 평가, 인스턴스 수준에서 '적어도 하나 통과'하면 성공으로 계산.
* (3) 인프라 최적화: 결정적 단계 탐색은 C를 선형 스캔하지 않고 이분법으로 확인 횟수를 O(log\|C\|)로 줄임, prefix 캐시(컨테이너 이미지+대화 로그)로 반복검증 비용 절감, MCQ는 cyclic rotation으로 위치 바이어스 제거 및 재현성 증가, prefix->base 브리지(프롬프트: transcript‖steer‖primer‖prefill)로 베이스 모델이 구조화된 도구 호출을 생성하도록 유도.

## 주요 결과

- 주 실험 코호트: 10개 공개 베이스 체크포인트(Nemotron Nano/Super/Ultra, Qwen-3.5-35B-A3B-Base, DeepSeek V4 Flash/Pro Base, Kimi-K2-Base, GLM-4.5-Air-Base, Hy3-Preview-Base, Gemma-4-26B)와 각 가족의 포스트-트레이닝 SWE-bench Verified pass@1을 다운스트림 목표로 사용(표 참조, 본문 Table 6).
- Decisive-Action BPB: DeepSWE 출처의 궤적으로 계산한 BPB는 포스트-트레이닝 SWE-bench Verified pass@1과 Pearson r=0.965, Spearman ρ=0.964를 기록(figure 3a, page 7–8). 전체 단계 평균 BPB 대비 '결정적 단계'만 점수화하면 Spearman ρ가 0.915 → 0.964로 개선(figure 2).
- Patch MCQ: DeepSWE 유래 패널에서 joint answer-letter(회전+집계) + think(추론) 1000 토큰 설정으로 SWE-bench Verified pass@1과 최대 상관(예: DeepSWE→SWE-Verified 경로에서 Pearson r≈0.915, Spearman ρ≈0.867–0.903, 자세한 조합은 본문 참조, fig.3b, table 13). 독립적 점수(argmin-BPB)보다 공동 문맥 판독이 훨씬 높은 다운스트림 순위 일치(예: argmin-BPB ρ≈0.665 vs rotated-read ρ≈0.867).
- Prefix-conditioned pass@K: DeepSWE 유래 prefixes에서 K=8/16/32일 때 Spearman ρ는 0.915/0.952/0.951(DeepSWE→SWE-Verified); SWE-bench Verified 동일-벤치 prefixes에서 K=8 및 16에서 ρ=0.988(높은 동일-벤치 일치), K=16이 대부분의 순위 일치를 확보하며 K 증가가 항상 개선으로 이어지지 않음(본문 Table 3, Fig.12).
- 엔드투엔드(베이스 모델을 그대로 에이전트로 구동) 평가는 대부분 체크포인트에서 pass@1=0으로 묶여 순위 판별 불가능(본문 Table 8), 따라서 제안된 '결정적 단계 기반' 접근의 필요성을 실험적으로 확인함. 또한 APTBench(SWE-MCQ)의 독립 감사 결과 원본 MCQ의 43.2%가 'Invalid'로 판정되어(Appendix A) 기존 MCQ 기반 방법의 한계 강조됨.

## 한계

- 저자가 명시한 한계: (i) 제안된 스크린은 성공한 에이전트 궤적과 해당 작업의 실행 가능한 검증기(verifier)를 필요로 함 — 즉, 프론티어 포스트-트레이닝 모델로부터의 '성공 궤적'과 실행 가능한 테스트가 전제되어야 함; (ii) 실험은 10개 베이스 체크포인트 코호트에 기반하며 downstream 포스트-트레이닝 모델들은 각기 다른 연구실의 상이한 후속 트레이닝 레시피 및 하니스에서 나온 결과를 사용하므로 완전한 통제 비교가 아님(본문 C절, 통계 프로토콜 참조).
- 본문에서 합리적으로 확인되는 추가 제약: (i) 샘플 기반 prefix pass@K는 결정적 단계의 포맷·프롬프트 브리징 방식 및 prefilling 설계에 민감하며, 베이스 모델이 도구 호출 형식을 따르도록 만드는 엔지니어링이 필요함(본문 J절); (ii) MCQ·BPB 수치에는 재실행(런-투-런) 스프레드가 저장되지 않아(본문 C) 개별 소폭 차이를 정밀하게 해석하기 어려움; (iii) 일부 벤치(예: Terminal-Bench)로의 전이는 트레이저리 소스의 도메인 차이 때문에 성능 차이를 보이며(본문 G), 트레이저리 출처 의존성 존재; (iv) 통계적 불확실성(부트스트랩 구간 없음)과 작은 n(특히 SFT 제어 실험은 n=3)이 있어 예측력의 일반화 추정에 한계가 있음(본문 D, K).

## 개발자 관점

- 베이스 체크포인트로 에이전트 후속 학습을 결정하기 전에 '결정적 단계' 기반 스크린을 적용하면 엔드투엔드 베이스 평가보다 훨씬 실용적이고 예측력이 높음 — 필요한 입력은 성공 궤적과 실행 가능한 검증기뿐임.
- 구현 팁: 결정적 단계 탐색은 궤적의 변경 단계 집합 C를 재생 후 이분법(bisection)으로 찾아야 검증기 실행 횟수를 크게 줄일 수 있음(복원/검증 비용이 핵심 병목).
- BPB 적용 시 채팅/도구 포맷 토큰은 마스킹하고 바이트 정규화(BPB)를 사용하면 다른 토크나이저 간 비교가 가능함(본문 H.1, Fig.7a).
- Patch MCQ는 옵션을 각각 독립 점수화(argmin-BPB)하지 말고 공동 문맥에서 answer-letter 우도를 읽는 방식(사이클 회전+집계)이 좋음; reasoning(think) 단계는 소폭 개선하지만 핵심은 공동 스코어링임(본문 I, table 13).
- prefix-conditioned pass@K의 실무 설정: base->agent 브리지(프롬프트: transcript‖steer‖primer‖prefill)와 'action envelope' prefilling이 베이스 모델이 파싱 가능한 도구 호출을 내도록 만드는 데 필수이며, K≈16이 실용적 균형임(샘플 비용 대비 순위 일치). 또한 컨테이너 이미지+대화 로그 캐시를 구현하면 반복 prefix 재생 비용을 크게 낮출 수 있음(본문 J).

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(본문, 그림, 표 및 부록 설명)을 직접 근거로 작성했다. 본문에 명시된 수치(예: Pearson r, Spearman ρ, pass@K 값 등)와 실험 설정을 인용했으며, 본문에서 저자가 직접 언급하지 않은 세부 재현 변수(엔드포인트별 런-투-런 분산, 추가 하이퍼파라미터 미기재 항목 등)는 생성하지 않았다. 일부 비교는 본문이 보고한 서로 다른 소스(DeepSWE vs SWE-bench Verified 등)에 따른 결과를 함께 인용했으며, 논문 자체가 부트스트랩 불확실도(신뢰구간)를 제공하지 않아 통계적 불확실성은 본문 기술대로 '서술적'으로만 보고됨.
