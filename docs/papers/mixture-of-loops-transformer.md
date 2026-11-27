# Mixture-of-Loops Transformer

- **게시일:** 2026-11-27
- **arXiv:** [2611.34923v1](http://arxiv.org/abs/2611.34923v1) · [PDF](https://arxiv.org/pdf/2611.34923v1)
- **저자:** Lianghui Zhu, Shijie Wang, Xinggang Wang, Jinze Bai, Bo Wang, Xiang Bai
- **분야:** cs.LG, cs.CL
- **선정 점수:** 4.27
- **선정 이유:** 최근성 0.7, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.0, 개발자 관심 1.0, 학술 신호 0.6, 오픈 웨이트·주요 연구조직 신호 0.0

[← 2026-11-27 목록으로 돌아가기](../daily/2026-11-27.html)

## 한 문장 요약

계층·루프 간에 계산된 키·값(KV)을 메모리로 주고받는 Mixture-of-Loops Attention(MoLA)을 도입하여 루프드(재사용) Transformer의 표현력은 유지하거나 개선하면서 추론·프리필 효율을 크게 개선하는 MoLT 계열(MoLT-R, MoLT-KV, U-MoLT)과 이를 위한 학습(루프 포싱)·추론(MoL, MoL-Hybrid) 절차를 제시한다.

## 해결하려는 문제

기존 루프드(무게 재사용) Transformer들은 반복 루프를 통해 표현력을 키우지만(같은 파라미터를 여러 번 사용) 그 대가로 추론 시에 루프를 순차적으로 모두 실행해야 해 비효율적이다. 표준적 해법인 루프 잔류(residual)만 전달하면 정보가 하나의 잔류 스트림으로 압축되어 레이어·루프를 거치며 표현 희석이 발생하고, 동일 위치의 이전 루프 출력에 대한 의존 때문에 추론을 병렬화하기 어렵다. 연구 질문은 ‘루프들 사이에 어떤 정보를 전달해야 표현력과 효율의 트레이드오프를 개선할 수 있는가?’이다.

## 핵심 기여

- Mixture-of-Loops Transformer(MoLT) 계열 제안: 루프 간에 키·값(KV)을 메모리로 전달하고, 각 레이어가 서로 다른 깊이와 루프의 KV를 한 번의 주의분포로 선택적으로 읽는 Mixture-of-Loops Attention(MoLA)을 도입하여 루프 간 및 깊이 간 재활용을 가능하게 함.
- 두 가지 루프 피드백 인터페이스 정식화: (a) MoLT-R(루프 잔류 + MoLA): 잔류 스트림을 유지하면서 같은 토큰 위치의 현재·이전 루프 로컬 KV를 직접 읽어 표현력을 보강, (b) MoLT-KV(루프 KV + MoLA): 각 루프는 임베딩으로 재시작하고 이전 루프의 strict-prefix 메모리 KV(j < t)와 현재 루프의 로컬 KV를 읽어 동일-위치 크로스루프 의존을 제거하여 단회 통과(MoL) 추론을 가능하게 함.
- 루프 포싱(loop forcing) 학습법과 MoL 단회-통과 디코딩 제안: 학습 중 모든 루프에 대해 예측을 감독(loop loss 부여)하여 병렬로 피드백 루프를 학습하고, 학습 루프 지평을 넘어 루프된 계산을 단회 통과로 확장하는 MoL 디코딩을 가능하게 함. 프리필-병렬성과 결합한 MoL-Hybrid 스케줄도 제시.
- U-shaped MoLT(U-MoLT) 제안: 루프 기반의 encoder(메모리 구축)를 분리하고 cross-only causal decoder(예측 읽기)를 밖에 두어 메모리 구성과 예측 읽기를 분리함으로써 사용되지 않는 decoder 반복을 생략해 효율/품질 균형을 달성.
- 광범위한 실험: 400B-token from-scratch 프리트레이닝(700M·1.5B dense, 3B MoE) 및 100B continued pretraining(Qwen3.5-0.8B-Base)에서 OLMo3 대비 검증 CE·퍼플렉시티·다운스트림 정확도 개선과 추론 지연 측정(특히 MoL-Hybrid로 non-looped와 유사한 지연 달성)을 보고.

## 접근 방법

* 논문 본문 기준 정리된 접근 방법은 다음과 같다.
* 핵심 아키텍처 요소
* Mixture-of-Loops Attention(MoLA): 각 레이어는 쿼리를 현재 입력에서 투사하고 하나의 소프트맥스 분포로 (1) 시퀀스 KV(다른 토큰의 KV, 루프 형식에 따라 현재루프 또는 이전루프 출력 기반 메모리)와 (2) 깊이(depth) KV(같은 위치의 이전 레이어 또는 이전 루프의 로컬 KV)를 결합해 읽음.
* Q/K에 대해 affine RMS QK 정규화와 RoPE를 사용.
* 피드백 인터페이스
* Loop residual (MoLT-R): 루프 출력(z_{r-1,t})을 다음 루프의 초기 잔류로 전달하면서, 현재 루프의 로컬 KV와 이전 루프의 같은-위치 로컬 KV를 depth KV로 읽게 함(표현력 지향).
* 단, 동일 위치의 이전 루프 출력에 의존하므로 추론 시 루프 순차 실행 필요.
* Loop KV (MoLT-KV): 각 루프는 임베딩(e(x_t))에서 재시작하고, 이전 루프의 정규화된 출력(z_{r-1,j})으로부터 j < t인 strict-prefix 메모리 KV를 읽음(시퀀스 KV).
* 현재 루프의 로컬 depth KV는 자신의 위치 포함.
* 임베딩 재시작+strict-prefix 마스크로 동일-위치 교차루프 의존을 제거하여 단회 통과 디코딩(MoL)을 가능하게 함.
* U-MoLT: 루프 KV 방식의 MoLT Encoder(LE 레이어, loop로 반복)와 루프 외부에 위치한 causal cross-only MoLT Decoder(LD 레이어)를 분리.
* Encoder는 메모리 구축과 피드백을 담당하고, Decoder는 정규화된 encoder 출력(z_r)을 각 레이어별로 투사한 decoder KV를 읽어 예측을 만듦.
* Decoder는 피드백 경로에 포함되지 않아 사용되지 않는 decoder 반복을 건너뛸 수 있음.
* 학습 및 추론 절차
* Loop forcing: 루프 KV 계열(MoLT-KV, U-MoLT)에서는 N 루프 각각에 대해 next-token 교차엔트로피 손실을 부여(가중치 α_r)하여 모든 루프가 병렬로 학습되도록 함.
* 이로써 Ft(xt, memory_prefix) 같은 피드백 맵을 루프 단위 병렬로 학습.
* 디코딩 스케줄
* Fixed-loop: 학습-사용과 같은 N 루프를 각 토큰마다 순차적으로 실행(비효율적).
* Mixture-of-Loops (MoL) 디코딩: 임베디드 재시작 및 strict-prefix 메모리에 기반해 새로운 토큰은 공유 스택을 한 번만 통과하여(단회 통과) 이전 토큰의 캐시된 메모리 KV를 읽고 자신의 메모리 KV를 추가.
* MoL-Hybrid: k-루프 병렬 프리필(1 혹은 2 루프)로 prompt를 초기화한 뒤, 이후 토큰은 MoL 단회-통과 업데이트를 사용하여 프리필 병렬성과 단회-통과 효율을 결합.
* 수치·구현 세부
* MoLA는 sequence KV와 depth KV를 연결(concatenate)해 단일 attention softmax로 처리하며, 저장된 depth keys는 writer의 정규화·RoPE을 보유해 reader가 이를 재사용.
* U-MoLT의 decoder KV는 정규화된 encoder 출력 z_r에서 레이어별로 투사하여 캐시하고, decoder는 이 캐시만 읽음으로써 decoder 생략(omission) 가능.
* 학습 세팅: S-size 실험(∼113M)에는 3B token(FineWeb), 스케일링 실험(700M/1.5B/3B MoE)은 400B token, Qwen 적응은 100B token 등.

## 주요 결과

- From-scratch 400B-token 프리트레이닝: U-MoLT는 OLMo3 대비 700M·1.5B dense 및 3B MoE 스케일에서 검증 퍼플렉시티/CE와 다운스트림 정확도 개선을 보임. 700M에서는 U-MoLT가 1.7× validation CE 토큰 효율성을 달성(즉 동일 성능을 더 적은 토큰으로 달성).
- 3B MoE(활성 파라미터 660M)에서 U-MoLT는 10-domain 평균 퍼플렉시티를 0.75 낮추고 10-task 평균 정확도를 2.1 퍼센트포인트 향상시킴(실험 세부 도메인·태스크는 본문 참조).
- Qwen3.5-0.8B-Base continued pretraining(100B tokens): U-MoLT 적응은 11개 도메인 모두에서 검증 CE를 낮추었고, 평균적으로 1.4× 토큰 효율성을 보고함.
- 추론 지연: S-size(약 113M)에서 4,096-token prefill과 64 decoding steps 조건하에 U-MoLT + MoL-Hybrid-2는 latency 996.6 ms로 non-looped OLMo3(1,000.6 ms)와 동급을 달성. (그림 2 및 본문 표 참조).
- S-size 구성의 ablation(Table 2): 단일 루프→2루프(잔류)로 바꾸면 CE가 3.318→3.299로 0.019 개선. U-MoLT의 일부 설정은 본 실험에서 최저 검증 CE(예: 3.273 등 표 내 값)를 달성하는 항목을 포함. (표에 다양한 placement·depth-source·projection 옵션별 CE, ∆파라미터, ∆FLOPs, step 시간 수치 있음).

## 한계

- 저자가 명시한 한계: (1) MoLT-KV(및 U-MoLT)의 단회-통과 디코딩은 학습 단계에서 도입한 loop forcing(모든 루프에 손실 부여)와 임베딩 재시작·strict-prefix 마스크에 의존한다. 특히 N=2(2-루프) 학습만으로는 Ft가 자기 자신 출력으로부터 재귀적으로 학습되는 것은 아니며, 따라서 학습과 추론의 메모리 소스(루프1에서 투사된 KV vs 재귀적 루프 출력으로부터 생성된 KV)가 달라지는 점을 교정하기 위해 여러 설계(공유 readout, 임베딩 재시작, 정규화 등)를 도입했다. 논문은 이 문제를 완화하는 설계와 실험적 증거를 제시하지만, 본질적으로 2-루프 학습이 긴 연쇄 재귀를 완전히 학습하는 것은 아님을 인정함.
- 저자가 지적한 계산·저장 비용: MoLT-KV는 추가 레이어별 메모리 KV 투사와 캐시를 필요로 하며(표에서 ∆Params와 ∆FLOPs 증가 항목 존재), fixed-loop 실행에서는 루프 수만큼의 prefix KV를 보관해야 하므로 메모리 증가가 발생할 수 있음(하지만 MoL/MoL-Hybrid로 완화 가능).
- 실험 범위에서 확인되는 제약(본문 기반 관찰): (a) 공개된 실험은 프리트레이닝·continued pretraining 및 벤치마크(언어모델 CE/PPL, 10개 태스크 정확도 등)에 집중되어 있으며, instruction-tuning/zero-shot 생성 품질·안전성·편향·탈동작(사례별 오류) 등 실제 배포 시 필요한 추가 평가는 제한적임. (b) 일부 구성(예: MoLT-KV dense placement)은 파라미터·FLOPs 증가(+수백만 파라미터, 표 참조)와 함께 업데이트 시간이 증가함(표의 step ms 참고). (c) 본문에서 루프-손실 가중치(αr) 설정은 성능/정렬에 민감하며, 가중치 트레이드오프에 따른 루프별 CE 변화가 관찰됨(본문 Table 3 언급).
- 검증 불완전성: 제공된 본문 텍스트에선 일부 상세한 하이퍼파라미터(정확한 αr 설정 값들, 학습률 스케줄 세부, MoE 학습 안정화 전략 세부 등) 및 전체 부록(appendix) 표·코드 경로 관련 세부가 본문 추출에서 완전하게 노출되지 않을 수 있어 재현 시 참조가 필요함.

## 개발자 관점

- 핵심 구현 요소: MoLA 커널(시퀀스 KV와 깊이 KV를 concat해 단일 attention softmax로 처리), 레이어별 KV 투사(로컬/메모리/디코더 KV), RoPE와 affine RMS QK 정규화의 일관된 적용이 필요하다.
- 루프 KV 인터페이스: embedding restart를 도입하고 이전 루프 출력으로부터 strict-prefix(j < t) 메모리 KV를 생성·캐시하는 구조를 구현해야 한다(여기서 strict-prefix 마스크로 j = t 제외).
- 학습(루프 포싱): 모든 루프에 대해 next-token 손실을 부여해 병렬로 루프를 학습하도록 구현(옵션으로 cross-loop 그래디언트 개방/분리). 루프 손실 가중치(αr)는 성능과 루프 간 정렬에 민감하므로 실험적으로 튜닝 필요하다.
- 추론 스케줄링: (1) fixed-loop(안전성 확인용), (2) MoL(빈 캐시부터 단회-통과), (3) MoL-Hybrid(k-루프 병렬 프리필 후 MoL) 스케줄을 구현·비교하라. U-MoLT의 경우 decoder omission(중간 루프에서 decoder 실행 건너뛰기)을 구현하면 프리필 계산량과 지연을 크게 줄일 수 있다.
- KV 저장·메모리 관리: MoL로 전환하면 persistent KV 저장을 루프별로 보관하지 않고 단일 prefix history로 유지 가능해 메모리 절감. 그러나 각 루프·레이어별 KV 투사와 프리필 시 추가 투사 비용이 발생하므로 메모리·연산-지연 트레이드오프를 계측해 적절한 LE/LD 분할(예: equal-split), sparse placement(대체 레이어에만 MoLA 적용) 등을 적용하라(본문 Table 2의 sparse vs dense 비교 참고). 더불어 Hkv·head dimension 등 KV 캐시 크기 전개를 미리 설계해야 함(식 11 등 참조).  
- 실험에서 보여준 실용 팁: U-MoLT + MoL-Hybrid-2는 S-size에서 non-looped와 유사한 지연을 내며, MoL-Hybrid-1은 프리필 지연 최소화에 유리하지만 첫 연속 예측 품질은 프리필 루프 깊이에 의존함.
- 재사용/이식성: Qwen3.5-0.8B-Base에 대한 continued pretraining 적응 사례가 있어 기존 모델에 대한 MoLT 적응 가능성이 있음(그러나 하이퍼파라미터·교육 예산 조정 필요).   
- 검증 권장 항목: (a) teacher-forced 연속 CE(여러 윈도우), (b) 프리필·디코딩 지연(다양한 프롬프트 길이/디코딩 스텝), (c) 루프 손실 가중치 스윕, (d) 메모리 사용량 및 쿼리·키 캐시 성능을 반드시 측정할 것. 
- 코드: 저자 공개 코드(https://github.com/hustvl/MoLT)를 참조해 비교적 복잡한 캐시·스케줄링 로직을 확인하라.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문 텍스트(본문, 그림 캡션, 표 일부 및 표시된 수치)를 기반으로 작성되었다. 본문에서 발췌된 표·그림 일부가 텍스트 추출 과정에서 잘리거나 축약되어 나타난 부분이 있으며(예: 부록의 모든 세부, 일부 표 행의 완전한 문맥), 따라서 세부 하이퍼파라미터(정밀한 αr 값, 전체 학습 스케줄 등)나 부록의 추가 실험 결과는 원문 PDF/저자 코드 저장소를 병행 확인할 것을 권장한다.
