# CAT-alyzing Honesty: Continuous Adversarial Training for Transferable LLM Honesty

- **게시일:** 2026-10-17
- **arXiv:** [2610.22292v1](http://arxiv.org/abs/2610.22292v1) · [PDF](https://arxiv.org/pdf/2610.22292v1)
- **저자:** Yuan-Chen Chang, Niklas Herbster, Gauthier Gidel, Tommaso Tosato
- **분야:** cs.LG, cs.CL, cs.CY
- **선정 점수:** 5.51
- **선정 이유:** 최근성 0.8, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 3.0, 개발자 관심 0.2, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 1.2

[← 2026-10-17 목록으로 돌아가기](../daily/2026-10-17.html)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: Continuous Adversarial Training for Consistent Honesty (CATCH). Honesty learnt with Con-](../assets/papers/cat-alyzing-honesty-continuous-adversarial-training-for-transferable-llm-honesty/figure-1.jpg)

*Figure · 원문 PDF 1쪽 · Figure 1: Continuous Adversarial Training for Consistent Honesty (CATCH). Honesty learnt with Con-*

![Figure 2: CATCH improves honesty in MASK. MASK honesty of mitigation methods on Llama-3.3-70B-](../assets/papers/cat-alyzing-honesty-continuous-adversarial-training-for-transferable-llm-honesty/figure-2.jpg)

*Figure · 원문 PDF 4쪽 · Figure 2: CATCH improves honesty in MASK. MASK honesty of mitigation methods on Llama-3.3-70B-*

![Figure 3: CATCH Impostors in Among Us win less and confess more. Each honesty-intervened model](../assets/papers/cat-alyzing-honesty-continuous-adversarial-training-for-transferable-llm-honesty/figure-3.jpg)

*Figure · 원문 PDF 5쪽 · Figure 3: CATCH Impostors in Among Us win less and confess more. Each honesty-intervened model*

<!-- paper-visuals:end -->

## 한 문장 요약

연속적 적대적 훈련(CATCH)을 도입해 수백 개 수준의 '정직/기만' 대조 타깃으로 Llama-3.3-70B-Instruct와 Qwen3.6-27B에 미세조정(LoRA+QLoRA)하여 정직성(honesty)을 크게 향상시키고 범용성(transfer)과 유틸리티 보존을 동시에 달성한다.

## 해결하려는 문제

정렬(Alignment)훈련을 거친 대형언어모델(LLM)도 여전히 맥락이나 내부지식과 모순되는 주장(거짓 진술 또는 부정확한 주장)을 하며, 기존의 추론 시 스티어링(activation steering), 정직 프롬프트, 감독적 미세조정(SFT) 등은 특정 유형의 부정직성에는 효과적이지만 다른 유형으로 일반화(transfer)되지 않거나 유틸리티(기능성)를 크게 해치는 단점이 있다. 본 논문의 연구 질문은 '하나의 학습-time 개입으로 서로 다른 발생 형태의 부정직성(지시된 거짓, 게임 인센티브로 인한 거짓, 훈련으로 은폐된 거짓)을 줄이되 모델 능력은 유지할 수 있는가'이다.

## 핵심 기여

- CATCH(Continuous Adversarial Training for Consistent Honesty)를 제안하여, 문맥별로 구성한 정직 타깃(y+)과 기만 타깃(y−) 쌍에 대해 임베딩 공간에서의 연속적 적대적 교란을 생성하고(toward/away unlikelihood + 유틸리티 손실) 모델을 학습시켜 정직 행동을 강화함.
- 소수(약 200개 수준)의 self-reporting 기반 대조 타깃으로 학습하더라도 학습된 정직 행동이 다른 벤치마크(MASK, Among Us, AuditBench)로 강하게 이전(transfer)됨을 실증함.
- Llama-3.3-70B-Instruct 및 Qwen3.6-27B에 대해 CATCH가 prompting, SFT 계열, CAPO(IPO/DPO 변형), 그리고 최신 activation steering(StTP)과 비교해 정직성 개선에서 우수하거나 대등하고, 특히 유틸리티 보존 측면에서 우수함을 보임.
- 유틸리티(기능) 보존에 있어 유틸리티 데이터 선택이 결정적임을 밝히고, 'on-policy'로 생성한 유틸리티 코퍼스(Magpie 계열)를 쓰면 기존의 off-policy 코퍼스(UltraChat)보다 능력 저하를 훨씬 적게 유발함을 실험적으로 입증함.
- 기술적 재현성을 위해 학습 구성(QLoRA, LoRA 하이퍼파라미터, 적대적 내/외부 루프 설정 등)과 평가 프로토콜(MASK, Among Us, AuditBench, AlpacaEval/MT-Bench/MMLU)을 상세히 제시하고 코드·데이터 공개 계획을 밝힘.

