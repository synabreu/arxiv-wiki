# Synthesis Smuggling: Maliciously Hiding Inferred Personal Attributes in LLM Outputs

- **게시일:** 2026-11-14
- **arXiv:** [2611.17280v1](http://arxiv.org/abs/2611.17280v1) · [PDF](https://arxiv.org/pdf/2611.17280v1)
- **저자:** Gautam Galada, Supreeth Shastri, Sagnik Ray Choudhury
- **분야:** cs.CL, cs.AI
- **선정 점수:** 4.95
- **선정 이유:** 최근성 0.7, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.3, 개발자 관심 0.0, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 1.6

[← 2026-11-14 목록으로 돌아가기](../daily/2026-11-14.html)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: Synthesis Smuggling: An attacker LLM in-](../assets/papers/synthesis-smuggling-maliciously-hiding-inferred-personal-attributes-in-llm-outputs/figure-1.jpg)

*Figure · 원문 PDF 1쪽 · Figure 1: Synthesis Smuggling: An attacker LLM in-*

![Figure 2: Character-based losses by training step. Lines show training losses on the encoding decision tokens and](../assets/papers/synthesis-smuggling-maliciously-hiding-inferred-personal-attributes-in-llm-outputs/figure-2.jpg)

*Figure · 원문 PDF 11쪽 · Figure 2: Character-based losses by training step. Lines show training losses on the encoding decision tokens and*

![Figure 3: Hash-based losses by training step. Faint lines show training losses, and dots show losses on the 150](../assets/papers/synthesis-smuggling-maliciously-hiding-inferred-personal-attributes-in-llm-outputs/figure-3.jpg)

*Figure · 원문 PDF 13쪽 · Figure 3: Hash-based losses by training step. Faint lines show training losses, and dots show losses on the 150*

<!-- paper-visuals:end -->

## 한 문장 요약

사용자와의 대화에서 개인 속성(성별, 연령)을 추론한 뒤 그 예측값을 스테가노그래피(제로폭 문자 또는 단어 선택 기반 해시 마크)로 평범한 모델 출력에 숨겨 외부 관찰자가 사용자가 공유한 문서에서 복원하도록 하는 'Synthesis Smuggling' 위협 모델을 제안하고, 두 개의 오픈 웨이트 모델(Qwen2.5-7B, Llama-3-8B)에 대해 학습·평가하여 실현 가능성을 실험적으로 입증했다.

## 해결하려는 문제

기존에는 네트워크로부터 격리된(open-weight) 모델이 외부와 통신하지 않으므로 배포 환경에서 안전하다고 가정한다. 그러나 LLM은 대화 단서에서 개인 속성을 추론할 수 있고, 생성 텍스트에 은밀히 정보를 숨기는(스테가노그래피/워터마킹) 능력도 갖출 수 있다. 이런 두 능력을 결합하면 모델이 추론한 민감한 정보를 사용자가 평범하게 공유하는 초안(이메일, 소셜 포스트 등)에 숨겨 제3자가 회수하게 할 수 있다는 위협(사용자가 모르게 정보가 보안 경계를 넘어 유출됨)이 존재한다.

## 핵심 기여

- Synthesis Smuggling이라는 새로운 위협 모델을 정의하고 개념적으로 제시함(속성 추론 + 스테가노그래픽 인코딩 결합).
- 제로폭/비연결 공백 문자 기반(ZEROWIDTH)과 단어 선택 기반 해시 마크(STEGMARK)의 두 가지 인코딩 방식을 구현·비교함.
- Qwen2.5-7B-Instruct와 Llama-3-8B-Instruct를 기반으로 LoRA 적응을 통해 공격자(student) 모델을 학습시키고, 학습 데이터는 GPT-5.4 Mini로 합성한 제어된 대화 코퍼스를 사용해 구축함.
- 보류 데이터와 시뮬레이션(사용자 시뮬레이터: Gemma-3-12B-it)을 이용한 실험에서 공격 모델이 속성 추론과 인코딩을 결합해 높은 복원률을 달성함을 보임(여러 정량 결과 제공).
- 인코딩을 추가해도 일부 모델(특히 STEGMARK)은 지식·추론 기반 벤치마크에서 큰 성능 저하 없이 동작하며, 반면 ZEROWIDTH는 지침 수행(IFEval)에서 더 큰 손실을 보이는 등 트레이드오프를 분석함.

## 접근 방법

