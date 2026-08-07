# Cooperative Coevolution for Resource-Constrained Agentic LLM Post-Training

- **arXiv:** [2608.02391v1](http://arxiv.org/abs/2608.02391v1) · [PDF](https://arxiv.org/pdf/2608.02391v1)
- **저자:** Zhiyuan Wang, Shengcai Liu, Jiahao Wu, Ning Lu, Hui Ouyang, Shaofeng Zhang, Haoze Lv, Ke Tang
- **분야:** cs.AI, cs.LG
- **선정 점수:** 12.46
- **선정 이유:** 최근성 0.7, 핵심어: large language model, 핵심어: llm, 핵심어: agent, 핵심어: efficient


### 한 문장 요약

CoPES는 전체 파라미터 공간을 K개의 저차원 서브스페이스로 협력적으로 탐색하는 파라미터-부분공간 진화 전략으로, 메모리 제약 하에서 에이전트형 LLM의 포스트-학습을 효율화하고 고정된 GPU-시간 예산 내에서 풀 파라미터 ES의 메모리 이점을 유지하면서 성능을 크게 끌어올린다.

### 해결하려는 문제

다중 턴의 도구 사용형 에이전트 LLM 포스트-학습에서 백프로파게이션 기반 학습이 필요한 활성화 저장 비용이 높아 메모리 한계에 직면한다. 반면 기존 진화전략(ES)은 메모리 측면에서 우수하지만 GPU-시간이 많이 들고, 자원 제약 환경에서 실용성이 떨어진다. 따라서 메모리 이점을 유지하면서도 고정 예산에서의 최적화 효율성을 높이는 방법이 필요하다.

### 핵심 기여

- CoPES를 제안하여 풀 파라미터 ES를 저차원 서브스페이스로 협력적으로 탐색하는 cooperative parameter-subspace evolution strategy를 도입했다.
- 차원 인식 perturbation 스케일링을 도입해 서브스페이스 perturbation의 에너지를 풀 스페이스와 맞추고, 동일한 업데이트 크기를 유지하도록 σk를 설정했다(σk = sqrt(K) σ).
- 서로 다른 서브스페이스의 보상들을 공동 표준화(joint reward standardization)하고 이를 바탕으로 전체 파라미터 업데이트를 동기화하여 각 서브스페이스의 추정치를 효과적으로 결합했다.
- 메모리-효율 구현을 위한 seed replay, chunked 처리, CPU 메모리 백업, partition replay 등을 통해 GPU 메모리 사용을 최소화하면서도 풀-파라미터 업데이트의 원칙을 유지했다. 또한 코드 오픈소스를 제공했다.
- 수학/QA 다섯 벤치마크와 하드웨어-적합성 및 제어 실험을 통해 K의 영향, 표준화 방식의 효과를 확인했고, ES와 LoRA-GRPO 대비 고정 예산하에서 CoPES의 성능 향상과 메모리 절감 효과를 실증했다.

### 접근 방법

* 문제 수식화와 알고리즘 흐름은 논문 본문과 보충자료에 기반한다.
* 에이전트 포스트-트레이닝 목표는 J(θ) = E_{x∼D, τ∼(πθ,E)(·\|x)}[R(τ)]이며, 풀이 방법은 다음과 같다.
* 1) 표준 ES 업데이트: d차원 파라메터 θ에 대해 N개의 가우시안 방향으로 θi = θ + σ εi를 샘플하고 각 perturbation으로 생성된 트래젝토리의 보상 ri를 얻어 평균 보상 µr, 표준편차 sr로 정규화한 후 θ+ = θ + α (1/N) ∑i ˆri εi를 업데이트한다.
* 2) Cooperative Subspace Search: 파라미터 벡터를 K개의 서로 소유 집합 Sk으로 무작위로 분할하고, 각 서브스페이스에 Nk = N/K perturbation을 할당한다.
* 각 서브스페이스에서 ϵk,i ∼ N(0, Idk)로 θk,i = θ + σk Pk ϵk,i를 만들고, 해당 서브스페이스에서만 perturbation을 수행해 rk,i를 얻는다.
* dk = d/K, σk = √K σ로 각 서브스페이스의 perturbation 규모를 보정한다.
* 3) 보상 표준화 및 업데이트 합성: 모든 rk,i를 하나의 공동 평균 µc와 표준편차 sc로 표준화하고 gk = (1/Nk) ∑i ˆrk,i ϵk,i를 계산한 뒤 θ+ = θ + α Σk Pk gk를 통해 풀 업데이트를 구성한다(동시성 있게 적용).
* 4) 메모리-효율 구현: perturbation 벡터를 재생성(seed 재생)하고, 파라미터를 청크별로 처리하며, perturbation 전에 pre-update weights를 CPU 메모리에 백업하고 perturbation 평가 후 복구한다.
* 또한 partition의 랜덤 시드를 저장하여 파라미터-수준 마스크 없이도 재생이 가능하도록 한다.
* 알고리즘 1에 요약된 한 사이클은 이 흐름으로 진행된다.
* 5) 실험 구성에 따른 하이퍼파라미터: N=40, σ=1e-3, α=5e-4, K=4(기본값), σk=2σ, Nk=10으로 설정하고, 16-step 고정 예산과 32-step/QA 예산 등 task별 설정을 Supplementary에 따른다.

