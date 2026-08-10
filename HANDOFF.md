# 핸드오프: 바이브코딩 창업 사례 DB 프로젝트

Cowork 세션에서 여기까지 진행한 내용을 요약. 클로드 코드에서 이어서 개발하면 됨.

## 프로젝트 목적

바이브코딩/에이전틱 코딩 시대(2023~2026)에 1인 또는 소규모 팀이 AI 코딩 도구(Cursor, Claude Code, Lovable, Bolt, Base44 등)로 만들고 수익화한 창업 사례를 모으는 아카이브 사이트. 다음을 파악하는 게 목적:
- 어떤 분야에서 성과를 내는지
- 어디까지 규모를 키울 수 있는지 (매출/exit)
- 어떻게 실제로 돈을 버는지 (BM)
- 창업자들은 어떤 사람들인지 (배경)

## 저장소 / 이름

- GitHub: `shokubase/micro-founders` (이미 빈 저장소로 생성됨)
- **이름은 잠정적**임 — 세션에서 20개 넘는 후보(microfounders, atomicmakers, foundedai, bonsai, daruma, tanuki, sango, fusafounders 등)를 검토했는데 다들 어딘가 브랜드 충돌이 있었고, "일단 MVP부터 만들고 나중에 정하자"는 결론으로 `micro-founders`를 임시로 선택함. 나중에 리브랜딩 가능성 있음 (저장소 rename은 쉬움).
- 도메인/최종 브랜드명은 아직 미정 상태로 남겨둠

## 지금까지 만든 것 (이 폴더 전체)

- `index.html`, `style.css`, `app.js` — 빌드 단계 없는 순수 정적 사이트. 필터(도메인/팀규모/매출구간/창업자배경) + 검색 + 정렬(매출순/최신순/신뢰도순) + 카드 클릭 시 상세 모달(출처 링크 포함) + 방문 시 "새 사례 N건" 배지(localStorage 기반)
- `data/raw_cases.json` — 4개 소스 클러스터(Indie Hackers/Starter Story, 뉴스/M&A, 한국어 소스, X/커뮤니티)를 병렬 리서치해서 모은 36건의 원본 사례 (중복 제거 완료)
- `data/cases.json` — raw_cases.json에 정규화 필드를 추가한 최종본. **사이트가 실제로 읽는 파일**
- `build_raw.py` — 원본 사례 정의 (`cases` 리스트에 dict 추가하는 방식)
- `build_normalize.py` — 정규화 로직. `ENRICH` 딕셔너리에 사례 id별로 아래 필드를 매핑:
  - `domain_category`, `team_size_bucket`(solo/2-3/4+/unknown), `founder_background`(developer/non-developer/mixed/unknown), `founder_experience`(first-time/serial/unknown/mixed)
  - `revenue_annual_usd_est` (연매출 추정 USD), `revenue_bucket`(<100K/100K-1M/1M-10M/10M+/unknown, 자동계산), `exit_value_usd`/`funding_usd`/`valuation_usd`(해당시)
  - `normalize_note` — 추정 산출 근거 설명 (환산 기준: 1 USD≈1,350원, 1 EUR≈1.08달러)
- `build_feed.py` — `cases.json` → `feed.xml`(RSS) 생성. **`SITE_URL` 변수가 아직 placeholder임 — 실제 GitHub Pages URL 확정되면 반드시 업데이트하고 재실행할 것**
- `README.md` — 배포 방법, 새 사례 추가 파이프라인, 알림 설계 등 상세 문서

## 사용자가 확정한 설계 결정들

1. **매출 표기**: 카드/상세엔 원문 그대로("MRR $30K" 등) 보여주고, 내부적으로만 연환산 USD 추정치를 정렬/필터용으로 사용. 산출 근거는 각 사례의 `normalize_note`에 남김
2. **사이트 기술**: 빌드 단계 없는 순수 정적 HTML/JS로 우선 시작 (나중에 사례 많아지고 개별 URL/SEO 필요해지면 11ty 등으로 마이그레이션 검토 — 데이터 스키마는 그대로 재사용 가능하다고 안내함)
3. **MVP 필터 축 4개**: 도메인/비즈니스 카테고리, 팀 규모, 매출 구간, 창업자 배경
4. **알림**: 사이트 배지(구현완료) + RSS(구현완료). 이메일은 RSS→이메일 브릿지(Blogtrottr 등)로 우회 가능. 카카오톡은 비즈니스 API 필요해서 보류
5. **사례 수집 방식**: 자동 스크래핑(정기 리서치, LLM 추출) + 수동 큐레이션 두 트랙 병행. 순수 스크래핑만으론 비정형 소스(뉴스/블로그/트윗) 파싱이 안 돼서 LLM 추출이 필수라는 걸 파일럿으로 확인함

## 막혔던 부분 (왜 클로드 코드로 옮기는지)

Cowork 클라우드 세션에는 GitHub 접근을 "미리 승인된 저장소 목록"으로만 제한하는 프록시가 있어서, 유효한 Personal Access Token을 줘도 이 세션 안에서는 `shokubase/micro-founders`에 git push/API 호출이 전부 차단됨. 로컬 클로드 코드는 이 제약이 없어서 정상적으로 push 가능.

## 다음에 할 일 (우선순위 순)

1. 로컬에서 git 세팅 후 이 폴더를 `shokubase/micro-founders`에 push
2. GitHub 저장소 Settings → Pages에서 main 브랜치 / root로 Pages 활성화, 실제 URL 확인
3. `build_feed.py`의 `SITE_URL`을 실제 URL로 바꾸고 `python3 build_feed.py` 재실행 후 재커밋
4. (선택) 신뢰도 `low`로 표시된 사례들 원출처 재검증
5. (선택) 정기적으로 신규 사례 리서치해서 `build_raw.py`/`build_normalize.py`에 반영하는 루틴 만들기 (예: 클로드 코드에서 주기적으로 실행하거나, Cowork 예약 작업으로 리서치만 하고 결과를 클로드 코드로 전달하는 하이브리드 방식도 가능)
6. (선택) 필터 축 추가 검토: exit 여부, AI 툴별 필터 등
