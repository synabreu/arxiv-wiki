# MemTrapBench: Benchmarking Cognitive Traps in LLM Memory Use

- **게시일:** 2026-08-22
- **arXiv:** [2608.20202v1](http://arxiv.org/abs/2608.20202v1) · [PDF](https://arxiv.org/pdf/2608.20202v1)
- **저자:** Mengru Wang, Haozhe Luo, Zhenqian Xu, Zhixiang Cui, Haoming Xu, Qu Yang, Jizhan Fang, Junfeng Fang, Ningyu Zhang
- **분야:** cs.AI, cs.CL, cs.CY, cs.DB, cs.LG
- **선정 점수:** 5.84
- **선정 이유:** 최근성 0.5, 인용 영향 0.0 (인용 0회), 저자 영향 1.6 (최고 h-index 15), AI 주제 적합성 3.0, 개발자 관심 0.5, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-08-22 목록으로 돌아가기](../daily/2026-08-22.html)

<!-- paper-visuals:start -->
## 주요 Figure

> 원문 PDF에서 실제 Figure 캡션과 그림 영역이 함께 확인된 자료만 자동 추출했다.

![Figure 1: Memory is not always what you need. (a) With-](../assets/papers/memtrapbench-benchmarking-cognitive-traps-in-llm-memory-use/figure-1.jpg)

*Figure · 원문 PDF 1쪽 · Figure 1: Memory is not always what you need. (a) With-*

![Figure 2: Overview of our MemTrapBench construction.](../assets/papers/memtrapbench-benchmarking-cognitive-traps-in-llm-memory-use/figure-2.jpg)

*Figure · 원문 PDF 3쪽 · Figure 2: Overview of our MemTrapBench construction.*

![Figure 3: Representative examples from our MemTrapBench.](../assets/papers/memtrapbench-benchmarking-cognitive-traps-in-llm-memory-use/figure-3.jpg)

*Figure · 원문 PDF 4쪽 · Figure 3: Representative examples from our MemTrapBench.*

<!-- paper-visuals:end -->

## 한 문장 요약

메모리 사용이 LLM의 추론과 신념을 왜곡하여 성능을 저하시킬 수 있음을 규명하고, 이를 진단하는 데이터셋 MemTrapBench와 추론시 프롬프트 기반 완화 기법 AdaptiveMem을 제안한다.

## 해결하려는 문제

기존 메모리 벤치마크는 정보 추출·저장·검색의 정확성에 주로 초점을 맞추지만, 검색된 메모리가 현재 과제에서 모델의 추론 전략과 신념을 어떻게 재구성하여 성능을 저하시킬 수 있는지를 평가하지 못한다. 본문은 '메모리 사용 자체가 동일한 쿼리에서 메모리 비사용(no-memory)보다 성능을 낮출 수 있는' 메모리 유도 인지 함정(Memory Traps)을 정의하고, 이를 체계적으로 진단할 수 있는 벤치마크와 완화 방법을 제시한다.

## 핵심 기여

- 메모리 사용이 모델의 추론 전략이나 신념을 왜곡하여 현재 과제 성능을 악화시킬 수 있음을 '메모리 유도 인지 함정(Memory Traps)'으로 공식화하였다.
- Reasoning Fixation(내·횡적 고착)과 Belief Distortion(신념 왜곡) 두 범주, 네 시나리오(Cognitive Bias, Trauma, Task Boundary, Safety)를 담은 진단용 벤치마크 MemTrapBench(총 1,050개 인스턴스)를 구축했다.
- Gemini-3-Flash-Preview 및 Qwen3-30B-A3B-Instruct-2507와 다섯 가지 대표적 메모리 전략(FullText, LightMem, MemOS, SimpleMem, EverMemOS)에서 평가하여, 모든 메모리 전략이 no-memory 대비 성능 저하를 보였음을 실험적으로 증명했다.
- 메모리 제공량(ablation)과 트랩-제거 통제 실험을 통해 성능 저하는 단순히 문맥 길이 때문이 아니라 트랩을 유발하는 메모리의 의미론적 내용 때문임을 확인했다.
- 추론 시 삽입 가능한 프롬프트 기반 스킬 AdaptiveMem을 제안하여, 다양한 메모리 프레임워크에 쉽게 통합 가능하고 MemTrapBench에서 인지 함정을 완화하면서 표준 메모리 벤치마크 성능을 유지하거나 향상시킴을 보였다.

