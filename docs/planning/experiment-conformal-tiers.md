# 실험 계획: conformal 구간 기반 경보 등급 검증

> 상태: 데이터 수집 대기 (집에서 다운로드 후 진행)

## 목적
80% / 95% / 99% conformal 구간으로 만든 경보 등급(정상·주의·경고·위험)이 실제 데이터에서
1. coverage가 명목 수준과 맞는지
2. 등급별 펀드 비율이 실무에서 감당 가능한 수준인지
3. 기준을 바꾸면(예: 90/97.5/99.5%) 어떻게 달라지는지
확인한다.

## 데이터
Washington State Investment Board 분기 사모펀드 보고서, 2020 Q1 ~ 2025 Q1 (21개 분기)
URL 패턴: `https://www.sib.wa.gov/docs/reports/quarterly/ir{MMDD}{YY}.pdf`

## 방법
- 펀드별 분기 납입 = 누적 납입 차분, 분기 분배 = 누적 분배 차분
- 분기 수익률 = (이번 평가액 + 분기 분배 − 분기 납입) ÷ 지난 평가액 − 1
- 시장 기준 = 같은 분기 전체(또는 같은 전략) 펀드 수익률 중앙값
- 잔차 = 펀드 수익률 − 시장 기준
- 과거 분기 잔차로 split conformal 구간 → 다음 분기에 적용 (rolling)
- 비교: 고정 split conformal vs adaptive conformal inference

## 확인할 지표
- 구간별 실제 coverage (전체, 분기별, 2020·2022 충격 구간)
- 등급별 펀드 비율, 분기당 경보 건수
- 2분기 연속 "주의" → "경고" 상향 규칙 적용 시 건수
