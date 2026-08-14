# The Role Specialization Model (RSM): Coordinating LLM-Based Tools in Agentic Software Development - An Exploratory Case Study

- **게시일:** 2026-08-14
- **arXiv:** [2608.12311v1](http://arxiv.org/abs/2608.12311v1) · [PDF](https://arxiv.org/pdf/2608.12311v1)
- **저자:** Carlos Alberto Fernández-y-Fernández, Jorge R. Aguilar-Cisneros
- **분야:** cs.SE
- **선정 점수:** 5.48
- **선정 이유:** 최근성 0.8, 인용 영향 0.0 (인용 0회), 저자 영향 0.0 (최고 h-index 0), AI 주제 적합성 2.4, 개발자 관심 0.5, 학술 신호 0.3, 오픈 웨이트·주요 연구조직 신호 1.5

[← 2026-08-14 목록으로 돌아가기](../daily/2026-08-14.html)

## 한 문장 요약

LLM 기반 도구들을 역할 분담(Architect/Analyst/Specialist)으로 조정하는 Role Specialization Model(RSM)을 제안하고, Antigravity, Gemini CLI, Qwen Code 세 도구로 Python 데스크탑 기후 데이터 시각화 애플리케이션을 단계별로 개발하면서 RSM의 실행, 편차, 프롬프트 강건화 기법 및 ISO/IEC 25010 기반 정성 평가를 문서화한 탐색적 사례연구.

## 해결하려는 문제

LLM이 개발 워크플로에 통합됨에 따라 여러 에이전트·도구를 동시에 사용하는 ‘Agentic Software Engineering(SE 3.0)’ 환경에서 각 도구의 상이한 능력을 어떻게 조직·조정할지에 대한 실무적 방법론이 부족하다. 기존 단일 에이전트 또는 완전 자동화된 멀티에이전트 연구와 달리, 상이한 실행 모드(클라우드 agentic IDE, CLI, 로컬 모델)를 가진 상용·오픈소스 도구들을 인간 오케스트레이터 하에 역할별로 분담할 때 발생하는 역할 침범, 문맥 전환 비용, 제약-지시 밀도 증가에 따른 성능 저하 및 출력 무결성 문제를 해결하거나 특성화할 필요가 있다. 연구질문은 (RQ1) RSM으로 어떻게 조정 가능한가, (RQ2) 계획된 역할 분배에서 어떤 편차가 왜 발생하는가, (RQ3) 산출물의 품질을 ISO/IEC 25010로 어떻게 평가할 수 있는가이다.

## 핵심 기여

- Role Specialization Model(RSM): 역할(Architect/Analyst/Specialist)에 근거한 다중 LLM-도구 조정 프레임워크 제안
- RSM을 적용한 전체 개발 워크플로 문서화 및 실행 중 관찰된 편차(특히 Gemini CLI가 Qwen Code의 역할을 대신한 사례) 기록
- 프롬프트 강건화(prompt-hardening) 기법(명시적 부정 제약 등) 적용 사례와 실무적 권고사항 제시
- ISO/IEC 25010(2011) 품질 모델에 대한 정성적 전문가 평가를 통해 결과 제품의 품질 특성(기능적 적합성·유지보수성·상호작용성 등) 보고
- 위협-타당성 분석 및 RSM의 이론적 검증(Separation-of-Concerns, 멀티에이전트 역할분화, SE 3.0 정합성)

## 접근 방법

* 단일 사례 탐색적 사례연구(한 개발자, 하나의 프로젝트)로 수행되었으며 관찰과 체계적 문서화(프롬프트, 에이전트 상호작용, 출력, 편차, 테스트 결과)를 통해 정성적 패턴 매칭 방식으로 분석했다.
* 사용 도구는 Antigravity(agentic IDE, 본문에서는 Gemini 백엔드로 설정됨), Gemini CLI(터미널 기반), Qwen Code(로컬 Ollama 실행)이고 RSM은 도구별 책임 영역을 분리하여 적용했다.
* 실험 프로젝트는 Python/Tkinter+Pandas+Matplotlib 기반의 'Climate Data Visualizer'로 설계·개발되었고, 개발은 5단계(초기 설계-데이터 생성·분석-검증·테스트-고급 상호작용-문서화)로 진행되었다.
* 품질 평가는 저자(제1저자)의 전문가 정성평가로 ISO/IEC 25010의 각 특성을 운영화하여 High/Moderate로 표기했다.
* 주요 실험적 절차로는 제로샷 요구사항 제시(Agent에게 자연어로 전체 프로젝트 지시), Gemini CLI를 통한 데이터 생성(프롬프트 강건화 반복), 아키텍처 감사 및 리팩토링 제안, Qwen Code로 검증 모듈과 단위테스트 생성, Antigravity로 인터랙티브 기능 확장 등이 포함된다.

## 주요 결과

- 도구별 관찰된 역할 적합성: Antigravity는 초기 다파일 생성 및 인터페이스 구현(Phase 1)에서 강점, Gemini CLI는 데이터 생성(최종 weather_data.csv), 아키텍처 분석·문서 통합(Phase 2·5)에서 강점, Qwen Code는 validators.py와 10개의 단위테스트(TestValidators, TestCSVValidation, TestDataModelBasic 등)를 생성하는 Specialist 역할을 수행함.
- 프롬프트 강건화: CSV 100레코드 생성 시 최초 2회 실패(에이전트가 터미널에서 사용 불가능한 내부 툴 호출 시도), 3번째 프롬프트에서 'Do NOT run commands / Do NOT use tools' 등의 명시적 부정 제약을 포함해 성공적으로 plain-text 출력을 리다이렉션하여 파일 생성(성공 사례 기록).
- 역할 편차: 계획상 Qwen Code에 할당된 리팩토링(아키텍처 개선) 작업을 Gemini CLI가 자발적으로 수행함 — 원인으로는 범위 경계 부재, 도구간 기능 중복, 문맥 전환의 인지 비용이 결합됨(본문 분석).
- ISO/IEC 25010(2011) 정성평가 결과(저자 운영화 기준): 기능 적합성(Completeness) High; 성능 효율성(Time behaviour) 개선(리팩토링 후 Figure/Canvas 재사용으로 데이터 리로드 지연 감소) 보고; 신뢰성(Faultlessness) Moderate(가상환경(venv) 손상 등 런타임 환경 취약성 관찰); 유지보수성(Modularity/Analysability) High(데이터 모델 분리·타입힌트 도입); 상호작용성(Interaction capability) High; 유연성(Flexibility) High(run.sh의 환경 감지·폴백 설치 지원).
- 기타 정성 관찰: 초기 Antigravity 산출물은 작동하는 단일 클래스(ClimateVisualizerApp)로 단일 책임 위반(모놀리식) 관찰 → DataModel 분리 권고 및 구현; 전체 개발 과정에서 인간 검증과 명시적 문맥 전달이 여러 차례 필요했음.

## 한계

- 저자 명시 한계(논문에서 보고된 사항): 단일 사례·단일 개발자·단일(부분적) 도구셋으로 수행되어 외적 타당성 제한, 내부 타당성 위험(관찰자 편향: 개발자=연구자), 구성 타당성(ISO/IEC 25010 평가는 정성적 전문가 평가에 의존), 신뢰성 문제(실행이 한 번만 수행되어 확률적 LLM 출력 재현 불확실).
- 본문에서 확인되는 추가 제약: 사용된 도구 중 Antigravity와 Gemini CLI가 동일/유사한 Gemini 계열 모델을 사용해(논문 본문에서 모델 버전 표기가 섹션마다 상이함) 집단의 인지 다양성(cognitive diversity)이 낮아 역할 중복을 촉진했을 가능성, 정량적 메트릭(예: 사이클로매틱 복잡도, 정확한 응답시간 수치, 자동화된 신뢰성 측정)은 제공되지 않음.
- 실험 설계상 제약: 단일 반복·확률적 모델 거동, 프롬프트·세션 버전 관리와 재현 프로토콜 미포함으로 동일 조건 재실행 시 결과 불변을 보장할 수 없음.

## 개발자 관점

- 역할 분담(Architect/Analyst/Specialist) 설계 시 명시적 범위 경계(phase 경계, 책임 인터페이스)를 문서화하여 도구의 자발적 관여를 억제하거나 허용 조건을 정의해야 함.
- 프롬프트 강건화: 시스템 도구 접근 권한이 있거나 터미널 출력을 기대하는 경우 명시적 부정 제약(Do NOT run commands 등)을 포함한 반복 보강이 필요하며, '프롬프트를 코드로(version control)' 취급해 Git에 버전 관리할 것을 권장함.
- 문맥 관리 비용 절감 방안: 도구 간 전환 시 프로젝트 파일·문맥을 자동으로 동기화하는 파이프라인(artifact exchange) 마련, 또는 강력한 모델 라우팅 정책으로 중복 작업 방지(작업 유형별 모델 라우팅) 권장.
- 품질 보증: 인간 오케스트레이터에 의한 검증은 필수이며, RSM에 LLM-as-a-Judge(평가자 에이전트)를 추가하여 감사 부담을 경감할 수 있으나 평가자 에이전트의 편향(positional, verbosity, self-affirmation) 완화용 루브릭 설계 및 캘리브레이션이 필요하다.
- 보안·운영: 에이전트에게 파일시스템·터미널 접근을 허용할 경우 샌드박싱과 자원·권한 제약, 외부 데이터(예: CSV)에 숨겨진 프롬프트 주입 위험을 방지할 검증체계 필요. 또한 가상환경 손상 같은 런타임 취약성을 고려한 복구 스크립트(run.sh 같은 폴백) 도입 권장.

**근거 범위:** 이 분석은 제공된 논문 PDF 본문(페이지 1–28)과 부록의 내용을 근거로 작성되었다. 본문에서 보고된 정성·사례 기반 결과(예: ISO/IEC 25010 평가는 저자에 의한 정성적 전문가 평가)와 실험적 숫자(예: 초기 샘플 데이터 31건, 생성 대상 CSV 100행, Qwen Code가 생성한 10개의 단위테스트 등)는 PDF 본문에서 직접 확인한 수치만 사용했다. 한편 도구 백엔드 모델 버전에 관한 표기는 본문 내에서 일관되지 않음(초록과 도구 설명 일부에서 서로 다른 Gemini 버전 표기)으로 본문 도구 설정 관련 세부는 본문 서술을 따랐으나 해당 부분은 원문에서 불일치가 있음을 주의해야 한다.
