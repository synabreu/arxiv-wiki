# STR-Agent: An LLM-Driven Agent for QoS-Aware Routing in LEO Satellite Networks

- **게시일:** 2026-09-18
- **arXiv:** [2609.20347v1](http://arxiv.org/abs/2609.20347v1) · [PDF](https://arxiv.org/pdf/2609.20347v1)
- **저자:** Bowen Lu, Mugen Peng, Yaohua Sun, Hongyu Wang, Kerui Guo, Wenjia Xu
- **분야:** cs.NI, cs.AI
- **선정 점수:** 4.96
- **선정 이유:** 최근성 1.2, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 3.0, 개발자 관심 0.2, 학술 신호 0.5, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-09-18 목록으로 돌아가기](../daily/2026-09-18.html)

## 한 문장 요약

자연어로 표현된 서비스 의도를 도메인 특화된 LLM 기반 에이전트(STR-Agent)가 해석하고, 툴 실행·경험 축적·반영(Reflection)을 통해 서비스별(지연·대역폭·최저홉) 적응형 QoS 라우팅 정책을 동적으로 선택·수행하여 LEO 위성망에서 지연 및 혼잡 완화 성능을 개선한다.

## 해결하려는 문제

기존 LEO 라우팅 연구는 고정된 최적화 목적이나 구조화된 서비스 입력을 전제로 하여(1) 서로 상충하는 지연·대역폭·부하분산 요구를 유연히 조절하지 못하고,(2) 사용자 요구가 자연어로 주어지는 현실적 상황에서 의도를 해석해 적절한 라우팅 정책으로 변환하는 문제를 다루지 못한다. 본 논문은 자연어 서비스 요청을 구조화된 라우팅 의미론으로 변환하고, 실시간 혼잡 정보와 과거 라우팅 경험을 이용해 서비스별로 적응적 라우팅 알고리즘을 매핑·선택하는 폐쇄루프 intent-to-routing 문제를 해결하고자 한다.

## 핵심 기여

- STR-Agent라는 LLM 기반의 폐쇄루프 의도→라우팅 에이전트 아키텍처(Perception, Execution, Experience Buffer, Reflection)를 제안하여 자연어 서비스 요청을 QoS-적응형 라우팅으로 연결했다.
- 네트워크 실시간 상태(평균 큐길이, 90퍼센타일 큐길이, 과부하 위성 수)와 홉별 경험 통계(지연·큐 길이 등)를 결합해 서비스(b)→알고리즘(a) 매핑을 동적으로 조정하는 Reflection 메커니즘을 제시했다.
- LEO 도메인 특화의 감독학습 데이터셋(각 클래스별 10,000 훈련 샘플, 테스트 1,000 샘플)과 Qwen2.5-7B 기반의 LoRA 수단을 통한 Perception 모듈의 SFT 절차를 구성·적용하여 의도 이해 성능을 크게 향상시켰다.
- 시뮬레이션(워커–델타, Np=72, Nm=22, N=1584, 고도 550km)에서 STR-Agent(SFT)가 DQ-Dijkstra·QSMR 기반 기법들보다 지연·큐 길이·홉 수 측면에서 우수함을 보였고, Reflection 모듈이 고부하에서 추가적인 지연 감소(예: 600 Mbps에서 약 120 ms 개선)를 제공함을 실증했다.

## 접근 방법

