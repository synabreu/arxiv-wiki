# Context-Shielded Backdoor Attack against Large Vision-Language Models

- **게시일:** 2026-11-03
- **arXiv:** [2611.01252v1](http://arxiv.org/abs/2611.01252v1) · [PDF](https://arxiv.org/pdf/2611.01252v1)
- **저자:** Zhifang Zhang, Qiang Huang, Chenpeng Wang, Weitong Chen, Olaf Maennel, Wei Emma Zhang, Lei Feng, Lei Zhang, Miao Xu
- **분야:** cs.CV
- **선정 점수:** 4.63
- **선정 이유:** 최근성 0.5, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 1.6, 개발자 관심 0.6, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 1.7

[← 2026-11-03 목록으로 돌아가기](../daily/2026-11-03.html)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1. Inference-time visual-token compression strips surrounding clean context and activates STRIPWAKE. We evaluate LLaVA-](../assets/papers/context-shielded-backdoor-attack-against-large-vision-language-models/figure-1.jpg)

*Figure · 원문 PDF 2쪽 · Figure 1. Inference-time visual-token compression strips surrounding clean context and activates STRIPWAKE. We evaluate LLaVA-*

![Figure 2. Overview of the STRIPWAKE training pipeline. Only the two-layer vision-to-language projector gϕ is updated while the](../assets/papers/context-shielded-backdoor-attack-against-large-vision-language-models/figure-2.jpg)

*Figure · 원문 PDF 5쪽 · Figure 2. Overview of the STRIPWAKE training pipeline. Only the two-layer vision-to-language projector gϕ is updated while the*

![Figure 3. Activation, trigger survival, and clean utility across token budgets. All 576 tokens are at the left end of every axis. (a) ASR](../assets/papers/context-shielded-backdoor-attack-against-large-vision-language-models/figure-3.jpg)

*Figure · 원문 PDF 7쪽 · Figure 3. Activation, trigger survival, and clean utility across token budgets. All 576 tokens are at the left end of every axis. (a) ASR*

<!-- paper-visuals:end -->

## 한 문장 요약

STRIPWAKE라는 프로젝트터 전용 백도어를 제안하여 'context stripping' 현상을 이용해 전체 토큰 감사 시에는 비활성(dormant)하고 추론 시 비가시적 시각 토큰 압축이 적용되면(여러 미지의 압축기들에 걸쳐) 활성화되는 LVLM 백도어를 학습한다.

## 해결하려는 문제

기존 LVLM(backdoor) 공격들은 전체 토큰(full-token) 조건에서 거의 100%로 동작하여 공개·사전배포 감사(풀-토큰 입력 검사)에서 곧바로 탐지된다. 반면 실제 배포 파이프라인은 모델 가중치를 변경하지 않고(비트-투-비트 동일) 추론 시 시각 패치 토큰을 대폭 축소하는 시각-토큰 압축(토큰 프루닝)을 적용한다. 본 논문은 (i) 이 배포-압축 경로가 백도어 활성화에 미치는 영향과 (ii) 감사 시 비활성이고 압축 시 활성화되는 컴프레서-불가지론적(backdoor)을 어떻게 설계할지라는 문제를 다룬다. 저자가 제기한 핵심 관찰은 'context stripping'으로, 주변의 깨끗한 패치들이 트리거를 억제하다가 압축으로 인해 그 주변 문맥이 제거되면 백도어가 활성화된다는 점이다.

## 핵심 기여

- context stripping이라는 메커니즘을 규명: 트리거 생존(trigger survival)과 주변(clean) 토큰 제거(context removal)가 압축 시 백도어 활성화의 필요충분 조건임을 두 가지 인과적 개입(강제 보존/강제 제거, 그리고 clean-token 복원 실험)으로 입증함.
- STRIPWAKE 제안: 프로젝트터(vision-to-language two-layer MLP)만 미세조정하여 전체-토큰에서는 잠자고(비활성) 다양한 미지의 토큰 압축기들에서 활성화되는 압축-유발 백도어를 설계.
- 압축-불가지론적 훈련 구성: (i) 무작위 토큰 위치에 multiplicative tint 트리거(q=5%, 29/576) 적용, (ii) 풀-토큰·약한 프루닝(비활성) 뷰를 깨끗한 캡션으로 감독하고, 랜덤화된 surrogate 압축기군 P로부터 뽑은 압축 뷰들을 공격 목표문(고정 target string)으로 감독하는 context-shielded multi-view poisoning을 도입.
- clean 유틸리티 보존을 위한 benign-teacher attention regularization 제시: 언어모델의 초기 층(레이어 1–12)에서 마지막 프롬프트 토큰의 비주얼 어텐션 분포를 고정된 정상(benign) 교사와 JSD로 정렬하여 in-LLM 어텐션 기반 압축기에서 CIDEr 열화 방지.
- 광범위한 실험 검증: LLaVA-1.5-7B에서 9개의 공개된 압축기(사전·in-LLM 포함)와 여러 예제 및 개입 실험으로 STRIPWAKE가 풀-토큰에서 거의 비활성(≈0.4% ASR)하면서 k=64 등 실무적 예산에서 다수 압축기에 대해 94%–99.7% ASR를 달성하고(clean CIDEr 손실 거의 없음)를 보임.

