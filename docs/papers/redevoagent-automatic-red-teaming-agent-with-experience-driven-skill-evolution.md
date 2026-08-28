# RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution

- **게시일:** 2026-08-28
- **arXiv:** [2608.27439v1](http://arxiv.org/abs/2608.27439v1) · [PDF](https://arxiv.org/pdf/2608.27439v1)
- **저자:** Junjie Zhang, Hui Liu, Kecheng Chen, Xianbo Mo, Changsheng Chen, Haoliang Li
- **분야:** cs.CR, cs.AI
- **선정 점수:** 5.03
- **선정 이유:** 최근성 1.2, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 3.0, 개발자 관심 0.6, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-08-28 목록으로 돌아가기](../daily/2026-08-28.html)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: RedEvoAgent overview. Given a jailbreak prompt, the attacker agent uses the current](../assets/papers/redevoagent-automatic-red-teaming-agent-with-experience-driven-skill-evolution/figure-1.jpg)

*Figure · 원문 PDF 2쪽 · Figure 1: RedEvoAgent overview. Given a jailbreak prompt, the attacker agent uses the current*

![Figure 2: Skill evolution from attack experience. (a) On the training split, RedEvoAgent collects](../assets/papers/redevoagent-automatic-red-teaming-agent-with-experience-driven-skill-evolution/figure-2.jpg)

*Figure · 원문 PDF 5쪽 · Figure 2: Skill evolution from attack experience. (a) On the training split, RedEvoAgent collects*

![Figure 3: Validation-ratchet evolution. The x-axis is the maximum number of ratchet rounds R;](../assets/papers/redevoagent-automatic-red-teaming-agent-with-experience-driven-skill-evolution/figure-3.jpg)

*Figure · 원문 PDF 9쪽 · Figure 3: Validation-ratchet evolution. The x-axis is the maximum number of ratchet rounds R;*

<!-- paper-visuals:end -->

## 한 문장 요약

제품 수준의 블랙박스 에이전트에서의 탈옥(jailbreak) 취약점을 자동으로 탐지하기 위해, 교차 사례의 공격 궤적을 간결한 자연어 '공격 스킬'로 증류하고 도구 효능 프로파일·결정도구(Deciding-Tool) 귀속·검증 래칫으로 스킬을 점진적으로 진화시키는 RedEvoAgent를 제안한다.

## 해결하려는 문제

LLM 기반 에이전트가 제품 수준 실행 허니스를 통해 파일 수정, 외부 API 호출 등 도구 사용과 영구 상태 변경을 할 수 있게 되면서 탈옥 공격의 위험이 확대되었다. 기존 자동 레드티밍은 고정된 공격 방식이나 궤적 기반 검색(retrieval)에 의존하는데, 궤적 검색은 유사도 편향으로 인해 오해를 낳거나 어떤 도구 선택이 실제 성공에 기여했는지 불명확하여 잘못된 경험을 재사용하고 최적화 불안정을 초래한다. 또한 전체 궤적을 맥락으로 넣으면 컨텍스트 오버헤드와 해석성 저하가 발생한다. 본 논문은 이러한 한계를 해결하여 재사용 가능한 고수준의 공격 전략(스킬)을 자동으로 학습·진화시키는 방법론을 제시한다.

## 핵심 기여

- 교차 사례 공격 경험을 압축한 사람 읽기 가능한 자연어 공격 스킬을 학습하고 진화시키는 RedEvoAgent 구조 제안(블랙박스 대상에 적용 가능).
- 도구별 독립 효능 측정(tool-effectiveness profile)과 Deciding-Tool Attribution(성공 직전의 도구에 성공 귀속)을 도입해 잘못된 공헌(credit) 할당과 자기강화적 편향을 완화.
- 검증(validation) 래칫 메커니즘을 도입해 후보 스킬 업데이트를 독립 검증집합에서 성능이 개선될 때만 수용함으로써 노이즈성 업데이트를 억제.
- 다양한 벤치마크(Agent Security Bench, AgentHarm), 여러 타깃 모델(MiniMax-M2.5, DeepSeek-V4-Flash, Qwen3.5-35B) 및 실행 허니스(Claude Code, Codex)에서 기존 고정·에이전트형 베이스라인을 능가함을 실험적으로 입증.
- 진화된 스킬이 공격자 모델 및 실행 허니스 간에 제로샷 전이가 가능하며, 스킬 사용으로 공격 도구 호출 효율(평균 도구 호출 수 감소)이 개선됨을 보임.

