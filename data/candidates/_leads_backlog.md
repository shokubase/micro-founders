# 리드 백로그 — 발견됐으나 아직 1차 출처 미판독

Stage 1에서 잡혔지만 Stage 2 추출까지 못 간 리드. 다음 실행은 여기부터 시작한다.
읽고 나면 후보 파일로 승격하거나 기각 사유를 적고 이 목록에서 제거할 것.

## 2026-09-21 정기 리서치 — 세션 전체 네트워크 정책으로 Stage 2/3 진행 불가 (2주 연속)

**이번 실행도 후보 큐를 건드리지 않았다.** 2026-09-14와 동일한 증상을 재확인했다:
`indiehackers.com`, `starterstory.com`, `x.com`에 대해 `WebFetch`와 직접 `curl` 양쪽 모두
게이트웨이 `403 connect_rejected`(egress 프록시 `organization policy` 거부)를 받았다.
`curl -sS $PROXY/__agentproxy/status`의 `recentRelayFailures`에도 세 도메인 전부가
같은 타임스탬프로 기록됐다 — 일시적 네트워크 오류가 아니라 **이 세션 종류(스케줄
자동 실행)에 적용되는 egress 정책 자체가 연구 소스 도메인을 막고 있다**는 뜻이다.
`WebSearch`는 정상 동작했다(테스트 쿼리 1건 확인).

Stage 3.0 사전 수집에 필요한 playwright 브라우저 툴도 이 환경의 사용 가능 툴 목록에
없었다(`ToolSearch`로 확인) — 애초에 SKILL.md가 전제하는 "오케스트레이터가 브라우저로
1차 출처를 직접 수집" 경로 자체가 이 세션 종류에서는 불가능하다.

파이프라인 핵심 원칙("검색 요약을 출처로 쓰지 마라" — caret 10배 오류, artmvstd 화자
오귀속 등 §RESEARCH_PIPELINE.md 실증)에 따라 WebSearch 요약만으로 Stage 2/3을 강행하지
않았다. 신규 후보 0건, 이월 후보(wrestle-ai/lunair 이미 merged, shiftnex 스코프 fail
확정) 재작업 불필요 재확인 — 09-14 판단 그대로 유효.

**2주 연속 100% 차단.** 09-07(부분 우회 가능) → 09-14(전면 차단) → 09-21(전면 차단,
동일 재현). 네트워크 정책을 바꾸지 않는 한 이 스케줄 실행은 구조적으로 매번 빈손이다.
사용자 판단이 필요한 사안으로 별도 보고함.

## 2026-09-14 정기 리서치 — 세션 전체 네트워크 정책으로 Stage 2/3 진행 불가

**이번 실행은 후보 큐를 건드리지 않았다.** 이유: 이 세션의 네트워크 egress 정책이
`WebFetch`·직접 `curl` 양쪽에서 **연구 소스 도메인 전부를 게이트웨이 403으로 차단**했다
(`indiehackers.com`, `x.com`, `disquiet.io`, `starterstory.com`, `lovable.dev`,
`trustmrr.com`, `note.com`, `producthunt.com`, `dev.to`, `medium.com`, `web.archive.org`,
`r.jina.ai` 전부 `EGRESS_BLOCKED`/`403`). 허용된 건 `github.com`류 개발 인프라 도메인과
`WebSearch`뿐이었다 — 2026-09-07 실행이 기록한 것과 같은 유형이지만 이번엔 **한 도메인도
안 열렸다**(그때는 WebSearch로 우회해 잠정 판정이라도 냈다).

이 파이프라인은 "검색 요약을 출처로 쓰지 마라"가 핵심 원칙이다(§RESEARCH_PIPELINE.md
"요약 fetch가 숫자를 바꾼다" — caret 10배 오류, artmvstd 화자 오귀속 등 실증 다수).
WebFetch/브라우저 없이 WebSearch 요약만으로 Stage 3 검증을 강행하면 정확히 그 실패
패턴을 재현하는 것이므로, **이번 실행은 신규 후보를 verified/rejected로 올리지 않았다.**
대신 아래는 WebSearch만으로 훑은 결과이며 전부 "발견 신호"일 뿐 출처 확인 안 됨:

- David Attias 앱 포트폴리오, Jason Zook(Solo Content Studio) — 둘 다 기존 백로그(아래)에
  이미 있던 리드. 이번 검색도 같은 정보 이상은 못 얻음(원문 미열람 그대로)