* 아키텍처: STR-Agent는 Perception, Execution, Experience Buffer, Reflection 네 모듈로 구성된다.
* Perception: 자연어 요청 rk를 {src_lat, src_lon, dst_lat, dst_lon, service_type}의 구조화된 의미로 변환한다.
* 서비스 유형 bk은 {Bdelay, Bbw, Bhop} 중 하나로 분류된다.
* 지리 엔티티 추출과 서비스 타입 분류를 결합한 출력 형식을 사용한다.
* Execution: Perception의 출력으로부터 출발·도착 접근 위성 쌍을 결정하고, 홉 단위 포워딩을 수행한다.
* 매 홉마다 Network State Tool로 현재 혼잡 프로파일 C(t) = (¯Q(t), Q90(t), Nhot(t))를 조회하고, Reflection이 반환한 서비스→알고리즘 매핑 M(t)에서 선택된 라우팅 툴(Delay-Sensitive, Bandwidth-Sensitive, Best-Effort 중 하나)을 호출해 다음 홉을 계산한다.
* 사용되는 툴에는 Satellite Access Tool, Network State Tool, 그리고 세 가지 Dijkstra 기반 라우팅 툴이 포함된다.
* 라우팅 알고리즘: 모든 라우팅 툴은 Dijkstra Shortest Path를 기반으로 하며 엣지 가중치는 서비스에 따라 다르다.
* 지연 민감형 가중치 w_delay_ij = dij/c + Lp/Rij, 대역폭 민감형 가중치 w_bw_ij = σ({Qn : n∈N(i)}) (이웃 큐길이의 표준편차), 베스트이포트 whop_ij = 1.
* Experience Buffer: 홉별 기록 e_h = (b_h, a_h, ℓ_h, Qdec_h, Qarr_h, τ_h)를 저장하고 창(rolling window) 단위로 S(b,a,ℓ) = (¯τ_{b,a,ℓ}, ¯Qdec_{b,a,ℓ}, ¯Qarr_{b,a,ℓ}, N_{b,a,ℓ})로 요약한다.
* 최근 관측이 더 크게 반영되도록 갱신한다.
* Reflection: 현재 혼잡 상태(심각 혼잡 판단 기준: 평균 위성 큐길이 ≥5 또는 큐>5인 위성 수 ≥50)와 최근 경험 통계 S를 비교해 서비스→알고리즘 매핑 M(t)를 조정한다.
* 예컨대 지연민감 트래픽의 경우 최근 대역폭 민감형의 평균 홉 지연이 더 낮다면 일시적으로 Bbw로 전환한다.
* 학습·추론 절차: Perception은 Qwen2.5-7B를 LoRA로 SFT(LoRA rank=8, scaling=16, dropout=0.05, lr=2e-4, batch=64, epochs=3)하여 사용한다.
* 실행 시 에이전트는 홉별로 툴을 호출하며 Reflection은 경험 요약을 기반으로 주기적으로 매핑을 갱신한다.

## 주요 결과

- 의도 이해(Perception): 테스트셋(클래스별 1,000 샘플, 총 3,000)에서 Base Qwen2.5-7B 평균 정확도 45.4% → Prompt 기반 80.74% → SFT 기반 92.45%. 클래스별 정확도(%)는 SFT: Delay 97.7, Bandwidth 95.45, Best-Effort 84.2. (Table I)
- 라우팅(시뮬레이션): 워커–델타(72×22, 1584 위성), 채널 fc=23.28 GHz, BW=2 GHz, EIRP=35 dBW, Gr/Ts=6.8 dB/K, 변조 8-PSK, 목표 BER=1e-7. 트래픽은 포아송 도착, 데이터율 90–270 Mbps(또는 추가 실험에서 350–600 Mbps)를 사용. 비교 대상은 DQ-Dijkstra, QSMR, STR-Agent(Base/Prompt/SFT).
- 정량 성과 예시: STR-Agent(SFT)는 270 Mbps에서 QSMR의 평균 지연 696.01 ms를 260.11 ms로 감소시킴(문헌 본문). 270 Mbps에서 DQ-Dijkstra 대비 평균 per-hop 큐 길이를 1.06→0.71로, per-hop 큐잉 지연을 5.22 ms→2.50 ms로 낮춤(본문). 270 Mbps에서 평균 홉 수를 QSMR의 53.03→25.94로 감소(본문).
- Reflection 효과: 고부하(350–600 Mbps)에서 Reflection을 켰을 때(STR-Agent SFT Full)와 끈 경우(No Reflect)를 비교하면, 부하 증가에 따라 이득이 커지며 600 Mbps에서 평균 지연이 약 1320 ms→1200 ms로 약 120 ms 감소(본문).

