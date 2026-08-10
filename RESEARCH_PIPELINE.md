# 사례 수집 파이프라인

신규 사례가 DB(`build_raw.py`)에 들어가는 유일한 경로. 이 절차를 거치지 않은 사례 반영 금지.

> 왜 필요한가: 2026-08-10 재검증에서 2차 출처만 믿은 7건 중 통화 단위(€↔$), 창업자
> 수(1인↔3인), 매출액, 창업 연도가 틀린 사례가 다수 실증됐고 1건은 스코프 밖(순수
> 노코드)이었다. 2차 출처 → DB 직행은 구조적으로 차단한다.

## 0. 원칙

1. **1차 출처 없이 DB 반영 금지.** 신규 사례는 Stage 3 검증을 통과해 medium 이상을
   받아야 반영. low는 후보 큐에서 대기만 가능.
2. **수치는 원문 통화·원문 표현 그대로.** 환산(연환산 USD)은 `build_normalize.py`에서만,
   근거는 `normalize_note`에 필수 기록.
3. **애그리게이터 수치 경계.** GetLatka·Starter Story 헤더 수치 등이 창업자 본인 발언과
   모순되면 본인 발언 채택, 모순 사실을 note에 기록.
4. **스코프 체크.** AI 코딩 도구(2023~ Cursor, Claude Code, Lovable, Bolt, Kiro 등)로
   만든 사례만. 순수 노코드 구시대(pre-2023) 사례는 제외 (선례: flexiple 제거).

## 1. 소스 레지스트리

### Tier 1 — 구조화된 사례 DB (정기 순회, 메인 파이프)
| 소스 | URL | 비고 |
|---|---|---|
| Indie Hackers | indiehackers.com/products, /interviews | 창업자 자진신고 매출 = 1차 출처 |
| Starter Story | starterstory.com | 케이스 스터디, 일부 페이월. 헤더 수치 주의 |
| Acquire.com | acquire.com | exit 사례 (매출/이익 명시 리스팅) |
| disquiet.io | disquiet.io | KR 메이커 수익 인증/회고 = 1차 출처 |

### Tier 2 — 반구조화 (RSS/신규 글 감시)
| 소스 | 비고 |
|---|---|
| Lovable customer stories / blog | 마케팅 → confidence 상한 medium, 툴 필드 확정용 |
| Cursor / Bolt / Base44 블로그 | 〃 |
| 언섹시비즈니스 (maily.so/unsexybusinesskr) | KR 큐레이션 뉴스레터 |
| GPTers, EO플래닛(eopla.net) | KR 커뮤니티 — 본인 글이면 1차 출처 |
| Trends.vc, Failory | EN 큐레이션 |

### Tier 3 — 키워드 발견 (보조)
표준 쿼리 세트 (분기마다 갱신):
- EN: `"built with Lovable" ARR|MRR|revenue` / `"vibe coding" revenue|acquired` /
  `solo founder AI app MRR` / `"Claude Code" built revenue` / `indie hacker AI acquired`
- KR: `바이브코딩 수익|매출` / `1인 개발 매출` / `AI 코딩 창업` /
  `Cursor로 만든 서비스` / `사이드프로젝트 수익화 AI`

검색에 걸린 글은 그 자체를 출처로 쓰지 말고 **발견 신호**로만 취급 → Stage 3에서
1차 출처를 역추적한다.

## 2. 4단계 절차

```
Stage 1 발견   Tier 1-3 순회 → 신규 후보 식별 (기존 id/제품명과 중복 체크)
Stage 2 추출   후보 스키마(§3)로 구조화 → data/candidates/<id>.json (status: pending_verification)
Stage 3 검증   아래 체크리스트 수행 → verification 블록 기록 (status: verified)
Stage 4 반영   사람 승인 → build_raw.py + build_normalize.py ENRICH 반영 →
               파이프라인 재실행 → candidate status: merged → 커밋
```

### Stage 3 검증 — 3렌즈 심사, 2/3 통과제

후보마다 서로 다른 관점의 심사자 3개를 독립 투입한다 (에이전트 정의:
`.claude/agents/`). 심사자는 주장을 **반박하려 시도**하고, 반박 실패 시에만
통과시킨다. 불확실하면 기각이 기본값.

| 렌즈 | 심사자 | 판정 대상 |
|---|---|---|
| 실존 | `case-verifier` (existence) | 창업자 실명·본인 계정, 제품 실존(사이트/앱스토어), 팀·지역 교차 확인 |
| 수치 | `case-verifier` (figures) | 매출 주장의 원문 발화(누가·어디서·언제·원문 통화), 애그리게이터 모순 스크리닝 |
| 스코프·중복 | `scope-judge` | AI 코딩 툴(2023~) 사용, 팀 규모, 수익화 근거, 기존 사례와 중복 |

판정 규칙:
- **3/3 pass** → `verified` (confidence = 세 렌즈 recommendation의 최솟값)
- **2/3 pass** → `verified`, 단 fail 렌즈의 반박 내용을 notes에 명시
- **1/3 이하** → `rejected` (사유 보존)
- 예외: **수치 렌즈 fail + 매출이 핵심 주장**인 후보는 2/3이어도 `rejected`

### Stage 3.5 — Completeness critic

실행 말미에 별도 에이전트 1개가 전체 실행을 심사: 안 돌린 쿼리, 안 읽은 1차 출처,
미검증 주장, 빠진 소스. 발견된 공백은 즉시 메우거나 쿼리 세트 갱신 제안으로 기록.

## 3. 후보 큐 (`data/candidates/`)

파일당 후보 1건, 파일명 `<id>.json` (id는 kebab-case). 스키마:

```json
{
  "id": "example-product",
  "status": "pending_verification | verified | approved | rejected | merged",
  "discovered_at": "2026-08-10",
  "discovery_source": "발견 경로 URL (Tier 1-3 중 어디서)",
  "case": { "build_raw.py의 dict와 동일한 필드": "..." },
  "verification": {
    "verified_at": null,
    "checklist_passed": [],
    "primary_sources": [],
    "corrections": [],
    "excluded_figures": [],
    "confidence_recommendation": null,
    "notes": ""
  }
}
```

- 검증·중복 검사: `python3 check_candidates.py` (커밋 전 필수)
- `rejected` 파일은 사유를 `verification.notes`에 남기고 보존 (같은 사례 재발견 방지)

## 4. 정기 실행 루틴

표준 실행 절차는 **`/research-run` 스킬**(`.claude/skills/research-run/SKILL.md`)로
고정되어 있다 — 어느 세션에서든 스킬 호출 한 번으로 동일 프로토콜이 실행된다. 개요:

1. Tier 1-2 소스별 신규 글 확인 + Tier 3 표준 쿼리 1회전
   (`source-hunter` 각도별 병렬 팬아웃 — 각도 간 결과 비공유가 설계 의도)
2. 신규 후보 → Stage 2 추출 → Stage 3 3렌즈 검증 → Stage 3.5 completeness critic
3. `check_candidates.py` 통과 확인 → 후보 큐 커밋
4. verified 후보는 사용자 승인 요청 → 승인분만 Stage 4 반영
5. 커밋 메시지에 신규/검증/반영 건수 요약

검증 팬아웃은 후보가 많은 실행에서 Workflow 하네스(adversarial verify 패턴)로
확장 가능 — 사용자 명시 요청 시에만.
