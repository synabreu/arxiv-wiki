# COVER: Identifiable Evaluation of Coalition Routing

- **게시일:** 2026-08-31
- **arXiv:** [2608.28475v1](http://arxiv.org/abs/2608.28475v1) · [PDF](https://arxiv.org/pdf/2608.28475v1)
- **저자:** Raghul Sugumar, Amrit Gopinath
- **분야:** cs.AI
- **선정 점수:** 4.87
- **선정 이유:** 최근성 0.5, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.2, 개발자 관심 0.2, 학술 신호 0.8, 오픈 웨이트·주요 연구조직 신호 1.2

[← 2026-08-31 목록으로 돌아가기](../daily/2026-08-31.html)

## 한 문장 요약

COVER는 공용 정보 경계와 downstream 스택 G, 그리고 유한한 합법적 팀 가족을 사전에 고정해 ‘선택된 연합(coalition)’만을 바꿔서 측정함으로써, 동일 스택 조건하에서의 유한-벤치마크 오라클 회귀(regret)를 식별 가능한 방식으로 평가하는 계약(평가방법론)을 제안한다.

## 해결하려는 문제

기존의 다중 에이전트/라우팅 비교는 시스템 전체(라우터 + downstream 파이프라인)의 end-to-end 성능 차이를 보고 ‘라우팅 효과’로 해석하는 경향이 있으나, 실제로는 팀 선택이 바뀌면 비공개 메시지와 파이널라이저 동작이 함께 바뀌어 관찰된 차이가 라우팅 선택 때문인지 downstream 변경 때문인지 식별 불가능해지는 교란(confound)이 존재한다. 따라서 라우팅의 선택 품질(oracle 대비 회귀)을 동일한 downstream 프로토콜과 고정된 공용 정보 경계 하에서 어떻게 정확히 식별·측정할지에 대한 문제가 남아있다.

## 핵심 기여

- 스택-조건(conditional) 평가 계약(COVER)을 제시하고, 유한-벤치마크 오라클 회귀의 완전-커버리지(complete coverage)가 동일 스택 G 하에서 정확히 식별됨을 명확히 함.
- 유한 정책(라우터) 집합 비교에서 ‘라우트 합집합(route union)’이 모든 쌍wise 정책 대비(pairwise contrasts)의 최소한의(및 포함-최소) 가정-자유(assumption-free) 실행 지지(minimal support)임을 증명(정리 1).
- 두 개의 완전 개입(complete-intervention) 통제 표(Controlled tables, MuSiQue-12, HotpotQA-4)와 소스 ID가 분리된 train/dev/held-out 분할을 제공하여 평가도구를 인스턴스화하고 검증함.
- 고정 스택(동일 workers·finalizer) 하에서 실행을 분해하여(verified-evidence vs raw-answer) 선택(선택된 연합)과 합성(파이널라이저 성능)을 분리 평가하는 절차·진단을 제시함.
- 자연적 도구 환경(5-family ToolSandbox)에서 선언된 16개 팀을 완전 평가하는 변이-이동(variant-shift) 검증을 수행해, 선언된 가족 오라클과 실제 prospectively frozen 라우터 성능의 격차를 노출함.

## 접근 방법

* 핵심은 평가 계약으로 다섯 항목을 고정하는 것이다: (1) 사전 선언된 행동 공간(유한한 합법적 팀들 Fx), (2) 정보 경계(라우터는 공용 텍스트와 카드만 보고 비공개 증거·결과는 알지 못함), (3) downstream 프로토콜 G(작업자, 메시지 순서, 토큰 정책, 파이널라이저, 유틸리티 등)를 고정, (4) 커버리지 규칙 — 절대 오라클 회귀를 원하면 모든 합법 팀을 실행하거나, 동결된 정책들(frozen policies)의 쌍별 대비만 식별하려면 그들이 선택한 팀들의 합집합(route union)만 실행, (5) 추론 규칙 — 라우터는 held-out 이전에 고정(freeze)하고 task를 재표본하여 불확실성을 평가한다.
* 이론적으로는 Theorem 1을 통해 frozen-policy 비교에서는 각 태스크별로 정책들이 선택한 서로 다른 팀들의 합집합 Ax(R)이 포함되어야 쌍별 차이가 점-식별(point-identified)됨을 보였다.
* 구현·검증 측면에서는 두 제어된 표(MuSiQue-12: 500개 held-out, 각 태스크 220개의 size-3 팀; HotpotQA-4: 300개 held-out, 각 태스크 4개의 size-3 팀)를 구성하여 완전 개입으로 정확한 벤치마크 회귀를 측정하고, UNIFIED-COVER(문장 인코더(MiniLM) + 집합 불변(pool) + MLP로 팀 값을 회귀/순위 학습)과 PARTITION-COVER(쌍 호환성 qij를 학습하고 균형 파티션을 비트마스크 DP로 정확히 복원하는 구조적 디코더)를 정책·검증 도구로 사용했다.
* 추가로 고정 스택(Llama 실행)에서 두 라우터의 합집합을 실행해 '검증된 증거(verified evidence) 전송'과 'raw answer'를 분리 측정했고, ToolSandbox에서는 5개 가족(단일/쌍/전체 포함 16개 연합)을 선언해 Qwen2.5-14B-AWQ 실행기로 공식 안전-도구 마일스톤 완료 비율로 값을 측정하는 자연적 검증을 수행했다.

## 주요 결과

- 이론적: 정리(Thm.1) — 유한 frozen-policy 비교에서 각 태스크별 정책들이 선택한 서로 다른 팀들의 합집합(Ax(R))을 Ox에 포함하면 모든 쌍별 대비가 점-식별되며, 이 합집합이 포함-최소(uniquely inclusion-minimal) 지원임을 보였다.
- MuSiQue-12(500 held-out, 220 legal size-3 팀/task): 사후 설계된(public) 인터페이스 대조에서 partition 디코더(공개 인터페이스)가 regret 0.424 vs matched graph 0.554(후향적(retrospective) 결과로서 해석 제한). 사전에 지정된(privileged) positive control은 0.402 vs 0.532로 도구 민감도 검증(제어). (Table 4, 8)
- HotpotQA-4(300 held-out, 4 legal size-3 팀/task): UNIFIED-COVER 대 leave-one-out baseline 결과 regret 0.110 vs 0.313, 페어드 이득 0.2033, CI [0.1533,0.2567], sign-flip p = 1e-5 (사전 지정된 주 검정). (본문 Sec.4.1–4.2, Table 4, Fig.2)
- 고정 스택 Llama 실행(300-task): 'verified evidence complete' 비율 UNIFIED-COVER 81.67% vs leave-one-out 62.67%; 실행된-route(regret) 차이는 0.190 포인트(95% CI [0.140,0.240], Holm p = 3e-5)으로 유의함. 반면 raw-answer 차이는 0.010(95% CI crossing zero: [−0.0067,0.0267])로 파이널라이저 영향을 분명히 보임. (Table 5, Sec.5)
- ToolSandbox 자연적 검증(held-out 14 tasks × 16 coalitions = 224/224 valid rows): 선언된-가족 오라클(declared-family oracle) completion 0.768. Prospectively frozen public-capability router completion 0.637, regret 0.131 (task-bootstrap CI [0.042,0.244])로 미리 정한 0.10 기준 실패. 사후(후향) 개발-선택된 comparator와 all-workers는 0.655로 일치하며 평균 worker 수는 5.00 → 4.57로 감소(사후 비교). (Table 6, Sec.6)

## 한계

- 저자가 명시한 한계: 통제된 테이블 결과는 '구성된(evidence-coverage) 측정'이며 자연적 팀 유틸리티나 대규모 도구 풀에 대한 일반화 주장 아님; MuSiQue의 pre-specified 정책은 특권적(privileged) positive control이고 public-interface 결과는 후향적(retrospective)이라 배포-타당성 대체 불가; ToolSandbox는 held-out에 14개 변이만 포함되어 있으며 사후 비교는 전향적 결과로 승격 불가; 제공자(provider) 단일 호출(one-draw) 실행은 모집단(population) 유틸리티를 식별하지 못함; COVER는 스택 불변(stack-invariant) 또는 보편적 라우팅 우월성을 주장하지 않음 (본문 Sec.9).
- 본문에서 합리적으로 확인되는 제약(저자와 구분): 완전-커버리지는 비용(개입 수)이 커서 실무에서 확장성 문제 존재함(저자도 언급); 대규모 행동공간에서는 완전실행 불가하며 route-union도 전체 오라클 회귀는 식별하지 못함; 제공자 실행 결과는 재현 가능한 로그-아티팩트와 해시가 있어도 provider-side 변화로 완벽 재생성 불가(본문 Sec.7); Partition-COVER의 DP 디코더는 O(2^n n^2) 시간·O(2^n) 메모리로 n=12까진 실용적이지만 큰 n에 비실용적임(본문 C.2).

## 개발자 관점

- 평가 설계: 라우팅 실험에서는 (1) 평가 전에 합법적 팀 가족(Fx)을 사전 선언하고, (2) downstream 스택 G와 정보 경계를 문서화·고정하며, (3) 라우터를 held-out 전에 동결(freeze)해야 라우팅-선택 효과를 식별할 수 있다.
- 실험 비용·스케일: 절대 오라클 회귀 식별을 위해선 모든 합법 팀을 실행해야 하므로 비용이 빠르게 증가한다. 유한 frozen-policy 비교 목적이면 각 태스크에서 정책들이 선택한 서로 다른 팀들의 합집합(route union)만 실행하는 것이 포함-최소 지원이며 비용을 줄이는 현실적 절충이다.
- 분해 측정 권고: 선택(팀) 성능과 파이널라이저(합성·answering) 성능을 분리(예: verified-evidence 전송 vs raw-answer)해야 라우팅이 실제로 증거를 전달했는지, 혹은 downstream 합성에 의해 성능이 가려지는지 판단할 수 있다.
- 재현성·아티팩트 관리: 소스-ID 매니페스트, 라우트 파일, 태스크-레벨 결과, 해시·freeze 기록을 공개하여 후속 재평가·감사를 가능하게 해야 한다. 단, 원문(public source text) 라이선스 문제로 sanitized archive만으로는 새로운 라우터를 실행할 수 없음을 명확히 기록해야 한다.
- 방법·구현 팁: UNIFIED-COVER는 사전학습 문장 인코더(MiniLM)와 집합 불변 풀링+MLP 조합으로 구현했으며, PARTITION-COVER는 qij 호환성 학습 후 비트마스크 DP로 균형 파티션을 정확히 복원(복잡도 O(2^n n^2))한다—따라서 n 범위를 사전에 제약해야 한다.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(페이지 1–17 및 부록)을 근거로 작성되었다. 주요 수치(예: 각 실험의 regret, 비율, CI, task·team 수 등)와 이론적 정리는 본문에 직접 표기된 값을 그대로 사용했다. 제공자가 내부적으로 변경 가능하다는 점, 일부 비교(예: MuSiQue public 인터페이스)는 후향적이라고 저자가 명시한 점 등도 본문에서 확인했다. 코드·데이터 접근성·운영 세부(예: provider 환경의 비결정성) 등은 저자 진술과 공개 아티팩트를 바탕으로 해석했으며, 본문에 명시되지 않은 추가 구현·하이퍼파라미터는 생성하지 않았다.
