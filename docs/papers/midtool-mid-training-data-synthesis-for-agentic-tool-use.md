# MidTool: Mid-training Data Synthesis for Agentic Tool Use

- **게시일:** 2026-08-21
- **arXiv:** [2608.20314v1](http://arxiv.org/abs/2608.20314v1) · [PDF](https://arxiv.org/pdf/2608.20314v1)
- **저자:** Fengqing Jiang, Yite Wang, Boyi Liu, Zhaoyang Wang, Canwen Xu, Zhewei Yao, Radha Poovendran, Yuxiong He
- **분야:** cs.AI
- **선정 점수:** 6.39
- **선정 이유:** 최근성 0.8, 인용 영향 0.0 (인용 0회), 저자 영향 1.6 (최고 h-index 13), AI 주제 적합성 2.9, 개발자 관심 0.8, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-08-21 목록으로 돌아가기](../daily/2026-08-21.html)

## 한 문장 요약

일반적 도구 사용(agentic tool use)을 목표로 웹/PDF/코드/구조화된 툴 아티팩트를 합성해 20.3B-token 규모의 mid-training 코퍼스(MidTool-Mix)를 만들고, 이를 Qwen3-4B/8B 베이스 모델에 적용해 후속 SFT 및 RL 성능을 안정적으로 개선함으로써 '도구 사용은 전적으로 post-training에 맡길 것이 아니라 mid-training으로도 형성할 수 있다'를 입증한다.

## 해결하려는 문제

기존에는 LLM의 도구 사용 능력 개선을 주로 post-training(예: SFT, RL)으로 해결해 왔으나, 도구 인식(tool affordance), 스키마 기반 인자 추출, 다중-툴 워크플로우 구성, 불완전 정보에서의 복구 등 도구 사용에 필요한 기저 지식이 문서·코드·API 등 흩어진 형태로 존재해 좁은 후속 데이터만으로 습득시키기 어렵다. 연구 질문은 '일반적 도구 사용 능력을 전용 mid-training으로 조형하면 downstream SFT/RL 성능이 개선되는가'다.

## 핵심 기여

- 도구 사용(agentic tool use)을 목표로 설계된 공개적 중간학습 파이프라인 MidTool을 제안하고, web/PDF/code/structured tool 소스와 두 축(문맥 기반 보강, 네이티브 실행 궤적 합성)의 합성 방법을 제시함.
- MidTool 파이프라인으로 만든 MidTool-Mix(20.3B tokens, 11.22M 샘플)를 공개하고, 웹 42% / 코드 26% / PDF 23% / 네이티브(실행가능) 궤적 9%의 혼합을 구성함.
- Qwen3-4B-Base와 Qwen3-8B-Base에 MidTool-Mix로 mid-training을 수행한 뒤 동일한 SFT(TOUCAN 100K 샘플) 및 선택적 RL(Agent World Model 환경, 526개 합성 환경) 파이프라인을 적용하여 BFCLv3, 𝜏2-Bench, MCP-Universe에서 일관된 성능 향상을 보였음을 실증함.
- 데이터 설계 관점에서 context-grounded augmentation(문서→QA/궤적)과 native agentic trajectory(실제 API/MCP 스킬 기반 실행 궤적)가 상보적으로 기여함을 세부 ablation으로 분석함.
- 일반 도구 사용(mid-training)이 web-search와 같이 깊은 탐색을 요구하는 탐사형 행동과는 구분되는 능력 경계를 드러내어, 향후 전문화된 mid-training 필요성을 제시함.

## 접근 방법