## 접근 방법

* 문헌과 본문 절차에 따라 RedEvoAgent는 다음 구성요소와 흐름을 가진다.
* 문제 설정: 타깃 에이전트 Mtar=(mtar, htar)과 공격자 Matt(s)=(matt, hatt(s,T))를 정의하고, 공격 툴박스 T와 공격 스킬 s(마크다운 문서)를 사용한다.
* 공격 예산 B는 attacker-agent 루프에서 허용되는 최대 턴 수이다.
* 각 턴에서 공격자는 QUERYTARGET 또는 툴 호출 tk ∈ T 중 행동을 선택한다.
* 툴박스(T): 논문에서는 7개 도구를 통합—GCG(gradient-based), AutoDAN(evolutionary), AmpleGCG(generator suffix), Template(템플릿 래핑), FlipAttack(문자 플립 변형), RolePlay(역할놀이 재작성), Prompt Substitution(보조 LLM으로 실패한 프롬프트 재표현).
* 스킬 표현: 스킬 s는 공격자 시스템 프롬프트에 삽입되는 마크다운 문서로, 도구 우선순위와 오케스트레이션 규칙(예: 직접 요청 → 거부 시 FlipAttack → 실패 시 강한 도구로 전환 등)을 담는다.
* 경험 수집: (1) Tool-Efficacy Profile e: 각 도구를 Dtr(학습집합)에서 고립 평가하여 et = (1/\|Dtr\|) Σ_x r_x(t)로 측정.
* (2) Trajectory Collection Γ(s): 현재 스킬로 Dtr에 대해 공격 롤아웃을 실행하여 각 케이스의 전체 궤적(도구 호출, QUERYTARGET·응답, 점수 등)을 수집.
* Deciding-Tool Attribution: 성공한 궤적의 성공을 해당 성공을 낳은 첫 번째 성공적 QUERYTARGET 직전에 호출된 도구에 귀속시켜 도구 공동출현으로 인한 오해를 방지.
* 스킬 합성(증류): Distiller(LLM)이 현재 수용된 스킬 s*, 도구 효능 프로파일 e, 수집된 궤적 Γ(s*), 그리고 이전에 탈락한 후보들의 기록(거부 컨텍스트 C)을 읽고 미니배치별로 성공·실패 궤적을 비교·분석하여 제한된 변화 범위 내에서 후보 스킬 ŝ_i를 생성.
* 검증 래칫: 후보 ŝ_i를 독립 검증집합 Dva에서 평가(J_Dva(ŝ_i)).
* 만약 J_Dva(ŝ_i) > J_Dva(s* )이면 ŝ_i를 수용하고 Dtr에서 새 궤적을 다시 수집하며 거부 컨텍스트를 초기화, 아니면 ŝ_i를 거부 목록에 추가하고 기존 s* 유지.
* 이 과정을 R 라운드 반복(알고리즘1).
* 구현상 세부: 실험에서 공격자 모델은 GPT-4o mini, 예산 B=20, 라운드 R=4, SkillOpt 기본 미니배치 8, 편집 상한 L=6, 시드=42.
* 후보 선택 기준은 ASB에서는 ASR, AgentHarm에서는 HarmScore.

## 주요 결과

- 데이터셋·분할: ASB(Agent Security Bench) 400 케이스, AgentHarm 208 케이스(52 base behaviours × 4 variants). 학습/검증/테스트 분할은 ASB: 80/40/280, AgentHarm: 40/20/148으로 설정.
- 타깃 모델·허니스: MiniMax-M2.5, DeepSeek-V4-Flash, Qwen3.5-35B을 각각 Claude Code 또는 Codex 실행 허니스와 페어링해 평가.
- 대표적 정량 결과: AgentHarm에서 DeepSeek-V4-Flash / Claude Code 조합에서 RedEvoAgent는 74.3% HarmScore를 달성해 FlipAttack(67.9%) 및 RedCodeAgent를 능가함(표1, 본문). ASB에서 MiniMax-M2.5 / Codex 조합에서는 RedEvoAgent가 92.8% ASR을 기록해 FlipAttack(81.1%) 보다 크게 개선함.
- 스킬 기여(표2): 예를 들어 ASB / Claude / MiniMax-M2.5에서 No Skill은 77.5% ASR(평균 도구 호출 3.0), Human Skill은 78.3%/3.2, RedEvoAgent는 93.2% ASR에 평균 도구 호출 1.8로 도구 호출 효율을 개선함.
- 경험 구성 요소 기여(표3): 도구 효능 프로파일 제거 시 ASR이 93.2%→76.9%로 최대 악영향(−16.3) 발생. 궤적 수집 제거 시 85.0%(−8.2), Deciding-Tool Attribution 제거 시 87.5%(−5.7)로 성능 저하를 보여 제안된 구성요소들이 실험적으로 기여함을 확인함(본문 표3).

