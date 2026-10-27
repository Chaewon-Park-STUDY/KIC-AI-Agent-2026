# KIC AI Agent Competition 2026

> 데이콘 × 한국투자공사(KIC) **「국부펀드 KIC, AI 에이전트 공모전」** 참가 저장소
> 주제: 투자 및 금융 업무 혁신을 위한 AI Agent 기획 및 MVP 구현

| 항목 | 내용 |
|---|---|
| 주최 | 한국투자공사(KIC) · DACON |
| 접수 마감 | 2026-11-12 (목) 10:00 KST |
| 대회 페이지 | https://daker.ai/public/hackathons/kic-ai-agent-competition |
| 팀 구성 | (팀명 / 인원) |

## 1. Problem
<!-- KIC의 어떤 투자·금융 업무를 겨냥하는지, 현재 pain point는 무엇인지 -->

## 2. Agent Overview
<!-- 에이전트가 하는 일, 입력 → 처리 → 출력 흐름 -->

```
User request
   └─▶ Orchestrator
         ├─▶ Tool A (e.g. 데이터 수집)
         ├─▶ Tool B (e.g. 분석/리스크 평가)
         └─▶ Tool C (e.g. 리포트 생성)
```

## 3. Repository Structure

```
.
├── src/
│   ├── agent/        # orchestrator, prompts, tool definitions
│   ├── tools/        # 개별 tool 구현 (API, 데이터 처리 등)
│   └── app/          # MVP UI / API 서버
├── data/             # 샘플 데이터 (원본·대용량은 커밋 X)
├── notebooks/        # 탐색·실험
├── docs/             # 기획서, 발표자료, 다이어그램
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## 4. Getting Started

```bash
git clone https://github.com/Chaewon-Park-STUDY/KIC-AI-Agent-2026.git
cd KIC-AI-Agent-2026
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # API key 입력
```

## 5. Evaluation / Demo
<!-- 데모 영상, 스크린샷, 성능·검증 방법 -->

## 6. Timeline

- [ ] 아이디어 확정 및 기획서 초안
- [ ] 핵심 tool 구현
- [ ] Agent orchestration 및 MVP UI
- [ ] 검증·데모 영상
- [ ] 최종 제출 (~11/12 10:00)