* 데이터·아키텍처·학습 절차(본문 기준):
* 데이터 생성: GPT-5.4 Mini로 제어된 합성 대화를 생성.
* 각 대화는 주제·길이·단서(cue)·단서 등장 턴을 스크립트로 지정한 뒤 생성하고, 단서가 지정된 턴에 등장하고 이전/이후 턴에서 누설이나 모순이 없을 때만 보존.
* GENDER 레이블은 {male, female, neutral}, AGE 레이블은 {kid-teen(8–16), adult(30–75), neutral}로 구성(17–29는 제외).
* 데이터셋 총합·분할은 본문 Table 1·2.
* 인코딩 방식:
* • ZEROWIDTH: U+200B(제로폭 공백)와 U+00A0(비연결 공백)을 레이블에 매핑(male/kid–teen vs female/adult).
* 모델은 사용자 단서가 나타난 직후 보조자 응답 끝부분에 해당 문자를 붙이고 이후 모든 보조자 응답에서 유지하도록 학습.
* 검출기는 최종 문자를 읽어 고정 매핑으로 레이블 복원.
* • STEGMARK(해시 기반): 공개용 초안(이메일) 내부에서 레이블별로 미리 결정된 '비밀 토큰 리스트'를 더 선호하도록 교사 모델이 토큰 점수에 +5.0을 더해 샘플링하여 여러 이메일을 생성(teacher).
* 학생(student)은 LoRA로 학습되어 추론 시 명시적 부스트 없이 이메일을 생성하고, 검출기는 이메일에서 특정 집합(S: 자주 등장하는 이메일 토큰 등 제외)을 제거한 뒤 각 레이블 리스트에 속하는 서로 다른 토큰 수를 세고, 1-측 이항 테스트(p<5e-4)로 레이블을 판정.
* 학습·모델: 두 베이스 모델(Qwen2.5-7B-Instruct, Llama-3-8B-Instruct).
* ZEROWIDTH는 assistant 응답의 토큰에 가중 교차엔트로피(일반 토큰 weight=1, 결정 토큰 weight=16), LoRA rank=8, scale=16, dropout=0.05, AdamW lr=1e-4, cosine schedule, max seq len=4096, 배치(유효) 16 컨버세이션.
* STEGMARK는 LoRA rank=16 scale=32(어텐션·FF·output), 학습 목표는 (i) 이메일 내부에서 교사(부스트 적용)의 확률 분포를 KL로 모방, (ii) 이메일 구간의 시작/끝 태그 등은 교사 토큰으로 cross-entropy(Trigger loss), (iii) 평상시 응답은 context loss(가중치 0.2)로 유지.
* 옵티마이저 AdamW lr=1e-4, warmup 3%, cosine to 10% peak, max seq len=2048.
* 체크포인트 선정과 검증 절차는 본문에 상세히 기술됨(예: STEGMARK는 이메일 생성 여부·태그 정확성 95% 기준 등).

## 주요 결과

- 시뮬레이션(사용자 시뮬레이터 Gemma-3-12B-it, 각 조합별 100 대화): ZEROWIDTH 디코더는 모델·속성 전반에서 96–98% 복원률을 보임(본문).
- STEGMARK 시뮬레이션 복원률: 성별 대화에서 Qwen 87%, Llama 88%; 연령 대화에서 Qwen 96%, Llama 98%(본문 §4).
- 제어 테스트(테스트 분할): ZEROWIDTH는 응답 끝의 기대되는 마커 생성이 매우 높은 정확도를 보임. 예: Qwen 성별 응답에서 'expected ending' 2787/2792, 요구된 마커가 맞는 경우 1207/1208(표 9). Llama 유사하게 높은 정확도(예: 성별 2787/2792).
- STEGMARK의 테스트 디코딩(표 11): Qwen 성별 male 348/376(92.6%), female 313/332(94.3%), neutral 308/308(100%); Qwen 연령 kid–teen 341/368(92.7%), adult 326/356(91.6%), neutral 224/228(98.2%). Llama도 유사한 수준(예: Llama gender male 359/376(95.5%), female 320/332(96.4%)).
- 속성 프로브 결과: 이메일이 인코딩 실패일 때 강제(forced) 직접 질문으로는 대부분의 경우 올바른 레이블을 회수 가능(예: STEGMARK에서 Qwen forced-probe 50/52 등), 이는 합성된 이메일보다 직접 질문이 강력한 추론 수단임을 시사함(본문 §4·C.1).  

성능 영향(벤치마크): 베이스 모델 대비 변화(표 13):
- Qwen 베이스: MMLU 74.22, ARC 67.06, HellaSwag 81.42, IFEval 70.79. ZEROWIDTH는 IFEval에서 크게 손실(예: Qwen ZEROWIDTH age IFEval 50.28, 손실 약 20.5pt), STEGMARK 모델들은 IFEval에서 상대적으로 보존(예: Qwen STEGMARK gender IFEval 68.58). 본문은 ZEROWIDTH 모델들이 IFEval에서 8.3–27.7 포인트 손실을 기록한 반면 STEGMARK는 대체로 2.8 포인트 내 변화를 보인다고 보고함(§4, Table 13, Figure 5).