## 한계

- 저자가 명시한 한계: 성능은 툴박스의 강도와 다양성에 의존하며(즉, 집합 T에 포함된 개별 도구들의 능력에 따라 성과가 제한됨), 검증 래칫은 검증집합의 대표성에 따라 과적합될 수 있음(예: 논문에서 AgentHarm/MiniMax의 경우 R4 후보가 검증점수를 올렸으나 테스트에서는 성능 저하를 보였음).
- 본문에서 확인되는 제약(실험적 범위로부터 합리적으로 도출): 실험은 주로 GPT-4o mini를 공격자 모델로 사용하고 특정 상용/연구용 타깃 모델·허니스 집합으로 제한되어 있어 다른 공격자 모델·툴 조합·대상 환경에서의 일반화는 추가 검증이 필요함.
- 추가적 실무 제약(본문에 명시적 수치로는 없음): 스킬 진화에는 도구의 고립 평가, 다회성 후보 검증, 여러 라운드의 롤아웃 실행이 요구되어 계산·API 비용(특히 상용 LLM 호출 비용)과 시간이 다소 높을 수 있음.

## 개발자 관점

- 구현·재현: 논문은 공격자 모델(GPT-4o mini), 예산 B=20, 진화 라운드 R=4, 미니배치 크기 8, 편집 캡 L=6, 시드=42 등 핵심 하이퍼파라미터를 명시하므로 동일한 환경(또는 유사 모델)에서 재현성이 높음. 단, 타깃 모델·허니스는 저자들이 재현한 인프라를 활용해야 함(저자가 재현된 허니스 제공을 언급).
- 시스템 구성: 공격 스킬을 시스템 프롬프트의 마크다운 문서로 유지하고, 공격자 에이전트는 ReAct 스타일 루프에서 QUERYTARGET 또는 툴 호출을 선택하도록 구현해야 함. 툴은 독립적으로 호출 가능한 단일턴 변환기여야 함(논문의 7개 도구와 같은 인터페이스 권장).
- 검증·안정화: Deciding-Tool Attribution을 구현해 성공 귀속을 명확히 하고, 후보 스킬은 검증집합에서 엄격히 개선될 때만 수용하는 검증 래칫을 도입해 자기강화적 편향과 과적합을 줄일 것.
- 비용·효율: 진화된 스킬은 평균 도구 호출 수를 줄여 효율을 개선하지만, 스킬 진화 자체(도구 고립평가 + 다회 롤아웃)는 비용이 든다. 실험에서 진화 후 평균 도구 호출이 1.x–2.x 수준으로 감소한 사례가 보고되어 실제 배포 시 공격 비용 절감 가능성을 보여줌.
- 안전·윤리: 본 시스템은 악용 가능성이 높은 자동화된 레드팀 도구이므로 내부 통제(허가된 평가 환경, 로깅, 접근 제어)와 윤리적 검토·거버넌스가 필수적임. 공개 배포 시 오용 방지를 위한 제한 조치 필요(예: 인증된 연구자에게만 공개 등).

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(모든 페이지)에서 직접 추출한 정보에 기반한다. 본문에 명시된 수치(예: ASR/HarmScore, 실험 설정: 공격자 모델 GPT-4o mini, B=20, R=4, 미니배치=8, L=6, seed=42)와 표·그림의 결과만을 사용했다. 본문에 상세히 서술되지 않은 내부 구현의 미세한 파라미터나 추가 실험(예: 비용 산출의 세부 내역, 일부 내부 로그 포맷 등)은 PDF에서 확인되지 않아 생성하지 않았음을 밝힌다.