## 접근 방법

* 벤치마크 구성: 연구진이 설계한 시드(seed)를 바탕으로 GPT-5.4를 이용해 다중 턴(18–40턴) 대화를 확장하되, 'Plant the Trap'으로 잘못된 규칙·피드백·선입견을 역사에 심고, 'Bury it in Noise'로 잡음(turn)들을 섞은 뒤, 'Spring the Trap' 단계에서 조건이 바뀐 최종 쿼리를 제시한다.
* 생성 후보는 자동 필터와 전문가 인간 검토의 두 단계 품질 통과를 거쳐 최종 포함된다(최종 데이터셋은 1,050개: Cognitive Bias 350, Task Boundary 350, Safety 200, Trauma 150).
* 정의 및 측정: 메모리 사용에 따른 실패는 s(ŷ_M) < s(ŷ_∅)로 정의하고 응답 품질을 정답성(correctness), 형식(format), 관련성(relevance), 효율성(efficiency) 네 차원으로 채점한다.
* GPT-5.2를 주 심사자로 사용하고 Claude-Sonnet-4.6으로 일관성 확인.
* 평가 설정: 두 모델(Gemini, Qwen)과 다섯 메모리 전략(FullText, LightMem, MemOS, SimpleMem, EverMemOS) 및 no-memory를 비교.
* 추가 실험으로 메모리 길이(25%,50%,75%,100%)와 트랩-제거(no-trap control) 설정을 통해 원인 분석을 수행.
* 완화법(AdaptiveMem): 아키텍처 변경 없이 추론 시 프롬프트로 삽입되는 '스킬' 형태로, 모델에게 검색된 메모리가 현재 과제에 적용 가능한지 점검하고 적용 방식을 조정하도록 지시한다.
* 동일한 메모리 프레임워크에 직접 통합하여 성능 비교(프롬프트·구체적 텍스트는 보조자료에 제시됨).

## 주요 결과

- MemTrapBench 전체(1,050개)에 대해 no-memory 기준에서 Gemini-3-Flash-Preview 평균 85.16%, Qwen3-30B-A3B-Instruct-2507 평균 81.83%를 기록했음(테이블 1).
- 모든 평가한 메모리 전략이 no-memory 대비 성능 하락을 보였음. Gemini에서 최고 성능 메모리(EverMemOS) 평균 71.17%(no-memory 85.16%), Qwen에서는 LightMem 평균 70.13%(no-memory 81.83%)로 보고되었음—저자 기술대로 '가장 강한 방법조차 10%p 이상 하락'을 관찰함.
- 시나리오별 저하가 특히 Cognitive Bias와 Safety에서 두드러짐(예: Gemini Cognitive Bias 메모리 전략 점수 범위 46.66%–65.48%, Safety 56.15%–69.70%).
- 트랩-제거 통제: 같은 Task Boundary 및 Trauma 하위집합에서 'no-trap' 버전(역사에서 트랩 요소 제거)을 제공하면 성능이 크게 회복됨(예: Task Boundary no-trap 평균 94.39% vs 트랩 유도 설정 31.05%; Trauma no-trap 평균 84.33% vs 트랩 유도 69.43%), 이는 실패가 트랩 유도 역사 내용에 의해 발생함을 시사함(테이블 3).
- 메모리 길이 영향: 특정 Task Boundary 서브셋에서 25% 메모리 길이 시 평균 36.03%에서 100%일 때 31.05%로 감소(wo/Mem는 92.29%). 트랩은 적은 양의 역사만으로도 유발되며 메모리 길이가 늘수록 악화되는 경향(테이블 4). 25%→50% 구간에서 추가 하락이 크게 나타남(약 3.4%p).  
    • 예시 수치(테이블4): 25% 평균 36.03%, 50% 32.63%, 75% 31.58%, 100% 31.05%.  
    • 예시 수치(테이블3): Task Boundary wo/Mem 92.29%, no-trap 94.39%, MemTrap 31.05%.   
    • 평가 신뢰성(테이블5): GPT-5.2 judge wo/Mem 평균 92.29±1.25 → Mem 31.05±5.68; Claude-Sonnet-4.6 wo/Mem 95.57±0.53 → Mem 40.07±2.69, 두 심사자가 추세 일치함.)  
    
    (위 수치는 논문 본문 테이블에서 직접 인용한 값임.)

