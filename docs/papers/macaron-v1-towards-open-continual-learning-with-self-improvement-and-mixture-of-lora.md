# Macaron-V1: Towards Open Continual Learning with Self-Improvement and Mixture-of-LoRA

- **게시일:** 2026-08-12
- **arXiv:** [2608.09819v1](http://arxiv.org/abs/2608.09819v1) · [PDF](https://arxiv.org/pdf/2608.09819v1)
- **저자:** Mind Lab, :, Vin Bo, Asher Cai, Jingwei Cao, Song Cao, Vic Cao, Amelia Chen, Andrew Chen, Kaijie Chen, Cleon Cheng, Steven Chiang, Kaixuan Fan, Hera Feng, Huan Feng, Arthur Fu, Jun Gao, Pyke Han, Nolan Ho, Ori Hong, Hailee Hou, Piers Hua, Charles Huang, Miles Jiang, Nora Jiang, Yuyi Jiang, Qiuyu Jin, Fancy Kong, Kuss Koo, Jaron Lee, Andrew Lei, Alexy Li, Dawn Li, Lucian Li, Ray Li, Ricardo Li, Smith Li, Theo Li, Allen Lin, Elliot Lin, Fan Lin, Chen Ling, Kairus Liu, Kieran Liu, Logan Liu, Neo Liu, Xiang Liu, Yuxin Lu, Maeve Luo, Pony Ma, Verity Niu, Cole Qiao, Guian Qiu, Vince Qu, Sentry, Niko Song, Vincent Wang, Bo Wu, Rio Yang, Evelyn Ye, Fiona Ye, Ina Ye, Regis Ye, Josh Ying, Atlas Zeng, Danney Zeng, Salmon Zhan, Anya Zhang, Di Zhang, Mia Zhang, Sueky Zhang, Wei Zhao, Ada Zhou, Adrian Zhou, Yuhua Zhou, Juno Zhu, Murphy Zhuang
- **분야:** cs.LG, cs.CL
- **선정 점수:** 6.62
- **선정 이유:** 최근성 0.8, 인용 영향 0.0 (인용 0회), 저자 영향 1.8 (최고 h-index 25), AI 주제 적합성 2.2, 개발자 관심 0.6, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 1.0

[← 2026-08-12 목록으로 돌아가기](../daily/2026-08-12.html)

## 한 문장 요약

Macaron-V1은 '고정된 대형 베이스 모델 + turn-level로 선택되는 LoRA 전문화기'(Mixture-of-LoRA) 아키텍처와 모델-하니스 공동설계 기반의 재귀적 자기개선(Recursive Self-Improvement, RSI) 루프를 결합해 배포 후 경험으로 계속 학습하는 열린 연속학습(continual learning) 시스템을 제안한다.

## 해결하려는 문제

중앙집중식(post-training) 재학습 방식은 배포 환경, 도구, 사용자, 상호작용 상태가 계속 변하는 현실 세계에서 발생하는 새로운 지식·도메인·상호작용을 반영하지 못해 정적 최적화에 머무른다. 기존 통합 파라미터 학습은 이종 과제 간 교란(cross-task interference)을 일으키고, 배포 경험을 체계적으로 후속 모델·하니스 수정으로 전환하는 메커니즘이 부족하다. 논문은 배포 경험을 이용해 안전하게 반복 개정할 수 있고, 서로 다른 전문화기를 조합해 협업하는 시스템 설계 문제를 다룬다.

## 핵심 기여

- Mixture-of-LoRA(MoL) 아키텍처: 고정된 대형 베이스를 유지하고 복수의 LoRA 전문화기(어댑터)를 등록·조합하며, 각 사용자 턴에서 L0(채팅 어댑터)가 constrained decode로 한 개 어댑터 라벨을 출력해 Proxy가 해당 어댑터로 라우팅하는 per-turn 구성 및 서빙 허브를 제시하고 공개했다.
- Model–Harness 공동설계와 재귀적 자기개선(RSI) 알고리즘: UI4A(GenUI 하니스), REPL 기반 에이전트 하니스, Harness Context Protocol(HCP)으로 하니스·도구·세션을 버전관리하고, MindForge 에이전트 RL 프레임워크로 task discovery·trajectory expansion·연결된 모델/설정 업데이트 루프를 제안했다(실험에서는 Expansion 단계 고정모델 하니스 탐색을 격리 평가).
- 인프라스트럭처: adapter 리비전·카탈로그·모델 거주를 다루는 MinT 포스트트레이닝 플랫폼, 고토큰 장문 실행을 지원하는 LongStraw 스택, 희소 MoE와 DSA 기반 베이스의 안정성·롤아웃-학습 불일치 제어 기법을 구현·제시했다.
- Personal Intelligence 중심 벤치마크와 평가지표: Macaron ChatBench(대화 사례 46건), Macaron LivingBench(시뮬레이션 40개 시나리오), UI4A-Bench(161개 UI 생성 사례) 등을 정의해 상호작용 궤적 단위로 평가했다.
- 공개 모델 가족과 배포 프로필: GLM-5.2(744B) 베이스에 4개 LoRA를 얹은 Macaron-V1-Venti와 Qwen3.6 기반 Macaron-V1-Tall(약 50B 환산)을 설계·배포하고, adapter 메타데이터(저장된 값 수, rank, alpha, 대상 모듈, 학습 하이퍼파라미터)를 공개했다.

## 접근 방법

* 아키텍처: 고정된 대형 베이스 모델을 유지하고(베이스는 고정), 여러 개의 LoRA 어댑터(L0 Chat, L1 Agent, L2 Coding, L3 GenUI)를 학습·레지스트리에 등록해 런타임에서 Proxy가 per-turn로 하나의 어댑터를 선택해 응답을 생성한다.
* 라우팅: L0이 constrained decoding(24토큰 예산)으로 정규화된 어댑터 라벨(L0–L3)을 생성하면 Proxy가 해당 어댑터로 턴을 전달한다(라벨은 하나만 허용).
* 응답-요약 루프: 선택된 어댑터가 응답을 생성하고(Answer), 이어서 최대 192토큰의 요약(Summary)을 생성해 서버에만 저장하고 다른 어댑터들이 이후 턴에서 상속할 수 있도록 함.
* 컨텍스트·KV 재사용: 각 어댑터의 own-view를 deterministic하게 재구성해 해당 어댑터 재진입 시 byte-identical prefix가 생성되므로 엔진의 prefix KV 캐시가 재사용되게 했다(요약은 다른 어댑터의 상세 상태를 노출하지 않음).
* 익스펜션/학습 루프(RSI): 모델-하니스 공동설계 아래 하니스 변형을 생산 환경에서 롤아웃하여 궤적을 감사(audit)하고, 외부 계약(HCP)에 따라 선택된 궤적을 학습 데이터로 변환해 어댑터를 업데이트하는 재귀적 개선을 제시하나, 본 보고서의 실험은 고정 모델 상태에서 하니스 탐색(Expansion)만 격리 평가함.
* 인프라: MinT(어댑터/모델 리비전/레지스트리), LongStraw(응답 전용 장문 실행), EAGLE 등 추정·사전 계산 스펙을 포함한 병렬화·KV 용량 관리 기법을 적용했다.

## 주요 결과

- MoL·라우팅 지연: Macaron-V1-Venti(GLM-5.2)에서 Route(L0 constrained-decode 24 tok)=0.54s, Answer(specialist gen)=3.17s, Summary(≤192 tok)=0.97s, 총 4.68s. Route+Summary 합계는 약 1.51s로 3-hop 총 시간의 ≈32%를 차지. Macaron-V1-Tall(Qwen3.6-35B-A3B)은 총 1.76s(0.20s+1.24s+0.32s)였다(표 Table 1).
- 라우팅 정확도: 6,448 샘플 트레이스(훈련 데이터에서 추출된 trace, 보류된 독립 검증 아님)에서 Macaron-V1-Venti는 6391/6448 = 99.12% 정확도(100% canonical compliance), Macaron-V1-Tall은 99.04%를 기록(표 Table 2).
- KV 재사용과 품질(작업별 Vita 전달 실험): Macaron-V1-Venti에서 Direct L1(단일 어댑터 기준) 보상 0.636 ± 0.026, Routed KV-off 0.650 ± 0.030, Routed KV-on 0.632 ± 0.019. Macaron-V1-Tall에서는 Direct 0.410 ± 0.030, Routed KV-off 0.398 ± 0.035, Routed KV-on 0.386 ± 0.054. (Table 3) 이 소규모(각 암 5시드, unpaired) 비교에서 명시적 열화는 보고되지 않았음.
- 어댑터·거주 파라미터: Macaron-V1-Venti 공개 어댑터 헤더 합계는 어댑터당 7,688,042,496 저장값(저장 텐서 수)이며 4개 어댑터로 약 +30.8B(논리적)로 베이스(명목 744B)에 더해져 논리적 총 774.8B가 됨. 복제된(merged) 각 베이스를 따로 배포하면 4복제 시 2.976T가 되므로 MoL은 논리적 파라미터 수에서 약 26% 수준(약 74% 절감). (Section 2.6)
- RSI(분리된 Expansion 실험) 결과: 고정 모델·하니스 탐색 실험에서 adaptive search가 선택된 base-failure 과제 세트 122/122 누적 커버리지를 달성한 반면, 두 개의 전체-셋 단일-구성 탐색 중 더 강한 하나가 11/122를 달성(Section 3 요약, 기여 항목 참조). 이 실험은 구성 검색(coverage)을 측정한 것이며 전체 RSI(롤아웃→학습)로 인한 성능 향상 증거는 아니라고 저자가 명시함(즉 학습 단계는 격리됨).

## 한계

- 저자 언급: MoL의 '어댑터 레지스트리'·'베이스 불변성'·'라이브 하니스 업데이트'는 아키텍처적 속성이며, 여러 세대에 걸친 지속적 개선이나 독립적으로 훈련된 다수 어댑터의 합성(collective intelligence)으로 인한 능력 증대는 본 리포트에서 증명되지 않았음(Section 2.7, 7.2).
- 저자 언급: RSI 실험은 Expansion 단계(모델 고정, 옵티마이저 스텝 없음)만 격리 평가했으며, 모델 가중치 업데이트를 포함한 전체 재귀적 자기개선 사이클의 효과(누적 개선, 전달 및 보존)는 아직 열려 있는 문제로 남아 있음(Contributions 및 Section 3 설명).
- 본문에서 확인되는 한계: 라우팅 정확도 측정에 사용된 6,448 샘플 트레이스는 훈련 데이터에서 뽑힌 trace로 독립된 홀드아웃이 아니며, 따라서 라우팅 일반화 성능의 엄밀한 추정치는 아님(Section 2.3).
- 본문에서 확인되는 한계: Vita·KV 재사용 비교는 소규모(각 암 5시드), seed 식별 미보존으로 unpaired 비교이며 동등성 또는 열등성을 입증하지 않음(표 3). 또한 route-decode overlay는 실험적 옵션으로 현재 기본 경로는 emergent own-view 경로임(Section 2.5).  
  
(추가 실험 설정·paired 평가·다양한 분포에서의 재현이 필요).

## 개발자 관점

- 재현 및 서빙 운영 주의: 엔진 버전, 하드웨어, attention 백엔드, 병렬화 레이아웃(예: DCP/TP 구성) 등은 단일의 '운영 포인트'로 간주해야 하며, 논문에서 보고한 용량·정확성·정합성 측정은 특정 구성에 귀속된다(Appendix C).
- 라운드트립 비용: per-turn 라우팅(route 24 tok)과 요약(≤192 tok)이 평균 응답 시간의 약 32%를 차지하므로 실시간 성능·비용을 고려해 라우팅 빈도 및 요약 길이 정책을 설계해야 한다(표 1).
- 자원 절감의 장점과 한계: MoL은 베이스를 공유함으로써 저장된 파라미터(저장 텐서 수)를 크게 줄여(약 26% 논리적 규모) 다전문가 서비스를 실현하지만, 이는 병렬 병목·KV용량·지연에서 별도 배포된 merged-specialist 대비 항상 유리함을 보장하지 않는다(Section 2.6). 성능·지연 비교는 운영 지점별로 측정 필요.
- 데이터·평가 설계: Macaron ChatBench·LivingBench 등은 제품 표적 분포를 반영한 내부 벤치이며 판정자(자동 judge)·시뮬레이터 스택의 편향 가능성이 존재(예: 동일 모델 계열이 유리할 수 있음), 재현 가능한 공개 벤치·인간 평가 동의율·데이터 오버랩 감사가 필요(Appendix B).
- 어댑터 운영·보안·거버넌스: 어댑터 등록·합성은 다수 소유자/개발자 환경을 겨냥하므로 어댑터 호환성·출처 증명·권한·도구 노출(visibility) 정책과 HCP 같은 런타임 계약·감사 로그가 필수적이다(Section 2.7, 3.1).

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(본문 및 부록)을 직접 인용·요약하여 작성했다. 표와 수치는 본문 및 부록에 명시된 값에 근거했으며, 일부 결과(예: 배포 성능·장문 처리 용량)는 다양한 엔진·하드웨어 구성에 크게 의존한다고 저자가 명시하므로 일반화에 주의가 필요하다. 독립적인 복제나 추가 실험이 필요한 항목(예: 전체 RSI 사이클의 누적 이득, 다팀 어댑터의 집합적 이점, paired 품질 검증)은 본문에서 저자도 열린 문제로 제시하고 있다.
