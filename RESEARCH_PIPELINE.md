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
| Indie Hackers | **indiehackers.com/tech** (공개 피드, 최우선) | 창업자 자진신고 매출 = 1차 출처. 검색 샘플링 말고 **피드 직접 순회** — 2026-08-12 실증으로 검색 대비 재포획률 77%→15%. `/products` DB는 로그인 게이트라 브라우저로도 5건(Build Board)만 보인다. 피드 순회 스니펫은 아래 |
| Starter Story | starterstory.com | 상당수 페이월 — 무료 프리뷰 + YouTube 채널 활용. 헤더/홍보 수치는 창업자 발언과 자주 모순 (stoppr 1회차 실증) |
| Acquire.com | acquire.com | 라이브 리스팅은 로그인 필요 — 계정 없으면 뉴스레터/X 공지로 대체. **블로그는 대체재 아님** (1회차에 exit 커버리지 0건) |
| disquiet.io | disquiet.io | KR 메이커 수익 인증/회고 = 1차 출처. **구글 site: 우회 금지** (인덱스 지연으로 신규 글 누락) — 내부 최신 피드/그룹 게시판 직접 순회 |
| **TrustMRR** | trustmrr.com/startup/&lt;제품&gt;, /founder/&lt;핸들&gt; | **결제사 API 연동 검증치** — 창업자가 Stripe·Polar·LemonSqueezy 키를 연결하면 last-30-days·MRR·all-time·활성구독수가 자동 산출된다. 자기보고와 대조할 수 있는 드문 준-독립 출처 |

#### TrustMRR 사용 규칙 (2026-08-12 실증)

`ai_tools` 심사만큼 중요한 도구다. 2026-08-12에 socialkit·postpeer·bazzly·leadverse 4건이
등재돼 있었고, jonathan-geiger 판정에서 결정적이었다. 단 해석에 주의할 점이 있다:

- **자기보고 편향의 방향이 지표별로 갈린다.** jonathan-geiger는 MRR에서 검증치를
  +34% 상회했으나 **총매출에서는 -12% 하회**했다. 즉 "과장" 프레임이 아니라
  "MRR 산정 정의 불일치"(트라이얼·연체 구독 포함 여부)로 읽어야 한다.
  bazzly도 TrustMRR($8,705)이 자기보고($7.5K)보다 **높다**.
- **`all-time` 집계 시작 시점 정의가 페이지에 없다.** API 키 연결 시점부터일 가능성이
  높아(제품 런칭 시점과 다름) 누적 매출 대조에 쓸 때 이 불확실성을 명기할 것.
- **정성 필드(가격 티어, 팀 규모)는 창업자 자기기재이거나 구식일 수 있다** —
  검증 위젯 수치와 등급이 다르다. socialkit Growth 티어를 $49로 적었으나 공식
  사이트는 $39였다.
- 등재 자체가 창업자의 선택이므로 **미등재가 음성 신호는 아니다.**

#### IH 피드 순회 스니펫 (오케스트레이터 전용)

`mcp__playwright__browser_navigate`로 `https://www.indiehackers.com/tech`를 연 뒤:

```js
() => new Promise(r => setTimeout(() => {
  const as = [...document.querySelectorAll('a[href*="/post/"]')]
    .map(a => ({t: (a.innerText||'').trim().replace(/\s+/g,' ').slice(0,140),
                h: a.getAttribute('href')}))
    .filter(x => x.t.length > 15);
  const seen = new Set(), out = [];
  for (const x of as) if (!seen.has(x.h)) { seen.add(x.h); out.push(x); }
  r({n: out.length, items: out});
}, 5000))
```

`innerText`로는 리스트가 안 잡힌다(재렌더 중복이 섞임) — 반드시 앵커 DOM에서 뽑을 것.
제목에 날짜·창업자명·수치가 들어 있어 목록만으로 1차 스크리닝이 된다.
**단 제목 수치는 IH 편집자 표기이므로 본문 본인 발화로 재확인해야 한다.**
`research_metrics.py --check "<이름>"`으로 먼저 중복을 걸러낸 뒤 본문을 읽어라.

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
               ※ Stage 2 필수 규칙 3종은 아래 참조 — 안 지키면 Stage 3에서 전부 되돌아온다
Stage 3 검증   아래 체크리스트 수행 → verification 블록 기록 (status: verified)
Stage 4 반영   사람 승인 → build_raw.py + build_normalize.py ENRICH 반영 →
               파이프라인 재실행 → candidate status: merged → 커밋
