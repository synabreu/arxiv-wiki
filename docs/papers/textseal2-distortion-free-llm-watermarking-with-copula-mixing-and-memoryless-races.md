# TextSeal2: Distortion-Free LLM Watermarking with Copula Mixing and Memoryless Races

- **게시일:** 2026-11-01
- **arXiv:** [2610.40613v1](http://arxiv.org/abs/2610.40613v1) · [PDF](https://arxiv.org/pdf/2610.40613v1)
- **저자:** Tom Sander, Pierre Fernandez, Itai Gat, Haiming Bao, Jiaxin Shi, Jason Park, Valeriu Lacatusu, Sylvestre-Alvise Rebuffi, Hongyan Chang, Hady Elsahar, Tomáš Souček, Tuan Tran, Surya Parimi, Alexandre Mourachko
- **분야:** cs.CR, cs.AI, cs.CL
- **선정 점수:** 4.13
- **선정 이유:** 최근성 0.5, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.8, 개발자 관심 0.6, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-11-01 목록으로 돌아가기](../daily/2026-11-01.html)

## 한 문장 요약

TextSeal2는 두 개 이상의 키를 가우시안 공간에서 합성한 가상 키에 AutoMark의 Gaussian copula를 적용하고, speculative decoding에서는 초과(잔여) 지수 레이스(residual race)를 사용해 출력 분포를 왜곡하지 않으면서 수신(검출) 신호를 보존·증강하는 distortion-free LLM 워터마킹 방법이다.

## 해결하려는 문제

기존의 distortion-free 워터마크들은 (i) 키에 의해 토큰이 결정되면 다양성이 떨어지고, (ii) 키를 전부 알 수 없는 경우(예: TextSeal의 코인-플립 두 키 구성) 검출기가 어떤 키로 생성되었는지 모르는 상태에서 두 키 점수를 평균해야 하므로 신호 대비 잡음비가 감소하며, (iii) speculative decoding(초안(draft) 제출·검증) 하에서 교체된 토큰들이 워터마크 신호를 잃거나 수용(acceptance)율이 줄어드는 문제가 있었다. 또한 고성능 대안(textGrain)은 매 토큰마다 후-로짓(post-logits) 최적화(예: Sinkhorn 반복)를 수행해 지연을 발생시키거나 speculative 모드에서 수용율을 낮쓸 수 있다. 논문은 이런 한계들을 해결하면서 (왜곡 없음, 다양성 보존, 추론 지연 최소화, speculative decoding 수용율 보존)이라는 네 가지 요구사항을 동시에 만족시키는 워터마크 설계를 목표로 한다.

## 핵심 기여

- Copula mixing: 두 개(혹은 다중)의 키에서 나온 가우시안 값을 정규화하여 더한 뒤 AutoMark 스타일의 Gaussian copula로 섞어 하나의 가상 키(G⋆)를 만들고, 이 가상 키로 Gumbel-max(지수 레이스)를 수행하여 두 키를 코인-플립으로 라우팅할 때 잃던 신호 손실(신호대잡음비의 √2 감소)을 제거함.
- Residual race for speculative decoding: 초안(draft) 레이스들의 '여유(leftovers)'에 대해 하나의 추가적인 지수 레이스를 실행(relay/잔여 레이스)하여 block verification의 결과(I,y)를 재현함으로써 출력 분포의 완전 보존과 block verification의 수용율 보존을 달성함(명제 1).
- 강도(엔트로피 제거량) 보정: copula의 상수 파라미터 ρ가 토큰 엔트로피를 제거하는 정도를 엄밀하게 조절하며(정리 1), 실무에서는 단일 ρ로 여러 토큰 분포에서 원하는 엔트로피 예산에 근접하게 맞출 수 있음을 보임.
- 실험적 평가: 세 개의 LLM(예: Llama-3.1-8B, Qwen3.5-9B, Qwen3.5-27B)과 세 가지 도메인(ELI5, MBPP 코드, AIME 수학 문제)에서 기존 TextSeal(코인-플립), AutoMark copula, textGrain, SynthID-Text 등과 비교하여 검출 성능과 다양성·지연·speculative 수용율을 보고함.
- 공개검출 지원: 가상 키 구조는 하나의 하부 키(k(1))를 공개 키로 둘 수 있어 공개 검출을 지원하면서도 전체 검출 신호를 희석시키지 않음(추가 키를 합쳐도 전체 검출 능력은 보존됨).

## 접근 방법

