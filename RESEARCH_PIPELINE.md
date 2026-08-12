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
| Indie Hackers | indiehackers.com/products, /interviews | 창업자 자진신고 매출 = 1차 출처. 검색 샘플링 말고 **최근 30-60일 피드 페이지네이션 직접 순회** (1회차 교훈) |
| Starter Story | starterstory.com | 상당수 페이월 — 무료 프리뷰 + YouTube 채널 활용. 헤더/홍보 수치는 창업자 발언과 자주 모순 (stoppr 1회차 실증) |
| Acquire.com | acquire.com | 라이브 리스팅은 로그인 필요 — 계정 없으면 뉴스레터/X 공지로 대체. **블로그는 대체재 아님** (1회차에 exit 커버리지 0건) |
| disquiet.io | disquiet.io | KR 메이커 수익 인증/회고 = 1차 출처. **구글 site: 우회 금지** (인덱스 지연으로 신규 글 누락) — 내부 최신 피드/그룹 게시판 직접 순회 |

### Tier 2 — 반구조화 (RSS/신규 글 감시)
| 소스 | 비고 |
|---|---|
| Lovable customer stories / blog + founder-stories-showcase.lovable.app | 마케팅 → confidence 상한 medium, 툴 필드 확정용 |
| Bolt / Base44 블로그, Cursor 블로그 + **forum.cursor.com showcase** | 〃 (Cursor 블로그는 엔터프라이즈 위주 — 포럼이 실성과, 1회차 실증) |
| 언섹시비즈니스 (maily.so/unsexybusinesskr) | KR 큐레이션 뉴스레터 |
| 조쉬 뉴스레터 (maily.so/josh) | KR 큐레이션 — 발견 신호 전용 (본인 글 아님, 해외 사례 번역·재요약 다수) |
| GPTers, EO플래닛(eopla.net) | KR 커뮤니티 — 본인 글이면 1차 출처 |
| Trends.vc, Failory | EN 큐레이션 — 리스트 등장 제품은 AI 툴 사용 여부를 스코프 렌즈로 선판정 후 후보화 |

### Tier 3 — 키워드 발견 (보조)
표준 쿼리 세트 (분기마다 갱신 — 최근 갱신: 2026-08-10 1회차 성과 데이터 기반):
- EN: `"built with Lovable" ARR|MRR|revenue` / `site:x.com OR site:indiehackers.com "vibe coded" MRR|ARR` /
  `solo founder AI app MRR` / `"Claude Code" built revenue` /
  `"sold my" app|SaaS "built with" Cursor|Claude|Lovable`
- KR: `바이브코딩 수익|매출` / `1인 개발 매출` / `바이브코딩 "월 매출"|"수익 인증"` /
  `클로드코드|커서 만들었다 매출 site:disquiet.io OR site:eopla.net` / `사이드프로젝트 수익화 AI`
- JP (2026-08-12 신설): `個人開発 "月商"|"収益報告"|"売上報告"` / `個人開発 MRR 公開 note` /
  `"個人開発" リリース 振り返り 収益 zenn` — 핵심 명사는 **個人開発**(1인 개발)

#### JP 층 실측 (2026-08-12 1회차)

재포획률 9%(11건 중 1건, 그마저 일본 매체의 Base44 재요약) — 층 자체는 완전히 새롭다.
**단 수확은 거의 없었다.** 구조적 이유 세 가지를 기록해둔다:

1. **SEO 수익화 가이드가 담론을 점령했다.** `個人開発 + 収益` 계열 쿼리는 shiftb.dev,
   AIVENTURE, 프로그래밍스쿨 비교 사이트 등 강좌·스쿨 판매 콘텐츠가 상위를 덮는다.
   창업자 자진신고가 아니라 교육 상품 마케팅이다