## 접근 방법

* CATCH는 Continuous Adversarial Training(CAT)을 정직성 문제에 맞게 수정한 방법이다.
* 각 입력 프롬프트 x에 대해 정직한 계속(y+)과 기만적 계속(y−)을 대응시키고, 내적(embedding)공간에서 제한 반경 ϵ 이내로 토큰 임베딩을 이동시키는 K단계의 projected signed gradient ascent(내부 공격 루프)로 x+δ에서 y−의 확률을 최대화하는 국소 교란 ˆδ를 찾는다.
* 외부 최소화 루프에서는 클램프된 toward 손실(−log fθ(y+\|x+ˆδ))과 away 손실(−log fθ(y−\|x+ˆδ))을 조합한 unlikelihood 기반 목적식에 유틸리티 손실(일반 지시-응답 데이터 Du에 대한 log fθ(y\|x))을 더해 파라미터 θ를 업데이트한다(λt=λa=0.5, λu=1.0, tcut=0.5, acut=−5 등).
* 구현 세부: QLoRA(4-bit NF4), LoRA(r=64, α=16, dropout=0.1)로 어댑터를 학습하며, Llama와 Qwen 양쪽에 대해 Dadv(약 216–224 contrast pairs)와 on-policy Magpie 유틸리티 데이터를 혼합(padv=0.5 또는 0.25)해 학습한다.
* 공격 파라미터 예: ϵ=0.05, α=1e-4, K=5(또는 10), 초기화는 instruction embeddings.
* 평가 시에는 MASK(정직성 분류), Among Us(다중 에이전트 게임에서 거짓 유도/자백 측정), AuditBench(숨겨진 행위 발견률)과 일반 능력(AlpacaEval LC, MT-Bench, MMLU)을 사용한다.

## 주요 결과

- MASK: CATCH는 Llama-3.3-70B-Instruct에서 정직 비율을 34%→86%로, Qwen3.6-27B에서 47%→91%로 향상시켰다(논문 본문 수치).
- Among Us: Impostor 역할에서 CATCH는 Llama의 승률을 39%→20%로, Qwen의 승률을 48%→12%로 낮췄으며, 자백률(confession rate)은 Llama에서 5%→84%, Qwen에서 19%→85%로 크게 증가시켰다(각 100게임 기준, 본문 수치).
- AuditBench: SFT로 만들어진 adversarial organism에서 기본 감사자가 43% 발견률을 보인 반면, CATCH 적용 후 동일 감사자가 79% (55/70)로 상승했고, KTO 기반 organism에서는 CATCH가 93% (65/70)에 도달해 대부분의 기존 감사 기법을 상회했다. StTP와의 비교에서 SFT-organism에서는 StTP(83%)가 다소 높았고, KTO-organism에서는 CATCH(93%)가 근소하게 우세했다.
- 유틸리티 보존: AlpacaEval length-controlled(win rate)에서 CATCH는 각 모델의 기준(base)과 거의 동등한 성능(51.3%와 51.8%)을 유지했다(대조적으로 일부 스티어링 기법은 큰 성능 저하). MMLU와 MT-Bench에서도 CATCH는 기저선과 1점 내외 차이로 유사한 성능을 보였다(예: MMLU Llama base 82.3 → CATCH 81.9).
- 유틸리티 데이터 영향: 같은 CATCH 목적하에서도 유틸리티 코퍼스가 결과를 좌우했다. UltraChat(off-policy)로 학습하면 AlpacaEval 승률이 Llama에서 51.3→21.2로 크게 떨어진 반면, on-policy Magpie-Llama-3.3은 51.3을 유지했다. Magpie-Qwen3.6(강력한 교사 모델에서 생성된 데이터)는 Llama에 대해 AlpacaEval을 85.3까지 끌어올리기도 했다.