- JP 개인 블로그 수익보고 시계열 직접 순회 — 여전히 미실행(브라우저/WebFetch 필요, 이번도 차단)
- ES/PT/KR 신규 쿼리 — 마케팅 리스티클(`aibusiness.vc` "Marcus $18K MRR" 류 익명 합성
  사례 등)만 걸림. 1차 출처 아님, 후보화 안 함
- 이월 과제(carryover) 확인: `wrestle-ai`·`lunair`는 **이미 merged**(2026-08-10),
  `shiftnex`는 기각 사유가 원문 발화 미확보가 아니라 **스코프 fail(팀 약 11명, 회사 공식
  About 명단으로 확정)**이라 원문을 추가로 찾아도 뒤집히지 않음 — 재작업 불필요로 판단하고
  건드리지 않았다

**다음 실행 권장:** 이 저장소 세션의 네트워크 정책을 연구 소스 도메인이 열리는 환경으로
바꾸거나(예: 대화형 세션·다른 egress 정책의 환경), 최소한 WebFetch가 `indiehackers.com`
하나라도 뚫리는 세션에서 재시도할 것. 그 전까지는 정기 스케줄 실행이 매번 빈손이 된다.

## 현재 백로그 (2026-09-07 정기 리서치 — weak 신호, 다음 실행 우선 판독)

이번 실행에서 Stage 2로 승격한 5건(payout-connor-burd, profit-pulse-jack, post-bridge-jack-friks,
gift-my-book-yoav-hornung, liu-xiaopai-portfolio)은 이미 후보 파일로 존재. 아래는 `weak: true`로
표시됐거나 수익화 근거가 약해 이번엔 후보화하지 않은 리드들.

### 이번 세션 최대 발견 — 환경 제약
**WebFetch가 이 세션 내내 거의 모든 도메인(indiehackers.com, x.com, starterstory.com,
disquiet.io, threads.com, gpters.org, linkedin.com 등)에서 `EGRESS_BLOCKED`였다.**
이건 x.com 특유의 402와 다른, 세션 전반의 프록시 차단이었다 — WebSearch로 우회했지만
raw HTML 직접 대조가 거의 불가능해 다수 판정이 "잠정(fetch_requests 있음)"으로 남았다.
**다음 실행이 브라우저/WebFetch 접근이 정상인 세션이라면 이번 회차의 fetch_requests부터
처리할 가치가 크다** — 특히 payout-connor-burd(수치), post-bridge-jack-friks(존재 확정),
liu-xiaopai-portfolio(재심 가능성 높음, 아래 참조).

### EN — 강한 신호였으나 이번엔 후보화 안 함 (다음 우선)
| 리드 | 창업자 | 신호 | 비고 |
|---|---|---|---|
| David Attias 앱 포트폴리오 | David Attias | 월 $10K, Figma MCP+Cursor+Firebase 구체적 도구 체인 | IH 글, 개별 앱명 미확인 — 다음 실행에서 Stage 2 승격 검토 |
| Solo Content Studio | Jason Zook (@jasondoesstuff) | MRR $1,907→코호트 $13K, Lovable→Claude Code Opus 전환 서술 | x.com 원문 미확인 |

### EN — weak (수익화 근거 약함/도구 미확인, 추적용만)
Northstone(덴마크 AI 회계, $2.8K MRR), WhatsScale($0 MRR), Angel Match/Rashid Khasanov(포트폴리오
$42K MRR, 도구 미확인), Sequenzy+BlogToPin/Nic Polotnianko($16K MRR, 도구 미확인), Max Artemov
30-앱 포트폴리오($22K/mo, 도구 미확인), AI Flow Chat/Starpop($20K MRR 합산, 도구 미확인),
35개 마이크로 SaaS/@ridark_eth($77K/월, 익명 핸들·미검증), Gramms(Claude, 수익화 전),
Inithouse/Jakub(Lovable 주력, 14개 SaaS, 매출 미확인), Quiqlog.com(Claude Code+Cursor, 수익화 전),
VoxDuru Media/Berk Eryaprak(Cursor, 매출 수치 없음), Pashu E-Chaara(Bolt.new, $3.7K/mo, 창업자
실명 미상), HERD(Cursor, 비영리 성격), WP Linker/Tatsuya Mizuno(Claude AI, 매출 소액),
RizzGPT/Umax(Blake Anderson·Zach Yadegari — cal-ai와 동일 클러스터, 도구 불명확, 중복 위험).