### 주요 결과

- 기계 학습 연구자 실험에서, 자원 제약 하의 포스트-학습 예산으로 GRPO의 최고 검증 성능이 달성되는 GPU-시간 예산을 기준으로, CoPES는 GRPO의 검증 정확도 향상분의 92%를 회복하고, 표준 ES의 67%에 비해 더 우수한 성능 향상을 보였다.
- 이론적 GPU 메모리 요구량은 풀 파라미터 GRPO의 1/8 미만으로 추정되며, 128K 컨텍스트 길이에서 MES/CoPES의 메모리 필요량은 약 12.78GB로 추정되고, 풀 GRPO의 시나리오는 약 453.44GB에 달한다( Mfull(L) = 69.44 + 3L GB; L=128K일 때). LoRA 기반 GRPO는 약 402.55GB.
- 메모리-효율 ES 기반 방법들보다 더 낮은 메모리로도 동등한 예측 공간에서 동작하며, 128K 컨텍스트에서 ES/CoPES의 메모리 총합은 12.78GB로 추정된다. 이는 LoRA-GRPO의 메모리 추정치보다도 크게 낮다.
- 하드웨어 자원 제약 하에서 ES 계통의 방법은 단일 24GB GPU에서도 구현 가능하였고, GRPO 계열은 8×48GB GPU가 필요했다. 따라서 자원 제약 하에서 ES 기반 방법이 실용적이라는 점이 확인됐다.
- 정량적 벤치마크 결과에서 CoPES는 수학 태스크의 다섯 벤치마크와 QA 태스크의 세 벤치마크에서 표준 ES와 LoRA-GRPO를 상회하거나 근접했고, Qwen3.5-4B 대비 성능 회복과 일반화 측면에서 강점을 확인했다. 예를 들어 수학 벤치마크에서 pass@1은 AIME2024 38.39%, AIME2025 52.75%, GSM8K 92.57%, MATH-500 88.29%, MATH-Test 90.16%를 기록했다(16-step 예산). QA 벤치마크에서는 2Wiki Acc 59.06%, EM 48.29, F1 55.50; HotpotQA Acc 53.30%, EM 46.96, F1 58.83; MuSiQue Acc 29.68%, EM 23.34, F1 33.73으로 나타났다.

### 한계

- Author-stated 한계: 현재 실험은 Qwen3.5-4B 두 태스크에 한정되며, 더 넓은 모델이나 에이전트 환경으로의 일반화는 향후 확장 필요하다. 적응적 파라미터 공간 분할(adaptive partitioning) 같은 고도화된 구성은 아직 도입되지 않았다.
- 실험적 한계: 메모리 계측은 이론적 추정으로, gradient checkpointing/오프로딩/퓨전 커널 등 프레임워크 특유의 메모리 최적화를 배제한 상태의 추정치이다. 실제 런타임에서의 메모리 사용은 다를 수 있다.
- 또 다른 한계: 컨텍스트 길이 128K, 킷 수(K=4)와 고정 예산(수치의 16스텝/QA 예산) 하에서의 실험이 주류이며, 다른 예산이나 컨텍스트 규모에서의 일반화는 아직 확인되지 않았다.
- 하드웨어 의존성: 실험은 8× RTX 5880 Ada 등 특정 하드웨어 구성에 의존하므로, 다른 하드웨어에서의 재현 시 성능 차이가 있을 수 있다.

### 개발자 관점