2. **공개된 수익 규모가 작다.** 실제 수익 보고 블로그는 존재하나 월 2만엔~30만엔대가
   중심이다 (예: TF's apps 2026-06 월 ¥20,400). 아카이브 하한에 못 미치는 경우가 많다
3. **도구명을 안 쓴다.** 일본 개발자들은 "AIを活用" 정도로만 적고 Cursor/Claude Code를
   특정하지 않는 경향이 뚜렷하다. 스코프 렌즈의 발화 편향이 영어권보다 심하다

**검색 요약을 출처로 쓰지 마라 (JP에서 실증).** 이번 실행에서 검색 요약이
"21세 비개발자가 Claude Code+Cursor로 만든 습관관리 앱, 3개월만에 월商 1,000만엔"을
두 번 생성했으나, 지목된 원문 기사에는 **그런 사례가 없었다** (실제는 나이·도구 언급
없는 "生活管理アプリ 월 500만엔"). 원문을 열기 전까지 리드는 존재하지 않는 것으로 취급할 것.

다음 JP 실행은 검색 대신 **개인 블로그·note의 정기 수익보고 시계열을 직접 순회**하는
쪽이 낫다 (`週末のアプリ作成`, `ぶべの開発日記` 등 — 본인이 매달 숫자를 올리는 곳).

갱신 원칙 (1회차 실증): 수익 발화 토큰("MRR", "수익 인증", "sold my") 없이 일반 명사만
조합하면 SEO 리스티클/튜토리얼만 걸린다. 시의성이 필요하면 검색 recency 파라미터나
연도 리터럴 변형을 쓸 것.

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

#### 1차 출처 fetch 경로 — 브라우저는 오케스트레이터 독점 (2026-08-12)

**WebFetch는 x.com에서 402, JS 렌더링 사이트(IH `/products` 등)에서 빈 응답을 준다.**
이 파이프라인의 1차 출처는 대부분 창업자 본인 X 발화이므로 이건 치명적이다 —
2026-08-11 점검에서 기존 기각 5건(wrestle-ai, caret, kevin-badi-portfolio, lunair,
shiftnex)이 전부 "원문 발화 미확보" 사유였는데, 당시 검증 에이전트에는 그 페이지를
열 수단 자체가 없었다. 즉 **증거 부재가 아니라 도구 한계였을 가능성**이 있다.

playwright가 그 페이지들을 여는 건 확인됐다(x.com 트윗 본문은 `og:description`,
IH SPA는 대기 후 `innerText`). **단 브라우저를 에이전트에 붙이면 안 된다.**

> 2026-08-12 실증: 검증 에이전트 3종에 playwright를 붙이고 5개를 병렬로 돌렸더니
> 에이전트들이 서로 탭을 뺏었다. 에이전트 자체 로그에 "shared browser keeps
> drifting to other agents' pages", "Browser is contended again"이 남았다.
> A가 연 페이지를 B가 읽고 "확인했다"고 보고할 수 있다 — 출처 검증이 존재 이유인
> 파이프라인에서 가장 나쁜 오염이다.

그래서 구조는 이렇다:

```
오케스트레이터(메인 세션)          검증 에이전트
  playwright 독점, 직렬 수집    →    Read로 스냅샷 판독
  스냅샷 파일로 저장                 못 여는 URL은 fetch_requests로 요청
  요청받은 URL 추가 수집        ←
  SendMessage로 에이전트 재개   →    최종 판정
```

- 스냅샷 저장 위치: 스크래치패드 `sources/<candidate-id>/<slug>.md`,
  파일 상단에 원본 URL과 수집 시각 기록
- 에이전트 도구에 playwright를 **넣지 마라**. `.claude/agents/*.md`의 `tools:`는
  WebSearch/WebFetch/Read(+Bash)로 유지
- 사전 수집 대상은 후보 파일의 `verification.primary_sources` — 이미 URL 목록이 있다
- **검색은 WebSearch로만.** 브라우저로 검색엔진에 가면 이 환경의 차단기(Freedom)에
  막힌다. 브라우저는 지정된 URL 열람 전용
- 에이전트는 `unverifiable`(찾았으나 확인 불가)과 `not_attempted`(수단이 없어 못 봄)를
  구분해 반환한다. **후자는 기각 근거가 될 수 없다**

#### 도구 미사용 판정 기준

문서 한 편에 도구 언급이 없는 건 미사용의 증거가 아니다. 2026년에는 Cursor·
Claude Code 사용이 기본값이라 언급하지 않는 쪽이 정상이고, 언급을 요구하면 도구를
*쓴* 사람이 아니라 도구 *얘기를 하는* 사람만 수집되는 발화 편향이 생긴다.

- `fail` — **본인이 명시적으로 부정**한 경우에만 (선례: zigpoll)
- `borderline` → pass — 확인했으나 언급 미발견. `unknown`이지 `none`이 아니다
- 판정 전 창업자 본인 공개 계정 1곳 이상 확인 필수

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

0. **실행 전 리드 대조.** 발견한 리드는 `python3 research_metrics.py --check "제품명"`으로
   먼저 걸러라. 재포획률이 높아 상당수가 이미 있는 사례다 — 검증에 들어가기 전에 버린다
1. Tier 1-2 소스별 신규 글 확인 + Tier 3 표준 쿼리 1회전
   (`source-hunter` 각도별 병렬 팬아웃 — 각도 간 결과 비공유가 설계 의도)
2. 신규 후보 → Stage 2 추출 → Stage 3 3렌즈 검증 → Stage 3.5 completeness critic
3. `check_candidates.py` 통과 확인 → 후보 큐 커밋
4. verified 후보는 사용자 승인 요청 → 승인분만 Stage 4 반영
5. **실행 지표 기록.** 마주친 고유 리드를 파일로 모아
   `python3 research_metrics.py leads.txt --as-of <실행일>` 실행.
   `--as-of` 없이 사후에 재면 신규 후보가 이미 인덱스에 있어 항상 100%가 나온다
6. 커밋 메시지에 신규/검증/반영 건수 + **재포획률** 요약

### 재포획률로 어디를 팔지 정한다

`research_metrics.py`가 내는 재포획률(= 마주친 리드 중 이미 DB/큐에 있던 비율)이
그 층(stratum)의 포화도다. Lincoln-Petersen 추정치도 함께 나오는데, 유명 사례일수록
양쪽 표본에 잡혀 중복이 부풀므로 **이 값은 하한**이다.

- 2026-08-11 실행: 영어권 인디미디어 층 재포획률 **77%**, 모집단 하한 ≈52건 (현재 40건)
  → 이 층은 거의 훑렸다. 스코프 규칙을 완화해서 얻는 건 남은 10여 건의 일부뿐이다
- 성장은 재포획률이 낮은 **새 층**에서 나온다. 미개척: 일본어·중국어·스페인어·
  포르투갈어권 (현재 각 0건)

**포화된 층에서 Workflow 팬아웃을 늘리지 마라** — 병렬 에이전트가 서로 같은 사례를
중복 발견해 토큰만 쓴다. 팬아웃은 층이 여러 개일 때 의미가 있으므로,
언어권 확장을 먼저 하고 그다음 언어권별 병렬로 붙이는 순서여야 한다
(Workflow 하네스는 사용자 명시 요청 시에만).
