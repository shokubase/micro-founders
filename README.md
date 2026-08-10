# 바이브코딩 창업 사례 DB

1인/소규모 팀이 AI 코딩 도구(Cursor, Claude Code, Lovable, Bolt, Base44 등)로 만들고 수익화한 창업 사례를 모으는 정적 아카이브 사이트입니다.

## 구조

- `index.html`, `style.css`, `app.js` — 필터/정렬/검색이 되는 프런트엔드 (빌드 단계 없음, 그대로 GitHub Pages에서 서빙)
- `data/raw_cases.json` — 리서치로 수집한 1차 원본 데이터 (36건)
- `data/cases.json` — `raw_cases.json`에 정규화 필드(매출 연환산 USD 추정치, 매출 구간, 팀 규모 버킷, 창업자 배경 버킷, 도메인 카테고리 등)를 추가한 최종 데이터. **사이트가 실제로 읽는 파일**
- `build_raw.py` — 원본 사례를 `data/raw_cases.json`으로 만드는 스크립트 (신규 사례는 여기 리스트에 dict 하나 추가)
- `build_normalize.py` — `raw_cases.json` → `cases.json` 변환/정규화 스크립트 (신규 사례의 `ENRICH` 딕셔너리 항목 추가 필요)
- `build_feed.py` — `cases.json` → `feed.xml`(RSS) 생성 스크립트
- `feed.xml` — RSS 피드 (Feedly, Blogtrottr 같은 RSS→이메일 브릿지에 구독하면 이메일 알림도 가능)

## 배포 방법 (GitHub Pages)

1. GitHub에 새 저장소 생성 (예: `vibe-founders-db`)
2. 이 폴더 전체를 저장소에 push
3. 저장소 Settings → Pages → Source를 "Deploy from a branch"로 설정, 브랜치는 `main`, 폴더는 `/ (root)` 선택
4. 몇 분 후 `https://<username>.github.io/<repo>/` 로 접속 가능
5. `build_feed.py`의 `SITE_URL` 변수를 실제 배포 URL로 바꾸고 다시 실행

## 새 사례 추가하는 법 (2트랙)

**수동 추가 (즉시 반영)**
1. `build_raw.py`의 `cases` 리스트에 새 dict 항목 추가 (같은 스키마 준수)
2. `build_normalize.py`의 `ENRICH` 딕셔너리에 같은 `id`로 정규화 필드 추가 (매출 추정치, 카테고리 등)
3. 순서대로 실행: `python3 build_raw.py && python3 build_normalize.py && python3 build_feed.py`
4. 변경된 `data/*.json`, `feed.xml`을 커밋 & push

**정기 리서치 (Claude 세션에서)**
- Claude Cowork의 "예약된 작업(scheduled task)" 기능으로 주기적으로(예: 매주) 새로운 사례를 리서치해서 위 파이프라인에 반영하도록 요청 가능
- 이 세션에서 한 것처럼 여러 소스(Indie Hackers, Starter Story, 뉴스, 한국어 커뮤니티, X/트위터)를 병렬 서브에이전트로 조사 → 중복 제거 → 스키마 정규화 순서로 진행

## 데이터 신뢰도 표기

각 사례는 `confidence` 필드(high/medium/low)로 출처 신뢰도를 표기합니다.
- high: 복수의 독립적인 언론/1차 출처로 교차 확인됨
- medium: 단일 출처(본인 블로그, 인터뷰 등)로만 확인됨
- low: 2차 정리글에서만 언급되어 원출처 확인이 어려움

매출 등 수치는 원문 그대로(`revenue` 필드)와 내부 정규화 추정치(`revenue_annual_usd_est`, `normalize_note`에 산출 근거 명시)를 함께 보관합니다. 통화 환산 기준은 1 USD ≈ 1,350 KRW, 1 EUR ≈ 1.08 USD 로 고정 사용했습니다(2026-08 기준 근사치).

## 알림 설계

- **사이트 배지**: 마지막 방문 시각을 `localStorage`에 저장해두고, 그 이후 `ingested_at`이 더 최근인 사례 수를 헤더에 "새 사례 N건"으로 표시
- **RSS**: `feed.xml`을 구독하면 새 사례가 추가될 때(피드가 재생성될 때) RSS 리더/이메일 브릿지로 알림 가능
- 카카오톡 알림은 비즈니스 채널+알림톡 API 연동이 필요해 아직 미구현 (추후 검토)

## 앞으로 다듬을 거리

- 사례 수가 늘어나면 개별 URL/SEO를 위해 11ty 등 정적 사이트 제너레이터로 마이그레이션 검토 (데이터 스키마는 그대로 재사용 가능)
- `revenue_annual_usd_est`는 상당수가 추정치이므로, 검증 강화가 필요하면 사례별로 사람 검수 플래그를 추가하는 것도 고려
- 카카오톡/이메일 알림 연동