* 핵심 아이디어는 두 단계다.
* (1) Copula mixing: 각 후보 토큰 v에 대해 두 키 j∈{1,2}으로부터 얻은 균등값 R^{(j)}_v를 표준정규공간으로 변환한 G^{(j)}_v = Φ^{-1}(R^{(j)}_v)를 계산하고 이들을 G⋆_v = (G^{(1)}_v + G^{(2)}_v)/√2 로 합친다.
* 그런 다음 AutoMark 식의 Gaussian copula로 가상 키 입력 Z_v = Φ(ρ G⋆_v + √(1−ρ^2) η_v)을 얻고, −ln Z_v 를 길이(E_v)로 하여 Gumbel-max / 지수 레이스(토큰 v는 길이 E_v 를 속도 p_v 로 달려 first-finish)를 수행해 샘플링한다.
* 이 구성은 모든 ρ에서 ˜R_v가 i.i.d.
* 균등이므로 단일-토큰 및 전체 시퀀스 평균 분포(키 평균)이 원 모델과 같아 distortion-free이다(Lemma 2).
* (2) Speculative decoding: drafter가 N개의 초안을 후보로 내면 각 위치 i에서 drafter 법칙 q_i로 레이스(초안 레이스)를 돌려 초안 토큰 d_i와 해당 레이스의 시간 τ_i를 얻는다.
* 각 레이스의 패자들(또는 남은 lane 길이)은 메모리리스 성질에 의해 다시 Exp(1)로 재표현되므로, 모든 위치의 'leftovers' 위에서 한 번 더 레이스(잔여 레이스)를 돌려 block verification의 정량적 결과(I, y)를 그대로 샘플링한다(식 (6)).
* 이로써 대체 토큰도 동일한 키-기반 신호를 지니고, block verification의 수용률과 출력 분포가 보존된다(Prop.
* 1).
* 검출은 각 (window, token) 쌍을 최초 발생 시 한 번만 점수화(−ln Φ(−G⋆_x) 등)하고 합산하여 Gamma 분포와 비교하는 기존 TextSeal의 검출 파이프라인을 그대로 사용한다.
* ρ는 토큰 엔트로피 제거량(∆(ρ; p))을 모수화하며 단일 상수로도 여러 분포에서 실무적으로 안정적인 엔트로피 제거 비율을 제공한다(정리 1 및 Appendix C).
* 구현적으로는 53-bit PRF(예: splitmix64) 사용을 권고하여 PRF 양자화로 인한 편향을 피함.

## 주요 결과

- 주요 비교 설정은 Self-BLEU(같은 질문에 대해 고정 키로 생성한 답변 간의 평균 BLEU, 낮을수록 다양성 큼)에서 동일한 다양성 수준으로 방법들 성능을 보간하여 비교함(검출 기준: false-positive rate 10^{-3}).
- without speculative decoding(표준 디코딩): TextSeal2(및 AutoMark copula)는 TextSeal의 코인-플립 대비 Llama-3.1-8B, Qwen3.5-9B, Qwen3.5-27B에서 각각 10, 22, 8 퍼센트포인트 더 많은 100-토큰 답변을 검출(페어드 95% 부트스트랩 구간 제시). AutoMark copula와 TextSeal2는 같은 분포를 가지므로 결과가 겹침.
- entropy-weighted test를 쓰면 모든 기법에서 검출 성능이 개선되며(예: 200토큰에서 4–23 포인트 개선), TextSeal2는 텍스트Grain과 전반적으로 유사한 검출력을 보이나 post-logits 최적화(예: Sinkhorn)가 필요 없음(Table 6).
- with speculative decoding(블록 검증, N=8 drafts, Qwen3.5-9B): TextSeal2는 100/200 토큰에서 각각 59% / 89% 검출을 달성했고, 같은 조건에서 TextSeal은 31% / 71%, textGrain은 31% / 67%, AutoMark copula는 25% / 60%, SynthID-Text는 17% / 50%를 기록함(모두 FPR=10^{-3}). 이로써 TextSeal2는 같은 수용률(acceptance) 조건에서 TextSeal 대비 대략 28 포인트(100-token) 혹은 18 포인트(200-token) 정도의 우위를 보임(본문의 페어드 비교 수치 참조).
- 수용률과 왜곡: 잔여 레이스는 block verification의 수용률(토큰/라운드)과 출력 분포를 정확히 보존함(Prop.1 및 구현 검사). 구현 시 53-bit PRF를 사용하면 −ln p_x − H(p) 같은 왜곡 검정에서 무의미한 차이를 보이며(13-bit PRF는 편향을 일으킴), TextSeal2는 key-only 작업을 forward pass와 겹쳐 실행하면 plain sampling 대비 0.6% 이내의 추가 지연만 발생함(Table 5). textGrain의 Sinkhorn 기반 post-logits 작업은 대체로 0.2–4 ms/토큰 범위의 추가 지연을 유발하며(구현/정규화에 따라 다름), TextSeal2는 post-logits 상에서 단 한 번의 어휘(전토큰) 패스만을 요구함(Table 4).