### KR — weak
심심이 사내 AI 캐릭터챗(김윤하+WOO, MRR 1억+ 주장이나 인트라프레너십에 가까워 스코프 불확실,
도구 미확인), 후디 hoodi_ux Claude 앱(Threads, "월천만원", threads.com 차단으로 미확인),
Vooster.ai/최수민(바이브코딩 도구 자체를 만든 창업자 — 도구 사용자가 아니라 도구 제작자,
매출 미확인), 릴리스AI(Lilys AI, 이미 투자 유치해 성장, AI 코딩 도구 사용 여부 불명 — 참고: 기존
cases.json의 `relic-ai`와 동일 실체인지 대조 필요, 이름이 유사해 혼동 주의).

### 미개척 층 재확인
- **중국어권: 첫 실행 완료(liu-xiaopai-portfolio, 실존 확정·rejected — 매출 수치 재조사 필요).**
  다음 실행에서 위 fetch_requests 3건 처리 시 재심 유력. 추가로 CNY 환산 레이트가
  CLAUDE.md에 아직 없음 — 재심 전 레이트 정의 논의 필요
- 스페인어권, 포르투갈어권: 여전히 0건
- 일본어권: 이번 실행에서도 재시도 안 함(KR 에이전트가 부수적으로 살짝 건드림) — 개인
  블로그·note 정기 수익보고 시계열 직접 순회 여전히 미실행

`indiehackers.com/tech` 피드 2026-06-27 ~ 2026-08-11 구간(20건)은 **전부 판독 완료**
(2026-08-12). 처리 결과는 아래 참조.

## 처리 완료 — indiehackers.com/tech 피드 1페이지 (2026-08-12)

피드 20건 = 재포획 3건 + 신규 17건. 신규 17건의 처분:

### 후보 적재 (pending_verification, 12건)

| id | 창업자 | 수치 | 도구 근거 |
|---|---|---|---|
| `faceless-video` | Jacob Seeger | 월 $83K / 10개월 ARR $1M | Bubble 노코드 (my-askai 선례) |
| `thirstysprout` | David Stepania | 월 $208K+ / 연 $2.5M+ | Claude·Claude Code 명시 (팀 규모 쟁점) |
| `ninjapear` | Steven Goh | 월 $15K | **Claude Code 명시** — 2주 제작 |
| `erik-aronesty-portfolio` | Erik Aronesty | 월 약 $15K | 스택에 Codex·Claude (용도 구분 필요) |
| `sergiu-chiriac-portfolio` | Sergiu Chiriac | 월 $10K+ / 최고 $15.7K | AI 코딩 사용 긍정 발화, 도구명 없음 |
| `rightblogger` | Ryan Robinson | ARR $350K / MRR $29K | 없음 (borderline) |
| `ai-toolbox` | Adi Leviim 외 1 | 월 $10K+ | 없음 (borderline) |
| `klipy` | Jung Hong Kim | 월 $10K+ | 없음 (borderline) |
| `bazzly` | Filip Panoski | 월 $7.5K | AI 활용 긍정 발화, 도구명 없음 |
| `ramsri-portfolio` | Ramsri Goutham Golla | 월 $6~7K | **Claude Code 명시** (단 제품은 도구 이전 제작) |
| `jonathan-geiger-portfolio` | Jonathan Geiger | MRR $6.4K | "Claude is my team, from writing code…" |
| `jobric` | Erik Chavez | MRR $3.3K | 없음 (borderline) |
| `leadverse` | Jakub Mužík | MRR $3.3K | 없음 (borderline) |

### 스코프 기각 (rejected, 4건)

| id | 창업자 | 기각 사유 |
|---|---|---|
| `pckgr` | Thomas Mahony | **본인 명시적 부정** — "This was before AI tools like Claude Code and Cursor were available" |
| `superpower-chatgpt` | Saeed Ezzati | 2022년 말 제작 (스코프 창 이전) + 도구 언급 없음 |
| `laravel-shift` | Jason McCreary | 2015-12-23 창업 — 7년 이상 앞섬 |
| `savvycal` | Derrick Reimer | 2020년 창업 + 도구 언급 없음 |

### 재포획 (기존 항목, 3건)
`lancer`(Ivan Nedelkovski) / `appalchemy`(Diego Roshardt) / `zigpoll`(Jason Zigelbaum, 기각됨)

## 다음에 열 것

- **IH 피드 "Load More"** — 2026-06-27 이전 구간은 아직 안 훑었다. 같은 방식이 그대로 통한다
- 중국어권 (0건), 스페인어권 (0건), 포르투갈어권 (0건)
- 일본어권은 1회 실행했으나 검색 경로가 막힘 — 개인 블로그 정기 수익보고 시계열
  직접 순회로 재시도할 것 (RESEARCH_PIPELINE.md JP 층 실측 참조)