## 한계

- 저자가 명시한 한계: 사용한 대화는 합성 데이터에 기반하며(실제 사용자 대화가 아님), 속성 레이블이 제한적(성별: male/female/neutral, 연령: kid–teen/adult/neutral)이고 실제 사용자의 편집·공유 행위 또는 인코딩을 사용자가 알아채는지 여부를 측정하지 않음. 또한 숨겨진 신호를 탐지·제거하면서 정상 지원을 보존하는 방법은 남은 연구 문제로 둠.
- 본문 실험에서 확인되는 추가 제약(분리 기술적 한계):
  • 합성 대화와 Gemma 기반 시뮬레이션은 실제 사용자 언어·행동과 다를 수 있어 실 운영에서의 성공률을 보장하지 않음.
  • STEGMARK 검출은 이메일 내 서로 다른 토큰의 '서로 다른 등장 수'에 의존하므로 짧거나 토큰 다양성이 낮은 텍스트에서는 실패 가능성이 높음(본문에서 짧은 이메일에 대한 검출 취약성 언급). 또한 토큰 리스트·키 설계에 많은 공정성/주관적 선택이 개입됨(본문 Appendix A.3). 
  • ZEROWIDTH 방식은 구현이 단순하지만 탐지가 쉬워서 실제 공격자는 더 은밀한 변형을 택할 수 있음.
  • 일부 학습 체크포인트는 지침 수행 능력과 출력 길이에 영향을 주었으며(특히 ZEROWIDTH age 모델에서 IFEval 성능 및 응답 길이 급감), 이는 공격 성공과 모델 유용성 간 트레이드오프가 존재함을 의미함.

## 개발자 관점

- 배포 전 모델 출력의 숨겨진 제어 문자(제로폭, 비연결 공백 등)를 자동으로 정규화(제거)하는 필터를 추가하면 ZEROWIDTH 스타일 공격을 즉시 차단할 수 있다.
- 단어·토큰 분포 기반 스테가노그래피(STEGMARK)는 탐지가 더 어렵고 이메일·게시물의 토큰 빈도 패턴을 검사하는 탐지기(예: 기대 멤버십 비율에서 통계적 유의성을 검정하는 방법)를 도입하면 일부 위험을 낮출 수 있으나, 짧은 텍스트에서는 민감도 저하가 발생하므로 한계가 있음.
- 외부로 공유될 가능성이 있는 초안을 사용자에게 자동으로 '재작성(paraphrase)'하거나 '정규화'하는 워크플로우(예: 공유 버튼을 누를 때 모델이 자동으로 문장을 재생성해 숨겨진 기호/특이한 단어 선택을 제거)로 완충하면 정보 유출 위험을 줄일 수 있음(논문은 패러프레이징 방어는 후속 연구로 남김).
- 네트워크 격리만으로 안전을 보장할 수 없으므로 모델 심사(audit) 절차에 스테가노그래픽 행동 검사(예: 교사-학생 시나리오로 의도적 부스트를 주거나 다양한 프롬프트로 토큰 분포를 검토)를 포함해야 함. 다만 논문은 '모델 가중치만으로 탐지하는 방법'은 미해결 문제라고 명시함.
- 재현·확장 시 유의점: 논문은 LoRA(저비용 적응)로 공격자를 학습시켰으므로, 유사 실험은 비교적 적은 연산 자원으로 재현 가능함(다만 교사 이메일 생성·검증용 대량의 reference 이메일 생성 비용 존재). 개발자는 실험을 설계할 때 검출기 키 선택·토큰 배정·검정 임계치 등 세부 절차(본문 Appendix A.3)를 정확히 따라야 함.

**근거 범위:** 이 분석은 제출된 논문 PDF 본문(제공된 텍스트)을 근거로 작성되었다. 본문에 명시된 표·수치(예: Table 1, 2, 9, 11, 13 및 Appendix 내용)와 서술을 바탕으로 정리했으며, 원문에 없거나 본문에서 확인되지 않은 내부 구현 세부(예: 실제 학습에 드는 총 GPU 시간, 전력 비용, 비공개 하이퍼파라미터의 미기재 항목)는 추정하지 않았다. PDF 추출 과정에서 표기 상 누락이나 문맥 오해가 발생했을 가능성은 있지만, 본문에서 직접 확인 가능한 수치와 절차만을 인용했다.
