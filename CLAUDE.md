# CLAUDE.md

바이브코딩 창업 사례 DB — 이 저장소에서 작업하는 Claude Code / 에이전트용 컨텍스트.
프로젝트 배경과 히스토리는 [HANDOFF.md](HANDOFF.md), 배포/파이프라인 상세는 [README.md](README.md) 참조.

## 1. 프로젝트

1인/소규모 팀이 AI 코딩 도구(Cursor, Claude Code, Lovable 등)로 만들고 수익화한
창업 사례를 모으는 정적 아카이브 사이트. GitHub Pages(`main` 브랜치 / root)로 배포.

- 저장소: `shokubase/micro-founders` (이름은 잠정 — 리브랜딩 가능성 있음)
- 빌드 단계 없는 순수 정적 HTML/CSS/JS. 프레임워크·번들러 도입 금지 (스키마 유지한 채 11ty 마이그레이션은 추후 검토)

## 2. 아키텍처 / 데이터 파이프라인

```
build_raw.py  →  data/raw_cases.json   (원본 사례 정의: cases 리스트에 dict 추가)
build_normalize.py → data/cases.json   (정규화 필드 부여 — 사이트가 실제로 읽는 파일)
build_feed.py  →  feed.xml             (RSS 생성 — cases.json 기반)
```

- `index.html` + `app.js` + `style.css` — 사이트 전체. `app.js`가 `data/cases.json`을 fetch해서 필터/검색/정렬/모달/신규 배지 렌더링
- 정규화 필드(`domain_category`, `team_size_bucket`, `founder_background`, `revenue_bucket` 등)는 `build_normalize.py`의 `ENRICH` 딕셔너리에서 사례 id별로 매핑
- 매출 표기 원칙: 카드/상세엔 원문 그대로, 내부 정렬/필터용으로만 연환산 USD 추정치 사용. 산출 근거는 `normalize_note`에 기록
- **환산 레이트는 여기 정의된 것만 쓴다:** 1 USD≈1,350원, 1 EUR≈1.08 USD, **1 USD≈150 JPY**
  (JPY는 2026-08-12 추가 — idm 후보에서 정의 없는 ≈147 레이트를 임의로 넣었다가 지적받았다.
  이 저장소가 €↔$로 겪은 사고와 같은 유형이다). **목록에 없는 통화가 나오면 레이트를 임의로
  만들지 말고 이 줄에 먼저 추가하라.**

## 3. 작업 규칙 (auto 모드)

이 저장소는 **auto 모드로 운영**한다. 저위험 정적 사이트이고 main 직접 배포 구조이므로:

1. **커밋/푸시 자동 진행.** 작업 단위가 완료되고 검증되면 `git commit` + `git push`까지
   사람에게 묻지 않고 진행한다. (order-sheet-generator와 달리 PR 게이트 없음)
2. **단, 파괴적 작업은 정지.** force push, hard reset, 데이터 파일 대량 삭제, 저장소
   설정 변경 중 되돌리기 어려운 것은 멈추고 확인받는다.
3. **데이터는 파이프라인으로만 수정.** `data/*.json`을 직접 편집하지 말 것 —
   `build_raw.py` / `build_normalize.py`를 수정하고 재실행해서 생성한다.
4. **cases.json이 바뀌면 feed.xml도 재생성.** `python3 build_feed.py` 실행 후 함께 커밋.
5. **커밋 전 검증.** `python3 build_raw.py && python3 build_normalize.py && python3 build_feed.py`가
   에러 없이 돌고, JSON이 유효한지 확인. 사이트 로직 변경 시 로컬에서 열어서 렌더링 확인
   (`python3 -m http.server`로 서빙 — file:// 로는 fetch가 막힘).
6. **푸시 = 배포.** main에 푸시하면 GitHub Pages에 그대로 반영된다는 걸 항상 의식할 것.

## 4. 사례 추가 절차

**신규 사례는 반드시 [RESEARCH_PIPELINE.md](RESEARCH_PIPELINE.md)의 4단계(발견→추출→검증→반영)를
거친다.** 2차 출처만으로 DB 직행 금지 — 1차 출처 검증 없이 반영된 사례에서 통화 단위·창업자
수·매출액 오류가 실증된 바 있다 (2026-08-10 재검증). 요약:

1. 후보를 `data/candidates/<id>.json`에 적재 (스키마는 RESEARCH_PIPELINE.md §3)
2. 검증 체크리스트 수행 후 `python3 check_candidates.py` 통과 확인
3. 사용자 승인된 후보만 `build_raw.py`의 `cases` 리스트에 dict 추가 (id는 kebab-case)
4. `build_normalize.py`의 `ENRICH`에 같은 id로 정규화 필드 추가 (`normalize_note`에 추정 근거 필수)
5. 파이프라인 3종 재실행 → `raw_cases.json`, `cases.json`, `feed.xml` 갱신, candidate는 `merged`로
6. 커밋 메시지에 추가된 사례 수와 출처 요약

## 5. 컨벤션

- 문서/UI 텍스트는 한국어 기본, 데이터 원문(영어 출처)은 원문 유지
- 신뢰도 필드(`confidence`): high/medium/low — 출처가 1차(창업자 본인 공개)면 high
- 날짜는 ISO-8601 (`ingested_at` 등)
- 코드 검색은 `rg` 사용 (`grep -r`, `find -exec` 금지 — 권한 게이트에 걸림)

## 6. Tooling conventions (auto-allow 레인 유지)

권한 시스템은 "임의의 하위 명령을 실행할 수 있거나, 인자를 숨기거나, read/write로
분류 불가한" 명령은 auto-allow 못 한다. 해결책은 settings를 넓히는 게 아니라
**명령 모양 자체를 피하는 것**:

- **파이프/체인 최소화.** `A | B`, `A && B`는 모든 구간이 allow에 맞아야 통과.
  JSON 필드 추출은 `python3 -c`로 파이프하지 말고 `gh api ... --jq '.field'` 사용.
- **`$(...)` 명령치환, `for`/`while` 루프 금지.** 분류 불가 → 무조건 프롬프트.
  반복 확인이 필요하면 한 번 실행하고 결과 보고 다시 실행.

> **2026-08-12 실측 — 게이트는 대부분 설정 문제가 아니라 명령 모양 문제였다.**
> 이 프로젝트 세션에서 거부된 Bash 호출 7건을 분류하니 **4건이 체인 또는 루프**였다
> (`git add -A && git commit ...`, `gh auth status && gh repo view ...`,
> `for i in 1 2 3...; do ... $(...)`). 나머지 3건은 `grep`·`git push origin main`처럼
> **이미 allow에 있는 명령**인데 사람이 의도적으로 거부한 것이라 설정으로 못 바꾼다.
> 즉 allow 목록을 넓혀서 얻을 게 거의 없었다 — 위 두 줄을 지키는 게 유일한 해법이다.
>
> 특히 `git add`는 **명시적 경로를 나열**하라. `-A`는 `.playwright-mcp/` 같은 도구
> 산출물까지 스테이징한다(2026-08-12에 실제로 발생해 `.gitignore`를 추가해야 했다).
> 커밋은 `git add <경로들>` → `git commit -m ... -m ...` → `git push`를 **각각 별도
> 호출**로 나눠라. 한 번에 묶으면 반드시 걸린다.
- **`python3 -c`는 실행문만.** 여러 줄 로직이 필요하면 스크래치패드에 임시 스크립트를
  Write하고 그 파일을 실행.
- **멀티라인 커밋 메시지도 게이트에 걸릴 수 있음.** 한 줄 `-m` 우선, 필요시 `-m` 두 번.