- CoPES 구현을 위한 기본 파라미터 구성은 K=4, Nk=10, σ=1e-3, σk=2e-3, α=5e-4로 시작하되, Nk가 10 미만으로 떨어지지 않도록 관리한다.
- 메모리-효율 구현의 핵심은 perturbation 벡터의 재생(seed replay), 파라미터 청크 처리(chunking), pre-update weights의 CPU 백업 및 partition seed 재생이다. 이를 통해 GPU 메모리 불확실성 및 부동 소수점 비가역성으로 인한 누적 오차를 방지한다.
- 표준화 전략은 서브스페이스 간의 개별 표준화가 아닌, 모든 보상을 하나의 공통 평균/표준편차로 합쳐서 가중치를 합성하는 joint standardization을 사용한다. 이 방식이 다중 서브스페이스의 업데이트를 보다 안정적으로 만들고 성능을 끌어올린다.
- 서브스페이스 간 비상호작용을 고려하되, 서브스페이스 간의 독립적 표준화보다 공동 표준화가 성능에 이득이 크다. 또한 서브스페이스 수(K)를 늘리되 Nk가 충분히 크도록 하여 업데이트 품질을 유지하는 것이 중요하다.
- 코드의 재현성을 위해 공개 코드를 활용하고, 메모리 제약 환경에서의 벤치마크를 구성할 때는 128K 컨텍스트/다중 턴 태스크를 기본으로 삼되, 하드웨어 차이를 보정한 GPU-시간 추정치를 제시하는 것이 필요하다.

## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: Overview of CoPES. At each training step, the model parameters are randomly partitioned into K disjoint subspaces,](../assets/papers/cooperative-coevolution-for-resource-constrained-agentic-llm-post-training/figure-1.jpg)

*Figure · 원문 PDF 4쪽 · Figure 1: Overview of CoPES. At each training step, the model parameters are randomly partitioned into K disjoint subspaces,*

![Figure 2: Theoretical GPU memory requirements versus con-](../assets/papers/cooperative-coevolution-for-resource-constrained-agentic-llm-post-training/figure-2.jpg)

*Figure · 원문 PDF 5쪽 · Figure 2: Theoretical GPU memory requirements versus con-*

![Figure 3: Pass@k of four post-training methods under the 16-step full-parameter GRPO budget, with Qwen3.5-4B and Qwen3.5-](../assets/papers/cooperative-coevolution-for-resource-constrained-agentic-llm-post-training/figure-3.jpg)

*Figure · 원문 PDF 6쪽 · Figure 3: Pass@k of four post-training methods under the 16-step full-parameter GRPO budget, with Qwen3.5-4B and Qwen3.5-*

<!-- paper-visuals:end -->

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: Overview of CoPES. At each training step, the model parameters are randomly partitioned into K disjoint subspaces,](../assets/papers/cooperative-coevolution-for-resource-constrained-agentic-llm-post-training/figure-1.jpg)

*Figure · 원문 PDF 4쪽 · Figure 1: Overview of CoPES. At each training step, the model parameters are randomly partitioned into K disjoint subspaces,*

![Figure 2: Theoretical GPU memory requirements versus con-](../assets/papers/cooperative-coevolution-for-resource-constrained-agentic-llm-post-training/figure-2.jpg)

*Figure · 원문 PDF 5쪽 · Figure 2: Theoretical GPU memory requirements versus con-*

![Figure 3: Pass@k of four post-training methods under the 16-step full-parameter GRPO budget, with Qwen3.5-4B and Qwen3.5-](../assets/papers/cooperative-coevolution-for-resource-constrained-agentic-llm-post-training/figure-3.jpg)

*Figure · 원문 PDF 6쪽 · Figure 3: Pass@k of four post-training methods under the 16-step full-parameter GRPO budget, with Qwen3.5-4B and Qwen3.5-*

<!-- paper-visuals:end -->

**근거 범위:** 논문 PDF 본문 기반 분석. Supplementary Material에 수치 및 구현 세부가 병기되어 있어 본문 텍스트만으로 해석한 부분은 일부 수치가 표 위치나 형식에 따라 다르게 읽힐 수 있다. 가능한 경우 원문 표/수치를 상응하는 Supplementary 자료와 대조하는 것을 권장한다.

---

- **소개 날짜:** 2026-08-05
- [← 2026-08-05 논문 목록으로 돌아가기](../daily/2026-08-05.md)
- [일별 아카이브 보기](../daily/index.md)