* 중요 구성 요소와 절차는 다음과 같다.
* 원천(4가지): FineWeb 기반 웹 문서(여러 덤프, 2020-2025), FinePDFs의 영어 PDF, GitHub 코드 저장소(두 슬라이스: 에이전트/MCP 관련 + 고품질 공개 저장소), 그리고 REST API·MCP 스킬 같은 구조화된 툴 아티팩트.
* 전처리: 코드에 대해 확장자·내용 기반 필터링(StarCoder 기준 유사), SHA-256/MinHash LSH 중복 제거, 문서(웹/PDF)는 키워드/URL 사전검사→fastText 분류(LLM 라벨로 학습)→품질 필터→MinHash LSH로 필터링.
* 코드 슬라이스는 벤치마크 저장소 블랙리스트로 유출 차단.
* 합성(두 브랜치):
* 1) Context-grounded trajectory augmentation: 문서에서 툴 어포던스/스키마 증거를 추출해 규칙 기반 플래너로 QA/단계적 궤적을 생성(생성 모델: Qwen3-235B-A22B-Instruct-2507 사용).
* 문서 품질에 따라 생성 예산을 제어하고 파싱·의미적 품질검사를 거친 샘플만 포함.
* 2) Native agentic trajectory synthesis: 구조화된 툴(API/MCP)에서 툴 인벤토리 구축, GPT-5 계열로 품질·실행 가능성 평가, 툴 스키마 정규화와 카테고리별 생성(생성 모델: GPT-5, GPT-5.1, GPT-5.2 혼합).
* 생성물은 턴 순서·스키마 정합성·필수 인자·툴 응답 일관성으로 엄격 검증하고 실패시 재시도.
* 에이전틱 롤아웃(Agent World Model)과 Nemotron Agentic 데이터의 필터링된 궤적도 혼입.
* 혼합: 최종 MidTool-Mix(20.3B tokens, 11.22M 샘플)를 웹/코드/PDF 소스(각각 소스 토큰과 그에 대한 context-grounded augmentation 토큰으로 표기)와 네이티브 에이전틱 궤적로 구성.
* 학습 파이프라인: Qwen3-4B/8B 베이스 모델에 대해 MidTool-Mix로 1 epoch mid-training(하이퍼파라미터: max seq len 8192, LR 3e-5, AdamW 등, 배치 4M tokens 전역) 수행 후 SFT(TOUCAN 100K 예제, max seq len 32768, LR 2e-5) 및 선택적 RL(GRPO, 526 합성 환경, RL 하이퍼파라미터 명시) 진행.
* 하드웨어: mid-training·SFT는 32 H200 GPU, RL은 8 B200 GPU.

## 주요 결과

- MidTool-Mix 구성: 총 20.3B tokens, 11.22M 샘플; 소스별 비중(web 42%, code 26%, PDF 23%, native agentic 9%).
- 주요 벤치마크(중요 수치들은 본문 Table 6의 ablation(4B SFT 설정 기준)에서 발췌): MidTool-Mix 적용(Qwen3-4B-Base + MidTool-Mix + SFT)으로 BFCLv3에서 Non-live(single-turn?) 66.38% (+6.4), Live 57.74% (+14.0), Multi-turn 26.63% (+11.1), Overall 50.25% (+10.5) — 모두 No mid-training(기준값 Overall 39.73%) 대비 개선. 𝜏2-Bench 전체 Pass@1 12.23% (+3.7) / Pass@4 28.06% (+7.6). MCP-Universe Overall score 18.66 (+5.5)와 Pass 5.03% (+3.4).
- SFT 후 RL을 추가하면 대체로 성능이 더 좋아짐. 예컨대 BFCLv3에서 Qwen3-4B-Base + MidTool-Mix + SFT + RL가 No mid-training + SFT + RL 대비 다중턴 성능·전체 성능에서 추가 개선을 보임(본문 Table 3, Table 5에 RL 후 개선 사례 다수 기재).
- Ablation: 원시 처리된 소스만으로도(합성 궤적 없이) 일부 이득이 있으나, context-grounded augmentation과 native agentic trajectory 두 브랜치를 모두 포함한 MidTool-Mix가 모든 측정치에서 일관된 개선을 보이며, 두 브랜치는 역할이 상보적임(예: native 궤적은 BFCL의 정밀한 함수 호출 개선에 크게 기여, context-grounded는 𝜏2-Bench·MCP 전이 성능에 특히 기여).
- 학습 역학: MidTool-Mix로 미드트레이닝한 초기화는 SFT에서 더 낮은 초기 loss, 빠른 초반 수렴, RL에서도 초기 보상 및 빠른 적응을 제공함(본문 C.1, C.2의 학습 곡선 분석).

## 한계

