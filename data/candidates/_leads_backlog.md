# 리드 백로그 — 발견됐으나 아직 1차 출처 미판독

Stage 1에서 잡혔지만 Stage 2 추출까지 못 간 리드. 다음 실행은 여기부터 시작한다.
읽고 나면 후보 파일로 승격하거나 기각 사유를 적고 이 목록에서 제거할 것.

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