## 접근 방법

* 모델/설정: LLaVA-1.5-7B(고정된 CLIP ViT-L/14 비전 인코더, 고정된 Vicuna-7B 언어모델, 학습 가능한 두-층 MLP 프로젝트터 gϕ)에서 프로젝트터만 미세조정한다.
* 트리거: 픽셀 단위가 아니라 패치 단위로 무작위로 선택한 q=5% (29/576) 패치에 multiplicative 채널 틴트(δ=96, 채널 부호 (+1,-1,+1))를 적용.
* 학습데이터/하이퍼: COCO 6,000장(포이즈닝률 ρ=5% → 300장 포이즌), AdamW lr=2e-4, 배치 32, 2 epoch.
* 목적함수(식(2)): Lclean + Ldorm + Lact + λ Lakd.
* 뷰 구성: 포이즌된 이미지에 대해 (1) 비활성 뷰들: 전체 N=576 토큰 CN(˜x)과 약한 프루닝 Cm(˜x), 둘 다 정답 캡션 y로 감독 → Ldorm; (2) 압축 뷰들: randomized surrogate compressors P에서 뽑은 두 개의 압축 뷰 P1(˜x), P2(˜x)를 공격 목표 문자열 t⋆로 감독 → Lact; 깔끔한 이미지들에는 전체 뷰와 P로부터의 압축 뷰를 y로 감독 → Lclean.
* surrogate 압축기 P는 다섯 축을 무작위화(k∈{48,64,96,128,192,256}, 깊이 d∈{0..4} with probs, 원래 위치 id vs repacked, 선택적 feature merging, 토큰 선택 규칙(score-mixed vs retention-controlled)).
* benign-teacher attention regularizer Lakd: 깨끗한 압축 뷰에서 언어모델 초기층 Λ={1..12}에 대한 마지막-프롬프트-토큰→비주얼 토큰의 헤드 평균 어텐션 분포(정규화)에 대해 JSD를 계산하여 고정된 benign 교사 gϕ0와 정렬(λ=15).
* 훈련 시 어떠한 실제 공개 압축기 C ∈C도 사용하지 않고 surrogate P만 사용하며, 시험시점에는 9개의 실제 공개 압축기들([CLS], VisionZip, DivPrune, FastV, SparseVLM, PruMerge, PruMerge+, VisPruner, FlowCut 등)을 적용하여 평가한다.

## 주요 결과

- 풀-토큰(모든 576 패치)에서 STRIPWAKE의 비활성: 전체 테스트(기본 300–500 이미지, 3 시드)에서 full-token ASR = 0.4% ± 0.2 (표 3).
- k=64(약 11% 토큰 유지)에서 주요 압축기들에 대한 압축 ASR(표 3): [CLS] 94.5% ± 0.2, VisionZip 94.0% ± 0.5, DivPrune 99.3% ± 0.6, FastV 99.6% ± 0.3, SparseVLM 99.7% ± 0.2.
- clean 캡셔닝 성능 보존(표 3): Clean 모델 Full CIDEr = 132.3; STRIPWAKE Full 132.0 (∆ −0.4 ±1.5), [CLS] 117.7 (∆ −0.4 ±3.2), FastV 110.0 (∆ +1.1 ±1.9). Lakd를 제거하면 FastV 및 SparseVLM에서 CIDEr가 4.9–6.2점 하락함(표 3, 표 5).
- 일반화(표 4): 추가 4개 사전-LLM 압축기에서 k=64 ASR: PruMerge 98.6% ±0.7, PruMerge+ 96.9% ±1.1, VisPruner 96.3% ±0.2, FlowCut 79.8% ±3.9. k=128에서는 모든 네 압축기에서 97.7%–99.7%로 상승.
- 메커니즘 개입(표 1·2): (1) 트리거 보존 강제: k=64에서 Force-keep trigger → ASR 100.0% ([CLS], Random 모두). (2) 트리거 제거 강제: Force-drop → ASR 감소([CLS] 35.7%, Random 30.9%). (3) 주변 깨끗한 토큰 복원(테이블 2): 트리거 29개 고정 상태에서 clean 토큰 c를 늘리면 ASR가 c=256까지 ≳97% 유지되다가 c=384에서 ≈48%로 급감, c=512에서 ≈1%로 붕괴 — 문맥(토큰 수)이 억제 메커니즘임을 입증.