## 한계

- 저자가 직접 언급한 한계: MemTrapBench는 '해로운 메모리 영향'을 진단하는 스트레스 테스트(diagnostic stress test)로 설계되어 메모리의 일반적 유용성을 포괄적으로 평가하려는 목적이 아니라는 점을 명시하고 있다. 또한 데이터 생성에 GPT-5.4가 후보 생성에 사용되었고, 최종 포함·평가는 자동 필터 + 인간 전문가 검토로 결정되었다고 명시되어 있다.
- 본문에서 합리적으로 확인되는 한계:  
    • 평가 대상 모델이 두 계열(Gemini, Qwen)으로 제한되어 있어 다른 모델군(예: 오픈소스 대형 모델들)에 대한 일반화가 불확실하다.  
    • 평가한 메모리 프레임워크는 다섯 개의 대표적 방법에 국한되며, 파라메트릭(내부화) 메모리 방식이나 다른 변형들은 포함되지 않았다.  
    • 데이터셋은 LLM으로 생성된 다중 턴 대화를 인간이 검수한 방식이라 생성 편향 또는 특정 스타일의 트랩이 포함될 가능성이 존재한다(즉, 실제 사용자 대화 분포와 차이가 있을 수 있음).  
    • AdaptiveMem은 프롬프트 기반의 추론-시 기법으로, 프롬프트 설계·튜닝에 민감할 수 있으며 공개된 프롬프트·내부 세부험이 보조자료에만 있어 재현 시 추가 작업이 필요하다.  
    • 평가 및 채점에 고성능 상용 심사자(예: GPT-5.2, Claude-Sonnet-4.6)를 사용하므로 동일한 자동 평가 환경을 재현하려면 접근권·비용 이슈가 발생할 수 있다.

## 개발자 관점

- 메모리 시스템을 실제 서비스에 배포하기 전, 단순한 정확도·검색 평가뿐 아니라 '메모리 유도 인지 함정'을 진단하는 테스트(예: MemTrapBench)를 필수적으로 수행하라. 메모리는 관련하고 사실적이더라도 현재 과제에 해가 될 수 있다.
- 메모리 제공량(문맥 길이)을 줄이는 것만으로는 항상 안전하지 않다. 논문 결과는 적은 분량의 역사(25%)만으로도 트랩이 유발될 수 있음을 보여주므로, 기억된 항목의 '의미론적 적합성(applicability)'을 점검하는 메커니즘이 필요하다.
- 추론 단계에서의 적용 제어(inference-time control)가 실용적이다. AdaptiveMem처럼 아키텍처 변경 없이 삽입 가능한 프롬프트 기반 스킬로도 메모리 유도의 부작용을 상당 부분 완화할 수 있다. 따라서 메모리 스토리지·리트리버를 바꾸기 전에 추론-레벨 안전막을 먼저 적용해보라.
- 트라우마(부정적 피드백)와 같은 사용자 피드백이 모델의 이후 권고를 과도하게 억제할 수 있으므로, 피드백을 저장·반영할 때 '격한 감정적(또는 예외적) 피드백'을 분리·표지화하고 일반화 단계에서 가중치를 낮추는 설계가 필요하다.
- 재현을 위해 필요한 자원: (1) 대상 LLM(평가용), (2) 메모리 프레임워크 구현(FullText, LightMem, MemOS, SimpleMem, EverMemOS 등), (3) MemTrapBench 데이터셋(저자 제공 예정 GitHub), (4) 자동 채점용 고성능 심사자(GPT-5.2, Claude-Sonnet-4.6) 접근권. 이들에 대한 접근·비용을 사전에 고려하라.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(본문 및 표, 그림 설명)을 기반으로 작성되었다. 데이터셋 통계(1,050개, 시나리오별 개수), 테이블(1–5) 및 본문에서 명시된 수치(예: no-memory 및 메모리 전략별 점수, 메모리 길이 ablation, AdaptiveMem 개선치)를 직접 인용하였다. 본문에서 상세 구현 프롬프트와 보조자료에 포함된 내용은 언급되었으나 PDF 본문에 완전한 프롬프트 텍스트가 포함되지 않아 해당 세부 프롬프트 문구는 본 분석에 포함하지 않았다.