## 한계

- 저자 명시 한계: 인간(label) 라벨링 요청의 검증, 학습 기반(learning-based) 비교 기법 추가 평가, 실시간(런타임) 오버헤드 분석이 향후 과제로 제시되었다(본문 결론 및 향후 연구).
- 본문 기반으로 합리적으로 확인되는 제약: 데이터셋이 Qwen2.5-7B로부터 합성적으로 생성되어(Section IV-A) 실제 인간 표현의 다양성과 노이즈를 완전하게 반영하지 않을 가능성이 있다. 실험은 단일 워커–델타 구성(Np=72,Nm=22)과 포아송 트래픽 모델에 대해 수행되어 다른 위성 토폴로지·교통 패턴·실측 무선 채널 변동성에서의 일반화가 검증되지 않았다. 에이전시 아키텍처는 홉별로 네트워크 상태 조회와 LLM 기반 의사결정(또는 툴 호출)을 수행하므로 실제 운영환경에서의 지연·연산·신호 오버헤드(런타임 비용)는 측정되지 않았다. 또한 베스트-이포트 클래스의 인식·성능이 타 클래스보다 일관되게 낮아(예: Base 8.27%→SFT 84.2%) 최종 성능에 민감한 분류 오류 위험이 남아 있다.

## 개발자 관점

- 재현성: 코드 저장소가 논문에 링크(https://github.com/IntelliSensing/STR-Agent)되어 있어 주요 구성요소(Perception SFT, 툴 인터페이스, Experience Buffer, Reflection 로직)를 확인·실행할 수 있다.
- 데이터/학습: Perception SFT는 Qwen2.5-7B를 LoRA로 미세조정했으며 하이퍼파라미터(LoRA rank=8, scaling=16, dropout=0.05, lr=2e-4, batch=64, epochs=3)가 논문에 명시되어 있어 유사 재현이 가능하다. 다만 원시 학습 데이터는 Qwen2.5가 생성한 합성 샘플이므로 실사용을 위해서는 인간 라벨링 데이터로 추가 검증이 필요하다.
- 구현·배포: 에이전트는 홉별로 Network State Tool 호출과 라우팅 툴 실행을 반복하므로 실시간 제약(응답 지연)이 엄격한 지연 민감형 서비스에선 LLM 호출 지연을 줄이기 위한 설계(예: 로컬 경량화 모델, SFT 모델을 계속 유지하여 프롬프트 호출 최소화, 캐싱)와 비동기적 툴 인터페이스가 필요하다.
- 비용·연산: Qwen2.5-7B를 포함한 대형 모델 SFT와 추론은 계산 자원·전력·비용이 크므로 운영 환경에서는 모델 경량화(LoRA로 SFT 후 소형 추론 백엔드 등), 배치 추론 또는 엣지-중앙 하이브리드 아키텍처를 고려해야 한다.
- 안전성·신뢰성: 의도 오분류 시 잘못된 라우팅 정책 선택으로 긴급 서비스 품질이 손상될 수 있으므로 인간 검토 경로, 보수적 기본 정책(critical 서비스에 대한 fail-safe), 및 모니터링·알림 체계가 필요하다. 또한 홉별 툴 호출이 네트워크 부하를 유발할 수 있으므로 제어 평면 부하를 제한하는 rate-limit과 로컬 추정치 사용을 권장한다.

**근거 범위:** 논문 PDF 본문(페이지 1–6)의 텍스트에 기반한 분석이다. 표 및 본문에서 명시된 수치(의도 이해 정확도, 시뮬레이션 설정, 라우팅 성능 지표, LoRA 하이퍼파라미터 등)를 직접 인용했으며, 그림에서 곡선 전체 수치가 표기되지 않은 부분은 본문에 명시된 주요 수치만 보고 반영했다. 코드·데이터의 세부 구현·런타임 비용·실제 운영 지연 등은 본문에서 정량적으로 제시되지 않아 해당 항목은 추정 없이 한계·시사점으로만 기술했다.