```

### Stage 2 필수 규칙 (2026-08-12 실증)

3렌즈 검증 5건을 돌린 결과, **fail의 대부분이 사례 결함이 아니라 후보 파일 기재 오류**였다.
아래 셋을 Stage 2에서 지키면 그 왕복이 사라진다.

#### (1) 애그리게이터·매체의 헤더 수치를 후보 파일에 옮기지 마라

Indie Hackers 글은 제목·인포박스에 **편집부가 계산한 수치**를 싣는다. 본문의 창업자
1인칭 발화와 다르다. 2026-08-12 실행에서 IH 유래 후보 3건이 전부 여기 걸렸다:

| 후보 | 내가 옮긴 값 | 실제 |
|---|---|---|
| faceless-video | 월 $83K | $1M ARR ÷ 12 파생값, 2024년 마일스톤. 본인 발화는 "6-figures in MRR"(더 높다) |
| jonathan-geiger | "MRR $6.4K" | 순수 MRR은 $5.2K. $6.4K는 MRR+일회성 총매출. 같은 기사 필드는 "$6.3K a month"로 또 다름 |
| thirstysprout | 월 $208K | 연 $2.5M ÷ 12 = $208,333 역산치. 창업자는 월 단위 금액을 말한 적 없음 |

**규칙: 수치는 본문의 1인칭 발화에서만 뽑고, 제목·인포박스 값은 그것과 다르면 기록조차
하지 마라.** 나눠떨어지는 수치(연매출÷12)를 보면 역산치를 의심할 것.

#### (2) `founded_year`를 반드시 채워라 — 스코프 창 판정의 결정값

thirstysprout(2018년 창업)이 Stage 3까지 살아온 이유는 **후보 스키마에 창업 연도 필드가
없었기** 때문이다. 이 값 하나면 Stage 2에서 걸러졌다. laravel-shift(2015)·savvycal(2020)·
superpower-chatgpt(2022)도 같은 축에서 기각됐다.

#### (3) `region`을 unknown으로 두기 전에 개발자 프로필을 봐라

2026-08-12에 unknown으로 적은 2건이 모두 틀렸고, 둘 다 **본인 GitHub/dev.to 프로필의
location 필드**에 있었다 (sergiu → 포르투갈 리스본, jonathan-geiger → 이스라엘).
IH 본문만 보고 unknown 처리하는 패턴이 원인이다. GitHub·dev.to·LinkedIn 프로필의
location을 기본 확인 항목에 넣을 것.

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

- `fail` — **본인이 명시적으로 부정**한 경우에만 (선례: zigpoll, pckgr, faceless-video)
- `borderline` → pass — 확인했으나 언급 미발견. `unknown`이지 `none`이 아니다
- 판정 전 창업자 본인 공개 계정 1곳 이상 확인 필수

#### 증거 비대칭을 데이터로 노출한다 — `tool_question_probed` (2026-08-12 신설)

위 규칙은 일관되지만 **증거 획득이 비대칭**이다. 2026-08-12 실증:

| 사례 | 스택 | 도구 질문을 받은 기록 | 판정 |
|---|---|---|---|
| my-askai | Bubble(80%) + OpenAI API | 없음 | pass |
| formula-bot | Bubble + OpenAI API | 없음 | pass |
| faceless-video | Bubble + Replicate | **있음** — 팟캐스트에서 바이브코딩을 설명받고 "out of that sphere"라 답함 | **fail** |

세 사례의 스택 구조가 동일한데 결과가 갈린다. 즉 걸러지는 것은 "부정한 사람"이 아니라
**"질문받은 사람"**이다. 솔직하게 인터뷰에 응한 창업자가 역차별받는 구조다.

**그럼에도 규칙은 유지한다** — 기록된 것만 기록하는 것이 원칙이고, 없는 증거를 추정으로
메우는 것은 이 아카이브가 반복해서 사고를 낸 방식이다(2026-08-12 세션에서 검색 요약
날조 3건, 그중 1건은 렌즈 판정까지 침투). 대신 비대칭을 은폐하지 않고 필드로 드러낸다.

- `tool_question_probed: true` — Stage 3에서 scope-judge가 도구 항목을 **명시적으로 심사**
- `false` — 초기 일괄 적재분 등. 언급이 없어서 안 적었을 뿐 확인한 것이 아니다

`ai_tools`가 채워져 있다는 것과 도구 사용을 심사했다는 것은 **다르다.** 2026-08-12 기준
41건 중 심사된 것은 6건(15%)이고, `ai_tools`는 있으나 미심사인 사례가 22건이다.
`research_metrics.py`가 매 실행 이 비율을 출력한다 — 낮으면 코퍼스의 도구 데이터
대부분이 미검증이라는 뜻이므로, 이 값을 근거로 스코프 규칙을 조이거나 풀지 말 것.

**구조 규칙 vs 계보 규칙 논쟁은 이 필드로 대체됐다.** faceless-video 재심에서
"선례(my-askai·formula-bot)를 스택 구조로 읽을지 창업자 계보로 읽을지"가 쟁점으로
올라왔으나, 기존 규칙("부정이 기록된 경우에만 fail")이 세 사례를 모순 없이 처리하므로
양자택일이 필요 없다. 기존 사례 재감사도 불필요하다 — 부정 기록이 없으면 pass가 맞다.

판정 규칙:
- **3/3 pass** → `verified` (confidence = 세 렌즈 recommendation의 최솟값)
- **2/3 pass** → `verified`, 단 fail 렌즈의 반박 내용을 notes에 명시
- **1/3 이하** → `rejected` (사유 보존)
- 예외: **수치 렌즈 fail + 매출이 핵심 주장**인 후보는 2/3이어도 `rejected`

#### fail의 두 유형을 구분하라 (2026-08-12 신설)

위 규칙을 기계적으로 적용하면 안 된다. fail에는 성격이 다른 두 가지가 섞인다:

- **사례 결함** — 창업자의 주장 자체가 무너지거나 스코프 밖. → `rejected`
  (예: thirstysprout — 2018년 창업, GMV/net 미확정, 팀 수십 명)
- **후보 데이터 오류** — 창업자 주장은 멀쩡한데 **내가 잘못 옮겨 적었고** 렌즈가 교정값을
  제시한 경우. → 교정 후 `pending_verification` 유지, 해당 렌즈만 재검증

후자를 기각하면 멀쩡한 사례를 잃는다. 2026-08-12 실행에서 faceless-video는 실제 수치가
내가 적은 것보다 **높았고**(월 $83K → 6-figure MRR), jonathan-geiger는 창업자 본인이
recurring과 one-time을 정확히 분리해 말했는데 내가 편집부 헤드라인을 옮긴 것이었다.

판별 기준: **렌즈가 교정값을 제시했는가.** 제시했다면 데이터 오류이고, "확정 불가"로
끝났다면 사례 결함이다.

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
  "case": {
    "build_raw.py의 dict와 동일한 필드": "...",
    "founded_year": "정수. 스코프 창(2023~) 판정의 결정값 — 반드시 채울 것 (§Stage 2 필수 규칙)"
  },
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

**재포획률은 층이 아니라 표집 프레임을 측정한다 (2026-08-12 정정).**

| 실행 | 표집 방식 | 재포획률 |
|---|---|---|
| 2026-08-11 (EN) | 검색 쿼리 | **77%** |
| 2026-08-12 (EN) | `indiehackers.com/tech` 피드 직접 순회 | **15%** |

같은 층, 같은 소스, 이틀 차이. 검색은 인기·정본 콘텐츠를 반환하는데 그건 **이미 DB에
들어와 있는 것들**이다. 피드는 최근 꼬리를 준다. 2026-08-11의 "영어권은 포화, 모집단
하한 52건" 결론은 층의 포화가 아니라 **검색 도달 가능성의 포화**를 잰 것이었다 —
피드 한 페이지(20건)에서 신규 17건이 나왔고, 그중 3건만 기존 사례였다.

교훈:
- **재포획률을 보고할 때 표집 방식을 반드시 함께 적어라.** 방식이 다르면 비교 불가다
- 검색 기반 재포획률이 높다고 층을 포기하지 마라. 먼저 **표집 방식을 바꿔보고**
  그래도 높으면 그때 층을 옮긴다
- 2026-08-11에 "포화됐으니 스코프 규칙을 완화해 남은 몇 건을 짜내자"고 한 판단은
  전제가 틀렸다. 규칙 완화가 아니라 순회가 답이었다

성장 경로: 재포획률이 낮은 **새 표집 방식** 또는 **새 층**. 미개척 층은 중국어·
스페인어·포르투갈어권 (각 0건), 일본어권은 1회 실행(§JP 층 실측).

**포화된 층에서 Workflow 팬아웃을 늘리지 마라** — 병렬 에이전트가 서로 같은 사례를
중복 발견해 토큰만 쓴다. 팬아웃은 층이 여러 개일 때 의미가 있으므로,
언어권 확장을 먼저 하고 그다음 언어권별 병렬로 붙이는 순서여야 한다
(Workflow 하네스는 사용자 명시 요청 시에만).