## 한계

- 저자가 명시한 한계: 본 논문은 고정된 해상도/패치 분해능(336×336, N=576)과 현재 평가된 정적 이미지 압축에 초점을 맞추며, 향후 작업으로 동적 고해상도 타일링(dynamic high-resolution tiling)과 비디오 토큰 압축(video-token compression)으로의 확장을 제시함 — 즉 동영상·고해상도 시나리오에 대한 검증은 수행되지 않았음.
- 본문에서 확인되는 제약/제한점: (1) 실험은 LLaVA-1.5-7B(고정된 CLIP ViT-L/14 + Vicuna-7B)와 두-층 프로젝트터 설정에 한정되어 있어 다른 아키텍처·해상도·프로젝터 설계로의 일반화는 추가 검증이 필요함. (2) 트리거는 multiplicative tint 형태·무작위 패치 배치(q=5%, δ=96)에 의존하며, 다른 트리거 유형이나 인간 눈에 명확히 보이는 패치의 경우 탐지 가능성이 높아질 수 있음. (3) 일부 압축기(예: FlowCut at k=64)에서는 ASR이 상대적으로 낮게(≈79.8%) 나타나며, 모든 압축 규칙에 대해 100% 보장을 하지 않음. (4) 방어·검출 실험(예: 압축-경로별 감사·출력-변형 탐지 혹은 입력 기반 방어)에 대한 본문 측면의 검증은 제한적임.

## 개발자 관점

- 재현(필수 구성요소): LLaVA-1.5-7B 체크포인트, CLIP ViT-L/14 입력 해상도(336×336, N=576), 두-층 MLP 프로젝트터만 업데이트하는 코드, multiplicative tint 트리거(무작위 29패치, δ=96), surrogate 압축기 P의 무작위화 규칙(논문/부록의 샘플링 확률을 따라야 함), benign teacher gϕ0(무독성 교사로 동일한 P로 학습). 논문 부록(A)에 훈련 하이퍼파라미터(AdamW lr=2e-4, 배치32, 2 epoch, 포이즈닝률 5%)가 명시되어 있어 이를 그대로 따라야 유사한 결과를 얻을 가능성이 높음.
- 구현 세부: surrogate 압축군 P는 k, pruning depth d(확률 분포 포함), 위치 ID 재패킹, 선택 규칙(score-mixed vs retention-controlled) 등을 무작위화해야 하며, Lakd 계산을 위해 언어모델 초기층(레이어 1–12)에서 마지막 프롬프트 토큰에 대한 헤드-평균 어텐션을 추출·정규화해야 함(작은 안정화 상수 ε 사용).
- 배포·감사 시 교훈: 배포 전 감사는 '풀-토큰 입력만'이 아니라 실제 배포 파이프라인에서 적용될 압축 경로(여러 압축기·예산 k)를 포함해야 한다. 압축-경로를 따로 점검하지 않으면 STRIPWAKE와 같은 공격이 우회될 수 있음.
- 비용 및 실용성: 공격자는 프로젝트터만 미세조정하므로 계산 비용과 개발 비용이 낮음(6,000 이미지, 2 epoch). 방어자는 다양한 압축기를 시험하고 attention 기반 이상 징후(특히 초기 레이어의 프롬프트→비주얼 attention 분포 변동)를 모니터링하는 추가 비용을 고려해야 함.
- 안전성 권고: (i) 공개 모델을 감사할 때 다양한 압축 규칙과 예산(k)을 포함한 행동 검사(behavioral testing)를 수행하라; (ii) 초기 레이어의 시각-텍스트 어텐션 분포를 정상 모델(또는 benign teacher)과 비교하는 검증 절차를 도입하면 clean 유틸리티 보존 관점에서 이상 여부를 포착할 수 있음; (iii) 프로젝트터 수준의 변화만으로도 백도어가 가능하므로 공급망(프로젝트터·미세조정 데이터)의 무결성 검증이 필요함.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(주문서와 부록 포함)의 텍스트에 근거하여 작성되었다. 모든 수치(ASR, CIDEr, 표의 신뢰구간 등)와 구현·하이퍼파라미터(예: q=5%, δ=96, 학습률, 배치, epoch, surrogate P의 확률 분포)는 본문·부록에서 직접 추출한 값이다. PDF 본문에 없거나 명시되지 않은 내부 구현 세부(예: 코드 수준의 미세 구현, 랜덤 시드 처리 방식, 정확한 데이터 전처리 파이프라인)는 유추하지 않았으므로 재현 시에는 논문에 기재된 하이퍼파라미터와 부록 내용을 엄격히 따를 것을 권고한다.
