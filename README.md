# KIC AI Agent Competition 2026

> 데이콘 × 한국투자공사(KIC) **「국부펀드 KIC, AI 에이전트 공모전」** 참가 저장소
> 주제: 투자 및 금융 업무 혁신을 위한 AI Agent 기획 및 MVP 구현

| 항목 | 내용 |
|---|---|
| 주최 | 한국투자공사(KIC) · DACON |
| 대회 페이지 | https://daker.ai/public/hackathons/kic-ai-agent-competition |
| 참가 형태 | 개인 참가 (박채원 / [@Chaewon-Park-STUDY](https://github.com/Chaewon-Park-STUDY)) |
| 서비스명 | (TBD) |

## Timeline

| 단계 | 마감 | 제출물 |
|---|---|---|
| 예선 | 2026-11-12 (목) 10:00 | AI Agent 기획서 PDF (양식 기반, 10p 이내) |
| 본선 | 2026-12-22 (화) 10:00 | 프로토타입 데모 URL · 발표자료 PDF (10분) · GitHub 실행 코드 · (선택) 시연영상 |

## 1. Summary
| 항목 | 내용 |
|---|---|
| 문제·사용자 | |
| Agent 제안 | |
| 데이터·기술 | |
| 기대효과 | |

## 2. Problem
<!-- 해결하려는 투자·금융 업무 문제, 현행 방식의 한계, 주요 사용자·업무 상황·활용 시나리오 -->

## 3. Service & Differentiation
<!-- 서비스 개요, 핵심 기능, 사용자 입력 → Agent 수행 → 최종 결과물 흐름 -->

## 4. Agent Role & Workflow
<!-- 역할·목표, 작업 계획, 정보 탐색·분석, 결과 생성·검증, 자율 판단 범위와 종료 조건 -->

```
User request
   └─▶ Planner / Orchestrator
         ├─▶ Retrieval (공시·뉴스·시장 데이터)
         ├─▶ Analysis (리스크·지표 계산)
         ├─▶ Report generation
         └─▶ Verification (근거·출처 검증) ──▶ 종료 조건 충족 시 출력
```

## 5. AI Stack · Tool/API
<!-- 모델, Agent framework, RAG·Memory, Tool/API별 역할·입출력·호출 조건,
     환각 대응·출처 표시·재시도·예외 처리 -->

| Tool / API | 역할 | Input | Output | 호출 조건 |
|---|---|---|---|---|
| | | | | |

## 6. Data Plan
<!-- 데이터·출처, 수집·갱신·전처리 방법, 활용 목적 -->

| 데이터 | 출처 | 수집·갱신 방식 | 활용 목적 | 이용 조건 |
|---|---|---|---|---|
| | | | | |

## 7. MVP Plan
<!-- 본선 기간 구현 범위, 기술 스택, 단계별 일정·완료 기준, 데모 시나리오, 리스크와 대응 -->

## 8. Expected Impact & Scalability
<!-- 시간·비용·품질·신뢰성 개선, 확장 가능성, 운영 적용 경로 -->

## Dev Log
개발 과정은 [`docs/devlog/`](docs/devlog/)에 날짜별로 기록합니다.

| 날짜 | 내용 |
|---|---|
| 2026-10-27 | 저장소 생성, 대회 규칙·기획서 양식 정리 |

## Repository Structure

```
.
├── docs/
│   ├── proposal/     # 예선 기획서 (pptx 원본, 제출 PDF)
│   ├── final/        # 본선 발표자료 PDF
│   └── devlog/       # 날짜별 개발 기록 (YYYY-MM-DD.md)
├── src/
│   ├── agent/        # orchestrator, prompts, tool definitions
│   ├── tools/        # 개별 tool 구현 (API, 데이터 처리)
│   └── app/          # MVP UI / API 서버
├── data/             # 샘플 데이터 (원본·대용량은 커밋 X)
├── notebooks/        # 탐색·실험
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Getting Started
<!-- 본선 제출 시 필수: 실행 방법, 사용 기술, 데모 URL -->

```bash
git clone https://github.com/Chaewon-Park-STUDY/KIC-AI-Agent-2026.git
cd KIC-AI-Agent-2026
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env          # API key 입력 (macOS/Linux: cp)
```

## Sources & AI Usage
대회 규칙상 사용한 모든 외부 자원의 출처와 이용 조건을 기록해야 합니다 (기획서 ⑧ 부록과 동기화).

| 구분 | 이름 | 출처 / 링크 | 이용 조건 / 라이선스 | 활용 범위 |
|---|---|---|---|---|
| 데이터 | | | | |
| 모델 / API | | | | |
| 오픈소스 | | | | |
| 생성형 AI·개발 도구 | | | | |

## Secrets Policy
- API key는 `.env`에만 저장하고 코드에서는 `os.getenv()`로 읽습니다. 코드·노트북·문서에 직접 쓰지 않습니다.
- `.env`, `*.key`, `credentials*.json` 등은 `.gitignore`로 제외합니다. 필요한 변수 이름은 `.env.example`에 둡니다.
- 데모 배포 시 key는 배포 플랫폼의 환경변수/Secrets 설정에 등록합니다.
- 커밋 전 `git diff --staged`로 key 포함 여부를 확인합니다. 노출 시 즉시 해당 key를 폐기·재발급합니다.