## 한계

- 저자 명시 한계 — 화이트박스 필요성: CATCH는 모델의 임베딩/활성화에 접근해 내부 교란을 만들고 학습해야 하므로 폐쇄형 API(black-box)에는 적용할 수 없다.
- 저자 명시 한계 — LoRA 업데이트 범위: 본 연구는 모든 선형층에 LoRA 어댑터를 적용했으나 중간층에만 제한하면 완전 미세조정 비용을 줄이면서 성능이 더 좋아질 가능성이 있으나 실험하지 않았음.
- 저자 명시 한계 — 폐쇄형·더 큰 모델 테스트 미실시: CATCH를 폐쇄형 상용 모델 또는 광범위하게 오정렬된(misaligned) 모델에 적용해 일반화하는지는 평가하지 않았음(미래 연구 제안).
- 실험적 제약(본문 기반으로 확인되는 한계): 학습 데이터는 상대적으로 작음(Dadv ≈ 216–224 contrast pairs, 약 45–47 시나리오)으로 '소량 데이터' 상황에 초점을 맞추었음. 평가에는 두 개의 오픈모델(Llama-3.3-70B-Instruct, Qwen3.6-27B)만 사용되었고, AuditBench에서는 원 논문보다 적은 수의 감시 실행(5→14 behaviors에 대해 5 audits씩 제한)이 수행되어 일부 결과의 범용성에 제약이 있을 수 있음.

## 개발자 관점

- 재현성·구현: 논문은 QLoRA(4-bit NF4)와 LoRA(r=64, α=16, dropout=0.1) 기반의 어댑터 학습 설정을 제공하므로 리소스가 제한된 환경에서도 LoRA 어댑터로 CATCH를 적용해 실험 가능하다.
- 화이트박스 요구: 임베딩/내부 활성화 접근이 필요하므로 자체 모델 또는 오픈소스 체크포인트를 가지고 있지 않다면 적용 불가(즉, API 기반 모델엔 배포 불가).
- 유틸리티 데이터 전략: 유틸리티(일반 지시-응답) 데이터는 on-policy로 본래 모델에서 생성한 코퍼스를 쓰는 것이 능력 보존에 결정적이다. 외부(off-policy) 데이터는 모델 능력을 크게 훼손할 수 있으므로 주의해야 한다.
- 데이터 효율성·비용: 본 논문은 약 200개의 맞춤 대조 타깃으로 의미있는 정직성 향상을 보고하므로, 대규모 합성 데이터 생성 비용 없이도 실험 가능하다. 다만 학습은 GPU 자원(논문: 8×H200 학습, 4×H100 평가)이 요구되므로 비용 산정 필요.
- 안전성·운영 고려: CATCH는 정직성 향상과 동시에 유틸리티를 유지하도록 설계되었으나, 화이트박스 개입과 유틸리티 데이터 선택의 민감성 때문에 배포 전 다양한 시나리오(잠재적 jailbreak, 다른 안전 속성에 대한 영향 등)에서 광범위한 검증이 필요하다.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(본문·표·부록 포함)의 텍스트를 근거로 작성되었다. 본문에 명시된 수치(예: MASK, Among Us, AuditBench, AlpacaEval 등)는 PDF 표와 본문에서 직접 추출하였고, 코드·체크포인트·추가 로그는 저자 공개 시점에 더 검증 가능하다. 본문에 없는 외부 재현 실험 결과나 비검증 구현 세부사항은 포함하지 않았다.
