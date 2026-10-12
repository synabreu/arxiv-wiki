# GPU-resident Execution for Timing-predictable Sensor Processing Systems

- **게시일:** 2026-10-12
- **arXiv:** [2610.13809v1](http://arxiv.org/abs/2610.13809v1) · [PDF](https://arxiv.org/pdf/2610.13809v1)
- **저자:** Soham Sinha, Rahul Choudhury, Shekhar Dwivedi, Gregory Lee, Gigon Bae, Anisha Goel, Elena Agostini, Patrick O'Grady, Yosi Levi, Mahdi Azizian
- **분야:** cs.DC, cs.OS
- **선정 점수:** 4.46
- **선정 이유:** 최근성 0.5, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 1.3, 개발자 관심 0.8, 학술 신호 0.6, 오픈 웨이트·주요 연구조직 신호 1.4

[← 2026-10-12 목록으로 돌아가기](../daily/2026-10-12.html)

## 한 문장 요약

GPU-resident Execution이라는 장기 실행 GPU-내 루프 모델을 제안해 센서→가속 처리→액추에이션 폐회로의 시간 예측성을 확보하고, Holoscan C++ 프레임워크로 구현해 다양한 GPU/SoC에서 지터를 대폭 감소시켰다.

## 해결하려는 문제

기존 실시간 임베디드 센서 처리 파이프라인은 GPU에서 연산을 수행하더라도 프레임 단위 I/O 감지·CUDA 작업 제출·완료 대기·액추에이션 커밋 같은 제어 흐름이 호스트(CPU)를 통해 이루어진다. 이 경로는 인터럽트 전달 지연, 호스트 스케줄러 변동, CUDA API 및 드라이버 오버헤드에 민감해 폐회로의 끝-끝 지연과 지터를 유발한다. PREEMPT_RT, 코어 격리, GPUDirect RDMA 같은 완화책은 일부 비용을 줄이나 제어평면(프레임당 I/O·CUDA 제어)을 호스트에 남겨두므로 근본적 시간 불확실성을 제거하지 못한다.

## 핵심 기여

- GPU-resident Execution이라는 실행 모델 제안: 센서 입력 수신, 장치내 데이터-준비 핸들러, GPU내 루프(장기 실행 CUDA Graph)로 센서→처리→출력 경로를 호스트 깨우기 없이 수행하도록 설계.
- NVIDIA Holoscan C++ 프레임워크에 모델을 통합하고, GPU-레지던트 연산자(operator), 데이터-준비 핸들러, 출력(디스플레이) 등 참조 컴포넌트 제공.
- GPU 메모리 RDMA(GPUDirect)와 GPU-driven I/O(DOCA GPUNetIO)를 결합해 센서 데이터의 GPU 메모리 입출력과 장치측 폴링을 달성함으로써 호스트의 주기적 제어를 제거.
- CUDA Graph WHILE 노드 또는 device-graph tail-launch를 활용해 그래프를 디바이스에 상주시키고 장치측 컨트롤러·IF·end-marker로 반복 루프를 구현하여 per-frame 호스트 API 호출을 없앰.
- 다양한 플랫폼(x86+Ampere, Orin/Thor SoC + Ada/Blackwell 등)과 워크로드(추론, 호스트 경쟁, 다중 루프, 카메라 스트리밍)에서 실험해 지터·표준편차·최댓값 등 시간 분포 개선을 입증 (산업용 1080p@60Hz 카메라→디스플레이 사례에서 photon-to-display 지터를 4.83ms→0.66ms로 7.3× 감소 등).

## 접근 방법

* 아키텍처 개요: 애플리케이션은 GPU-레지던트 연산자들로 구성된 DAG로 표현되고, 호스트는 초기화 시점에 센서/출력 엔드포인트와 디바이스 버퍼를 할당하고 연산자 DAG를 토폴로지 순서로 캡처하여 하나의 CUDA Graph(WHILE 기반 또는 device-tail-launch 기반)로 구성·한 번만 런칭한다.
* 그 이후의 정상 상태(steady-state) 반복은 GPU 내부에서만 실행된다.
* 주요 구성요소: 데이터-준비 핸들러(데바이스 메모리·NIC CQ를 폴링하고 dataReady 플래그를 세팅), 디바이스 컨트롤러 커널(플래그를 읽어 IF·WHILE 조건 설정 및 데이터-없음 시 지정된 sleep 간격으로 지연), IF로 게이트된 연산자 DAG(각 연산자는 device-only 포트로 CUDA 커널 또는 라이브러리 호출을 캡처), end-marker(반복 경계 처리 및 결과 커밋).
* I/O 서브스트레이트: Holoscan Sensor Bridge(HSB)와 ConnectX NIC를 통한 GPUDirect RDMA로 페이로드를 GPU 메모리로 직접 수신하고, DOCA GPUNetIO를 사용하면 GPU측에서 CQ 폴링·WQE 재게시·doorbell 작동이 가능.
* 실행 환경: 각 GPU-resident 애플리케이션은 고정 SM 예산(정적 CUDA MPS 파티션 또는 전체 GPU 컨텍스트)에서 실행되고 GPU 클럭은 고정(locked)해야 예측성이 확보된다.
* API/구현: Holoscan의 C++/CUDA API로 Application/ GPUResidentOperator/ GPUResidentHandler 인터페이스를 제공해 구성·캡처·런칭·종료를 지원.

## 주요 결과

- (마이크로벤치) 단일 단계 TensorRT 추론(5개 모델): 조용한 시스템에서 GPU-resident는 표준편차와 절대 지터를 모델별로 1.4×–2.4×까지 감소시키며 특히 MobileNetV2, EfficientNet-B0, ResNet-50에서 유의미한 분산 감소를 관찰(세부 수치: 본문 Fig.6).
- (호스트 경합) 동일 추론 모델을 CPU 배경부하(디스크 I/O·메모리 스트레스) 하에서 실행하면 CPU-driven CUDA Graph(CPU-CG)는 몇 개 모델에서 1.05ms–2.15ms 수준의 상위 꼬리와 한 사례에서 97.99ms 최댓값을 관측한 반면, GPU-resident는 9µs–86µs 범위의 낮은 지터로 안정적이었다 (본문 §V-B2 및 Fig.7).
- (에뮬레이트 I/O, 행렬곱 워크로드) RTX A6000에서 CPU-CG(블로킹) 대비 GPU-resident는 표준편차 14.5µs→9.3µs(−36%), p99.9−p50 25.7µs→16.5µs(−36%), 절대 지터 239µs→189µs(−21%)를 달성(본문 Fig.8a, 표본 수 1,000,000 반복).
- (동시 다중 루프 확장성) 1→20개 동시 루프(각 루프에 4-SM 정적 MPS 파티션) 실험에서 GPU-resident는 5→20루프 구간에서 p99.9와 최대지연이 비교적 안정(최대 약 2× 범위)인 반면 CPU-CG는 꼬리와 표준편차가 급격히 악화. 예: 10개 루프에서 GPU-resident는 stddev 29.3µs→7.6µs(상대 비교), p99.9 1113.6µs→50.2µs, 최대 1850.3µs→404.5µs로 개선(본문 Fig.10–11).
- (프레임워크 고정 오버헤드) WHILE 기반 그래프의 반복 경계별 플랫폼별 고정 비용을 Table I로 제시: handler→controller 전이 0.82µs, controller kernel 1.67µs, controller→body 3.69µs, body→end 1.37µs, end→DRH(next-iteration) 5.67µs(최대값). (본문 Table I).","(사례연구: IMX274 1920×1080@60Hz 카메라→디스플레이) IGX Orin + RTX 6000 Ada에서 하드웨어 측정(HSB FPGA + GPIO/광센서) 결과: CPU-driven (no GDR) 평균 photon-to-display 24.0ms, 지터 J=22.0ms(최대 35ms); CPU-driven (with GPUDirect RDMA) 평균 16.2ms, J=4.83ms(최대 18.83ms); GPU-resident 평균 12.8ms, J=0.66ms(최대 13.35ms)로 GPU-resident가 photon-to-display 지터를 CPU-driven(GDR) 대비 4.83ms→0.66ms(7.3×) 감소시킴. 소프트웨어 처리 구간(프레임 플랫폼 진입 이후): CPU-driven(w/ GDR) 평균 0.96ms, 최대 2.60ms, J=1.70ms; GPU-resident 평균 0.30ms, 최대 0.31ms, J=0.01ms으로 평균·최대·지터 모두 유의미하게 개선(본문 §V-C 및 Fig.14).

## 한계

- 저자 명시 한계(논문 본문에서 직접 명시): GPU-resident Execution은 정상 상태에서 (1) 고정된 디바이스 메모리 레이아웃과 미리 할당된 버퍼, (2) 고정(잠금) GPU 클럭, (3) 정상 상태에서 호스트와의 상호작용 없음, (4) 워킹셋이 디바이스 메모리에 맞아야 함, (5) 동시 루프는 각 그래프별로 구성된 SM 파티션에 묶어야 함 — 이러한 전제들이 충족되어야 시간 예측성이 성립한다고 저자가 명시.
- 저자가 언급한 향후·미미한 범위(본문): 공유 L2 캐시·메모리 대역폭 등 디바이스 내부 간섭에 대해서는 현재 제어·분석을 다루지 않으며(향후 강한 자원 분할 필요), GPU-resident 작업 간 또는 GPU-resident↔호스트 작업 간의 예측 가능한 통신·동기화 설계는 향후 연구로 남음.
- 실험으로 드러나는 제약(본문 관찰 기반): 디바이스 내부 간섭은 완전히 제거되지 않음 — 동시 루프 실험에서 1→5루프 구간에서 꼬리·표준편차가 상승함(디바이스 측 영향). 또한 device-graph tail-launch 메커니즘은 CUDA의 조건부 노드를 지원하지 않아 일부 동적 라이브러리 기능과 호환성 제약이 있음(본문 §III-B2).
- 재현 관련 제약: 플랫폼별 고정 오버헤드와 NIC/FPGA/DOCA 통합 같은 하드웨어-의존적 세부 구현이 필요하며, 본 논문은 특정 NIC(ConnectX), HSB FPGA, DOCA GPUNetIO 및 Linux DRM 기반 디스플레이 통합에 의존하므로 타 하드웨어·드라이버 환경에서 동일한 성능·제약이 보장되지는 않음.

## 개발자 관점

- 설계·배포 전 요구조건을 고정하라: 정상 상태 성능·예측성 확보를 위해 디바이스 메모리 레이아웃을 정적(사전 할당)으로 구성하고 GPU 클럭을 고정(lock), 각 GPU-resident 루프에 대해 정적 SM 파티션을 할당하라(CUDA MPS 또는 전용 컨텍스트).
- 데이터 경로 구성: 센서→GPU 직접 경로를 위해 GPUDirect RDMA와 NIC 연계(예: ConnectX + HSB)를 준비하고, GPU측 폴링·재게시를 위해 DOCA GPUNetIO 같은 GPU-driven I/O API를 통합해야 정상 상태에서 호스트 깨우기 없이 동작한다.
- 애플리케이션 구조화: Holoscan의 GPU-resident API 스타일(Operator/Handler/Application)을 사용해 연산자 DAG를 캡처하고 WHILE 기반 CUDA Graph(기본)로 런칭하라. 연산자는 device-only 포트로 구현하고 모든 CUDA 호출을 캡처 스트림에 실행해야 한다.
- 오버로드·정책 명시: 센서 주기와 처리율 불일치(오버런/언더런) 시 동작(최신 프레임 드롭, 중복 억제, 출력 반복 등)을 데이터-준비 핸들러와 egress 경계에서 명시적으로 설계하라(프레임 큐잉을 GPU가 아닌 애플리케이션 정책으로 처리).
- 성능 분석·검증: 플랫폼별로 표(Table I 수준)의 반복 경계 오버헤드를 측정하고, 다중 루프·호스트 경합·디바이스 내부 간섭(캐시·메모리 대역폭) 영향도 계측하라. 특히 안전·실시간 도메인에서는 worst-case/꼬리(p99.9, max) 측정을 필수로 수행하라. 또한 DOCA/드라이버/디스플레이 통합은 벤더 API에 의존하므로 각 타깃에서의 드라이버 호환성·인증 요구사항을 확인하라.

**근거 범위:** 이 분석은 제출된 논문 PDF 본문(본문과 그림·표·수치)을 근거로 작성되었다. 본문에서 명시되지 않은 구현 세부나 내부 코드·드라이버의 비공개 동작은 기술하지 않았다. 일부 수치(예: 평균·최대·지터)는 본문 그림과 표에서 직접 인용했으며, 플랫폼별 미세 구현 차이(드라이버 버전·NIC/FPGA 구성 등)는 본문에서 구체화되어 있지 않아 재현 시 환경에 따라 달라질 수 있다.