- 저자가 명시한 한계(본문 D):
  - mid-training과 post-training(특히 SFT/RL)의 공동 설계(co-design)가 아직 미구성되어 있으며, 본 실험은 downstream 레시피를 고정해 mid-training 효과만 고립시켜 평가함. 따라서 mid-와 post-training의 상호작용·대체성은 미해결.
  - 동일 예산(matched token/computation)으로 혼합 디자인을 완전히 탐색하지 못함(예: native-trajectory-only를 전체 예산으로 확장한 경우 등은 미래 과제).
  - 합성 과정에서 강력한 교사 모델(GPT-5 계열 등)에 의존함—교사 의존도를 줄이는 방법은 향후 연구 영역.
  - MidTool-Mix는 일반적 도구 사용에는 이득을 주지만, 'deep-search'처럼 반복적 증거수집·긴 탐색을 요구하는 탐사형 행동에는 유의미한 개선을 제공하지 못함(예: MCP-Universe의 web-search subset은 0.00로 남음), 이는 능력 경계(boundary)를 드러냄.
- 본문 실험 범위에서 확인되는 제약(본문에서 합리적으로 확인 가능한 한계):
  - 평가 모델 규모는 4B/8B로 제한됨; 대형(frontier) 모델에 대한 동일한 효과의 확장성은 본문에서 직접 입증되지 않음.
  - 일부 합성 궤적은 폐쇄형·비공개 교사 모델로 생성되었고(본문에 GPT-5 시리즈 사용 명시), 이는 재현성·민감도에 영향 가능.
  - MidTool-Mix 내 네이티브 궤적 생성·검증은 실행 가능한 환경을 요구하므로 동일한 데이터 파이프라인을 재현하려면 상당한 시스템(툴 서버, 롤아웃 환경) 구현 비용이 필요함.

## 개발자 관점

- 데이터 파이프라인: 웹/PDF/코드/툴 아티팩트를 조합하고 문서별 품질 점수를 기반으로 생성 예산을 제어하는 설계가 중요하다. fastText(LLM 라벨로 학습) → 품질 필터 → MinHash LSH 중복 제거 흐름을 재현해야 함.
- 생성 교사 의존성: 네이티브 궤적과 문맥 기반 보강을 위해 대형 생성 모델(GPT-5 계열, Qwen3-235B 등)을 교사로 사용하였으므로, 공개 재현을 위해선 동일하거나 대체 가능한 강력한 교사 모델이 필요하다. 교사 의존도를 낮추려면 향후 오픈 모델로의 대체·점진적 자가생성이 요구됨.
- 검증 파이프라인: 생성된 궤적은 턴 순서·스키마 정합성·필수 인자·툴 응답 일관성으로 엄격 검증해야 하며, 실패 시 재시도/폐기 로직을 구현해야 데이터 품질을 확보할 수 있음.
- 컴퓨트·비용: 본 논문 실험은 mid-training·SFT에 32 H200 GPU, RL에 8 B200 GPU를 사용했고 mid-training 배치 목표는 전역 4M tokens(데이터 패킹 포함) 등 대규모 자원이 필요함. 실무 적용 시 비용/하드웨어 고려 필요.
- 안전·데이터 유출 방지: 코드 슬라이스 수집시 벤치마크 블랙리스트를 파이프라인 단계에서 적용하고, 후속으로 DeCon 같은 표면 중복 감사를 수행해 벤치마크 유출 위험을 낮춘 점은 실무에서 반드시 모방할 것(논문은 웹/PDF/SFT 합성까지 검사했고 적발된 후보는 조사가 모두 false positive였음).

**근거 범위:** 이 분석은 논문 PDF 본문(메인 텍스트 및 부록)에 기재된 내용만을 근거로 작성되었다. 데이터 구성(20.3B tokens, 11.22M 샘플, 웹 42%/코드 26%/PDF 23%/네이티브 9%), 실험 설정(모델 이름·하드웨어·SFT 100K TOUCAN 사용·RL 환경 수 526), ablation 및 성능 수치(본문 Table 3–6 및 부록 수치)를 본문에서 직접 인용하였다. 복잡한 표의 일부 열 해석(예: BFCL 세부 하위 항목의 정확한 컬럼 레이블)은 PDF 표 서식 때문에 모호한 부분이 있어 가능한 한 본문에서 명시된 요약 및 Table 6의 ablation 델타를 중심으로 수치화하였다. 표나 부록의 세부적인 숫자 열 배치로 인해 해석상 불확실한 소수의 세부항은 본문에 명시된 정량적 요약(증가 폭·주요 수치)을 우선 사용했다.
