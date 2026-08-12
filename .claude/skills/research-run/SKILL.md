---
name: research-run
description: 바이브코딩 창업 사례 정기 리서치 실행. 신규 사례 발견→추출→3렌즈 검증→후보 큐 적재까지 RESEARCH_PIPELINE.md 프로토콜대로 수행한다. "정기 리서치 돌려줘", "신규 사례 수집해줘" 요청 시 사용.
---

# 정기 리서치 실행 (/research-run)

RESEARCH_PIPELINE.md의 4단계를 에이전트 팬아웃으로 실행하는 표준 절차.
이 스킬은 **후보 큐 적재와 검증까지**만 자동으로 진행한다 — `build_raw.py` 반영(Stage 4)은
사용자 승인 후에만 한다 (CLAUDE.md §4).

## 사전 준비

1. `RESEARCH_PIPELINE.md`를 읽는다 (소스 레지스트리·쿼리 세트가 바뀌었을 수 있음)
2. 기존 데이터 로드: `data/cases.json`의 id·제품명·창업자명 목록,
   `data/candidates/`의 전체 후보 상태 (merged/rejected 포함 — 재발견 방지용)
3. 전회 실행 시점 확인: 후보 파일들의 `discovered_at` 최댓값 또는 git log

## Stage 1 — 발견 (source-hunter 병렬 팬아웃)

`source-hunter` 서브에이전트를 **각도별로 병렬** 투입한다. 각도끼리 결과를 공유하지
않는 것이 설계 의도다 (한 각도가 못 찾는 걸 다른 각도가 찾는다):

- Tier 1 EN: Indie Hackers + Starter Story + Acquire.com
- Tier 1 KR: disquiet.io
- Tier 2: 벤더 쇼케이스(Lovable/Cursor/Bolt/Base44) + 뉴스레터
- Tier 3 EN: 표준 쿼리 세트 1회전
- Tier 3 KR: 표준 쿼리 세트 1회전

각 에이전트에게 기존 id/제품명 목록과 전회 실행 시점을 프롬프트로 전달한다.
결과를 모아 제품명·창업자 기준으로 1차 dedup.

## Stage 2 — 추출

리드를 RESEARCH_PIPELINE.md §3 스키마로 구조화해 `data/candidates/<id>.json`
(status: `pending_verification`)으로 저장. 수치는 원문 표현 그대로.
`weak: true` 리드는 후보로 만들되 verification.notes에 약한 근거임을 명시.

## Stage 3 — 3렌즈 검증 (후보당 2/3 통과제)

후보마다 서브에이전트 3개를 투입한다 (후보 간 병렬 가능):

| 렌즈 | 에이전트 | 판정 대상 |
|---|---|---|
| 실존 | `case-verifier` (existence 렌즈 지정) | 창업자·제품이 실재하는가 |
| 수치 | `case-verifier` (figures 렌즈 지정) | 매출 주장의 원문 발화를 찾을 수 있는가 |
| 스코프·중복 | `scope-judge` | 아카이브에 들어올 자격이 있는가 |

판정 규칙:
- **3/3 pass** → status `verified`, confidence는 세 렌즈의 recommendation 중 최솟값
- **2/3 pass** → status `verified`로 하되 fail 렌즈의 반박 내용을 verification.notes에
  명시 (사람 승인 단계에서 보이게)
- **1/3 이하** → status `rejected`, 사유 기록 (재발견 방지를 위해 파일 보존)
- 단, **수치 렌즈 fail + 매출이 핵심 주장인 후보**는 2/3이어도 `rejected`
  (매출 주장이 무너지면 사례 가치가 없음)

세 에이전트의 `corrections`·`primary_sources_found`를 candidate의 verification
블록에 병합한다.

## Stage 3.5 — Completeness critic

일반 서브에이전트 1개에게 이번 실행 전체를 주고 묻는다:
"안 돌린 쿼리, 안 읽은 1차 출처, 미검증 주장, 스윕에서 빠진 소스가 있는가?"
발견된 공백은 이번에 메우거나, RESEARCH_PIPELINE.md 쿼리 세트 갱신 제안으로 기록.

## 마무리

1. `python3 check_candidates.py` 통과 확인 (실패 시 수정 후 재실행)
2. **실행 지표 산출.** 이번 실행에서 마주친 고유 리드(기존 사례로 판명된 것 포함)를
   한 줄에 하나씩 파일로 모아 실행:
   `python3 research_metrics.py <leads.txt> --as-of <실행 시작일>`
   `--as-of`를 빠뜨리면 방금 만든 후보가 인덱스에 있어 재포획률이 100%로 나온다.
   재포획률이 70%를 넘으면 그 층은 포화 — 보고에 "다음 실행은 새 층에서" 명시
3. 후보 큐 커밋 + 푸시 (auto 모드 — CLAUDE.md §3)
4. 사용자에게 보고: 신규 후보 N건 (verified M건 / rejected K건), 후보별 한 줄 요약과
   confidence, borderline 논거, **재포획률과 층 포화도**.
   **verified 후보의 Stage 4 반영은 승인을 기다린다**
5. 승인받은 후보만: `build_raw.py` + `build_normalize.py` ENRICH 반영 → 파이프라인
   3종 재실행 → candidate status `merged` → 커밋 메시지에 건수·출처 요약

## 비용 참고

Workflow 하네스(adversarial verify 패턴)로 검증 팬아웃을 돌리면 후보가 많을 때
효율적이다 — 단, 사용자가 명시적으로 요청("워크플로 써")한 경우에만 사용하고,
아니면 Agent 툴 병렬 호출로 진행한다.

**포화된 층에서는 팬아웃을 늘리지 마라.** 2026-08-11 실행에서 영어권 인디미디어
층 재포획률이 77%로 측정됐다 — 이 층에 에이전트를 더 투입하면 서로 같은 사례를
중복 발견해 토큰만 쓴다. 팬아웃 확대는 언어권을 늘린 다음, 언어권별로 붙일 때
의미가 있다 (RESEARCH_PIPELINE.md §4 참조).