## 한계

- 저자가 명시한 한계: (a) 평가 데이터/모델 범위 제한 — ELI5(오픈형), MBPP(코드), AIME(수학) 및 세 가지 공개 가중치 모델(Qwen3.5-9B 등)과 온도 0.7–1 범위만 사용됨; (b) speculative-decoding 실험에서 블록 검증 대비 표준 디코딩은 2–4 포인트의 검출 손실이 있으며, 저자 구현은 배치 최적화가 없는(unbatched) 상태로 wall-clock 속도향상 수치는 제공하지 않음; (c) 공개 키를 악용하는 공격(공개 키 지식 활용 공격)에 대한 분석은 수행하지 않음; (d) textGrain는 코드가 공개되어 있지 않아 논문에서는 reimplementation을 사용했으므로 완전 동등 비교는 제한적임.
- 본문에서 합리적으로 확인되는 추가 제약(저자가 직접 명시하지 않은 부분 포함): (e) 이론 증명 상당부는 이상적인 PRF(키-값이 완전 균등 i.i.d.) 가정에 의존함 — 실무 PRF의 양자화나 상관성은 편향을 유발할 수 있음(따라서 53-bit PRF 권고); (f) 토큰 수준 워터마크는 파라프레이징(LLM에 의한 재문장화)에 매우 취약하여 거의 모든 신호가 제거됨(Table 7); (g) 잔여 레이스 구현은 수치적 세부(예: 라운드 경계에서의 반올림 처리 등)에서 주의가 필요하며, 구현 오차는 이론적 정확성 보장을 약화시킬 수 있음(Algorithm 1의 마감 처리 필요).

## 개발자 관점

- 재현성: 저자들이 코드(repo 링크)를 공개한다고 명시했으므로 공개 저장소를 통해 구현·검증 가능(본문에 URL 제시). 다만 textGrain는 공개 코드가 없어 재현 시 주의 필요(논문은 자체 reimplementation 사용).
- PRF 해상도: PRF 양자화는 샘플링 편향을 유발할 수 있으므로 53-bit 수준(PRF 예: splitmix64) 이상의 해상도를 권장함(13-bit는 편향 관찰됨).
- 성능·지연: TextSeal2의 post-logits 비용은 어휘 한 번 스캔 정도로 작아(한 토큰당 매우 낮음) key-only 작업을 모델의 forward pass와 겹쳐서 실행하면 실무적 추론 지연은 거의 없음(plain sampling 대비 ≲0.9%). 반면 textGrain 계열의 Sinkhorn 기반 방법은 토큰당 수 밀리초를 추가할 수 있어 실시간 추론/대규모 배포에서 비용 고려 필요.
- speculative decoding 통합: 블록 검증과 잔여 레이스(residual race)를 활용하면 speculative decoding의 acceptance를 보존하면서 워터마크 신호를 유지할 수 있음. 이를 적용하려면 초안 레이스의 leftover를 정확히 계산하고 단일 보조 레이스로 처리하는 Algorithm 1 스타일의 구현이 필요함(수치 안정성·반올림 처리 주의).
- 운영·보안 고려사항: 가상 키 구성은 하나의 하부 키를 공개 키로 둘 수 있어 공개 검출을 지원하지만 공개 키 공개는 공격자에게 목표를 제공할 수 있으므로(공개 검출 vs. 공격 표적 tradeoff) 실제 배포 시 공개/비공개 키 전략을 정책적으로 설계해야 함(탐지자·운영자 역할 분리 권고). 또한 파라프레이징 회피 등 능동적 제거 공격에 대비해 워터마크만 단독으로 신뢰하면 안 되며 다른 출처 추적 신호와 병행해야 함(본문 권고).

**근거 범위:** 분석은 제공된 논문 PDF 본문 전반(본문, 표, 보충자료 및 부록)을 근거로 작성함. 실험 수치, 명제 및 알고리즘 세부는 본문에 직접 기재된 내용에 한해 인용했으며, 텍스트Grain 관련 비교에서는 논문이 자체적으로 reimplementation을 사용했음을 반영함. 구현·성능 관련 수치는 논문에 보고된 실험과 표를 근거로 요약했으나, 저자의 공개 코드·환경과 재현 시 세부 파라미터(하드웨어, 라이브러리 최적화 등)에 따라 달라질 수 있음.
