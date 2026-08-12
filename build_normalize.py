import json

raw = json.load(open("data/raw_cases.json", encoding="utf-8"))

# ---- Controlled vocab ----
# domain_category, team_size_bucket, founder_background(dev/non-dev/mixed/unknown),
# founder_experience(first-time/serial/unknown), revenue_annual_usd_est (int or None)

# ---- 도구 심사 여부 (tool_question_probed) ----
# ai_tools 필드가 채워져 있다는 것과 "도구 사용 여부를 실제로 심사했다"는 것은 다르다.
# 아래 사례들은 Stage 3 3렌즈 검증에서 scope-judge가 도구 항목을 명시적으로 판정했다.
# 나머지는 초기 일괄 적재분으로, 언급이 없어서 안 적었을 뿐 확인한 것이 아니다.
#
# 왜 이 구분이 필요한가 (2026-08-12): faceless-video는 팟캐스트에서 바이브코딩을
# 질문받고 "out of that sphere"라 답한 기록 때문에 기각됐다. 반면 my-askai·formula-bot은
# 스택 구조가 동일한데 아무도 물어본 적이 없어 통과 상태다. 즉 "부정한 사람"이 아니라
# "질문받은 사람"이 걸러진다. 이 비대칭을 은폐하지 않고 데이터에 노출한다.
TOOL_PROBED = {
    "imaginary-space", "kleo", "lumoo", "ninjapear", "stoppr", "superx",
    "jonathan-geiger-portfolio", "sergiu-chiriac-portfolio",
    # 2026-08-12 백필로 1차 출처 원문을 직접 확인한 건
    "habit-pixel",
    # 2026-08-12 쟁점 4건 3렌즈 검증 통과분
    "rightblogger", "leadverse", "ramsri-portfolio",
}

# 백필 시도했으나 확정 실패 — 재시도 시 같은 벽을 다시 치지 않도록 기록한다.
#
# samuel-rondot-portfolio: ai_tools를 채우지 않는다.
#   IH 글(OA5p18fXtvHGxP9xTAwG)의 Claude/Cursor 언급 11건이 **전부 제3자 댓글**이다.
#   viascan("I created a SAAS in two days thanks to Claude AI")과 jettfu("All coding
#   written by Claude")는 댓글 작성자 본인 얘기이고, Finalertcleveland("Are you still
#   building by coding by yourself or vibe coding now?")와 Edgar("if you'd had today's
#   AI coding tools from the very beginning?")는 창업자에게 던진 **질문**이다.
#   창업자 본인 발화는 하나도 없다.
#   본문에 'Leveraging AI tools to build' 섹션이 존재하나 **IH 페이월** 안에 있어
#   접근 불가다(계정 생성은 하지 않는다). 즉 근거 부재가 아니라 not_attempted다.

ENRICH = {
"base44": dict(domain_category="AI 코딩/개발툴", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=2000000, exit_value_usd=80000000,
    normalize_note="2025-05 월 순이익 $189K를 연환산한 추정치(매출 자체보다는 이익 기준 proxy). exit_value_usd는 Wix 인수 현금가."),
"pieter-levels-portfolio": dict(domain_category="AI 이미지/영상 생성", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=3000000, exit_value_usd=None,
    normalize_note="Photo AI MRR $132K(연 $1.58M) + 포트폴리오 전체 약 $3M/yr로 인용된 수치 사용."),
"headshotpro": dict(domain_category="AI 이미지/영상 생성", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=3600000, exit_value_usd=None, normalize_note="월 $300K * 12."),
"cal-ai": dict(domain_category="헬스/라이프스타일", team_size_bucket="4+",
    founder_background="developer", founder_experience="mixed",
    revenue_annual_usd_est=30000000, exit_value_usd=None,
    normalize_note="소스마다 $24M~$40M ARR로 상이, 중간값 계열인 $30M 사용. MyFitnessPal 인수가는 비공개."),
"cluely": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="2-3",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=5200000, funding_usd=20300000,
    normalize_note="자체 주장 ARR $7M은 실제로 $5.2M로 확인됨(과장 논란) — 확인된 수치 사용."),
"marc-lou-portfolio": dict(domain_category="AI 코딩/개발툴", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=1032000, normalize_note="본인 뉴스레터(2026-01-04) 공개 2025년 실제 연 매출 $1,032,000을 그대로 사용 — 종전 '월 $100K+ 연환산 $1.2M' 추정치를 1차 출처 실측값으로 교체(2026-08-11 수동조사)."),
"tweethunter-taplio": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=1000000, exit_value_usd=10000000,
    normalize_note="12개월 ARR $1M 달성 후 약 $10M 규모로 매각 보도(매각가는 별도 필드)."),
"lovable": dict(domain_category="AI 코딩/개발툴", team_size_bucket="4+",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=100000000, valuation_usd=6600000000,
    normalize_note="'한달간 매출 $100M 추가'라는 표현이 ARR 증가분인지 월매출인지 소스가 불명확 — 최댓값 추정치로 표기, 낮게 잡으면 ARR $30M(출시 4개월 시점)."),
"bolt-new": dict(domain_category="AI 코딩/개발툴", team_size_bucket="4+",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=40000000, normalize_note="5개월 시점 ARR 약 $40M."),
"cursor": dict(domain_category="AI 코딩/개발툴", team_size_bucket="4+",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=2000000000, valuation_usd=60000000000,
    normalize_note="ARR $2B(2026-02 보도)를 연 매출 추정치로 사용. valuation은 2026-06-16 SpaceX 합병계약상 인수대가 $60B(전액 주식) — 2026-08-11 현재 규제 승인 대기로 클로징 미완료, 종전 표기 $29.3B(2025-11 라운드)에서 갱신."),
"wave-ai": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=7000000, normalize_note="2026-02 기준 연매출 확인치."),
"ben-broca": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="unknown", founder_experience="unknown",
    revenue_annual_usd_est=10000000, funding_usd=30000000,
    normalize_note="'연 $10M 궤도'는 목표치이지 확정 실적 아님, 참고용."),
"deep-personality": dict(domain_category="컴패니언/엔터테인먼트", team_size_bucket="2-3",
    founder_background="unknown", founder_experience="serial",
    revenue_annual_usd_est=132000, normalize_note="첫 30일 $11K를 단순 연환산(성장 중이라 과소추정 가능)."),
"dreamgf": dict(domain_category="컴패니언/엔터테인먼트", team_size_bucket="unknown",
    founder_background="unknown", founder_experience="unknown",
    revenue_annual_usd_est=1440000, normalize_note="월 $120K * 12."),
"appalchemy": dict(domain_category="AI 코딩/개발툴", team_size_bucket="solo",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=120000, normalize_note="MRR $10K * 12."),
"launch-fast": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=360000, normalize_note="현재 MRR $30K * 12."),
"sleek-design": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=120000, normalize_note="MRR $10K * 12."),
"habit-pixel": dict(domain_category="헬스/라이프스타일", team_size_bucket="solo",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=12000,
    normalize_note="MRR $1K * 12. ai_tools 백필(2026-08-12): 1차 출처에서 창업자 본인 1인칭 발화 3건 확인 — \"I used Claude Code to have it extract everything into localizable strings\", \"I asked Claude Code to simply translate the key values in the localization files (JSON)\", \"I have a checklist which Claude Code mantains\". 단 용도가 **로컬라이제이션 워크플로에 한정**돼 확인됐다(문자열 추출·번역·구현 체크리스트 유지). 앱 전체를 Claude Code로 만들었다는 근거는 아니므로 '도구로 만든 사례'로 과대 서술하지 말 것."),
"subscribr": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=744000, normalize_note="MRR $62K * 12 (1년차 실적 $500K와 유사)."),
"samuel-rondot-portfolio": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=360000, normalize_note="포트폴리오 합계 월 $28-35K * 12."),
"lancer": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=300000, normalize_note="현재 MRR $25K * 12."),
"creator-buddy": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="non-developer", founder_experience="unknown",
    revenue_annual_usd_est=300000, normalize_note="ARR $300K 확인치."),
"vibed-agents": dict(domain_category="AI 코딩/개발툴", team_size_bucket="solo",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=108000, normalize_note="MRR $9K * 12."),
"plinq": dict(domain_category="헬스/라이프스타일", team_size_bucket="unknown",
    founder_background="non-developer", founder_experience="unknown",
    revenue_annual_usd_est=456000, normalize_note="ARR $456K 확인치."),
"klar": dict(domain_category="교육", team_size_bucket="2-3",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=130000,
    normalize_note="ARR $130K — 창업자(Isabel Storgårds) LinkedIn 본인 공개(2026). 초기 2차 출처의 €130K는 오기로 확인, USD 원문 채택. 출시 1개월 시점 수치라 지속성 미확인."),
"quicktables": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="4+",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=129600, exit_value_usd=None,
    normalize_note="ARR €120K(출시 8주, 창업자 exit 포스트 원문), EUR→USD 1.08 적용. 2026-03 인수, 금액 비공개. 창업자 명단은 출처별 상이(Øresund는 Jaleel Miles+Kevin Sandmark 표기)."),
"appbilchat": dict(domain_category="AI 코딩/개발툴", team_size_bucket="unknown",
    founder_background="unknown", founder_experience="serial",
    revenue_annual_usd_est=None, normalize_note="매출 비공개."),
"gendy": dict(domain_category="컴패니언/엔터테인먼트", team_size_bucket="unknown",
    founder_background="unknown", founder_experience="serial",
    revenue_annual_usd_est=888888, normalize_note="월 1억원, KRW→USD 1350 적용 후 연환산."),
"relic-ai": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="2-3",
    founder_background="developer", founder_experience="unknown",
    revenue_annual_usd_est=88888, normalize_note="월 1,000만원, KRW→USD 1350 적용 후 연환산."),
"trend-widget": dict(domain_category="커뮤니티/미디어", team_size_bucket="solo",
    founder_background="developer", founder_experience="unknown",
    revenue_annual_usd_est=None,
    normalize_note="매출 비공개(광고+구독 라이브). 다운로드 2만+/DAU 4천+은 창업자 자진신고 — Play 설치 버킷은 1,000+에 불과, 대부분 iOS 추정. 앱스토어 1위는 뉴스 카테고리 한정."),
"my-askai": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="2-3",
    founder_background="non-developer", founder_experience="unknown",
    revenue_annual_usd_est=480000,
    normalize_note="$40K MRR × 12 (2025-07 Indie Hackers 창업자 인터뷰 원문). 기존 KRW 환산치(월 5천만원) 폐기, USD 원문 채택."),
"formula-bot": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=500000,
    normalize_note="$500K ARR(2024)·$42K+ MRR(2025) — Starter Story·IH 창업자 본인 인터뷰. 웹상의 $220K/월 류 애그리게이터 수치는 본인 발언과 모순되어 배제. 기존 KRW 환산치 폐기."),
"ai-coding-consultancy": dict(domain_category="B2B 대행/컨설팅", team_size_bucket="2-3",
    founder_background="unknown", founder_experience="unknown",
    revenue_annual_usd_est=None,
    normalize_note="매출 비공개(2차 출처의 $78K/4개월 수치는 원출처 불명으로 배제). MVP 40+건은 본인 사이트 기준(2차 기사의 45+에서 교정)."),
"anything": dict(domain_category="AI 코딩/개발툴", team_size_bucket="2-3",
    founder_background="developer", founder_experience="unknown",
    revenue_annual_usd_est=2000000, valuation_usd=100000000,
    normalize_note="출시 2주 시점 ARR $2M(초기 급성장 구간, 유지 여부 불확실)."),
"simon-berg-portfolio": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="unknown", founder_experience="serial",
    revenue_annual_usd_est=None,
    normalize_note="신규 벤처 매출 비공개. 이전 회사 Ceros는 ARR $60M까지 성장(참고용, 이 사례의 매출 아님)."),
# ── 2026-08-10 정기 리서치 1회차 반영분 ──
"kleo": dict(domain_category="커머스/마케팅", team_size_bucket="4+",
    founder_background="mixed", founder_experience="unknown",
    revenue_annual_usd_est=744000,
    normalize_note="$62K MRR × 12 (2025-12 창업자 IH 발화 스냅샷). 기존 6만 유저 확장의 재런칭이라 'from $0' 프레이밍 주의. 제3자 검증 없음·런칭 수치 공개 분쟁 존재 → medium 상한."),
"superx": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="mixed", founder_experience="serial",
    revenue_annual_usd_est=276000,
    normalize_note="$23K MRR × 12 (2026-02 창업자 IH 인터뷰, 본인 트윗 성장 궤적 $2K→$17K→$23K로 교차 확인). 월 스냅샷 연환산 추정치."),
"imaginary-space": dict(domain_category="B2B 대행/컨설팅", team_size_bucket="unknown",
    founder_background="unknown", founder_experience="unknown",
    revenue_annual_usd_est=1200000,
    normalize_note="월 $100K × 12. 출처는 Lovable 공식 비디오(벤더 마케팅) + 본인 LinkedIn 교차 — medium 상한."),
"lumoo": dict(domain_category="AI 이미지/영상 생성", team_size_bucket="2-3",
    founder_background="unknown", founder_experience="unknown",
    revenue_annual_usd_est=756000,
    normalize_note="ARR €700K, EUR→USD 1.08 적용. 유일한 발화자가 Lovable CEO(엔젤 투자자)라 이해관계 있는 수치 — 창업자 본인 발화 확보 전까지 low 유지."),
"stoppr": dict(domain_category="헬스/라이프스타일", team_size_bucket="solo",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=126000,
    normalize_note="앱 매출 월 ~$10.5K × 12 (2026-05 자가보고). 2025-11 주력 앱 퇴출 후 하락 추세(RevenueCat 연동 트래커 기준 단일 앱 MRR $1.4K, 2026-08) — 스냅샷 시점 주의. 플랫폼 리스크 표본."),
"rightblogger": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="mixed", founder_experience="serial",
    revenue_annual_usd_est=350000, ingested_at="2026-08-12",
    normalize_note="region '미국'은 팀 3인이 콜로라도(Ryan)·미주리(Andy)·플로리다(운영 총괄)로 원격 분산된 것을 국가 단위로 축약한 값이다. 회사 about 페이지는 Ryan을 'Los Angeles'로 적어 본인 X·ryrob 신고(콜로라도 Salida)와 충돌하며, 애그리게이터의 LA 표기도 이 페이지 유래로 보인다 — 최신·구체 자기신고를 채택했다. 본인 발화 '$350k ARR'(2026-07-01)을 그대로 사용. **÷12 파생을 어느 방향으로도 하지 말 것** — 같은 $350K를 IH 인터뷰는 'ARR'(전향 런레이트), 본인 사이트 ryan.biz는 '$350K TTM Revenue'(과거 12개월 실적)로 적어 지표명이 불일치한다. 크기는 두 본인 채널로 뒷받침되나 라벨은 신뢰 불가. IH 헤드라인·스탯박스의 'MRR $29K'는 편집부 3인칭 역산값($350K÷12=$29,167)이라 배제했다 — 본문에서 1인칭은 ARR뿐이고 3인칭이 MRR을 말한다. 도구는 **기술 공동창업자 Andy Feliciotti** 블로그(2026-07-26) 'running Claude Code as my main coding tool' — 유통 담당 창업자(Ryan) 계정에는 언급이 없다. 2023 MVP는 SaaS 보일러플레이트+OpenAI API였고 Claude Code는 2025~2026 지속 개발 도구이므로 '처음부터 바이브코딩'이 아니라 **개발 워크플로가 AI 도구로 이전된** 사례. ryrob.com 블로그 수익(월 $30K+)은 별개 사업체이므로 병기 금지. 성장 동력이 12년 축적 오디언스(월 독자 50만·이메일 30만)라는 조건이 빠지면 재현 불가능한 성공이 재현 가능해 보인다."),
"leadverse": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=39600, ingested_at="2026-08-12",
    normalize_note="MRR $3.3K × 12 (본인 발화 2026-08-11). **측정 시점 주의** — Stripe 검증 스냅샷이 2026-07-16 08:57(Reddit API 회수 당일)에 멈춘 'last 30 days $3,230'과 사실상 동일하고 IH 인터뷰가 그 사건을 한 줄도 언급하지 않아, 측정은 2026-07 중순일 개연성이 높다. 2026-07-16경 Reddit이 API 키 4개를 예고 없이 전량 회수해 핵심 기능이 정지했고(당시 유료 130명+) **복구 방법에 대한 본인 발화는 미확보**다 — stoppr(Apple 앱 퇴출)와 같은 플랫폼 리스크 표본. ARPU $25.4는 유료 130명 중 약 30명이 커스텀 플랜(가격 자가조정)이라 정상 범위다. 최초 가격은 **€9/€14(EUR)**였고 약 1개월 후 USD 전환 — 후보 최초 기재의 '$9/$14'는 통화 오류였다. ai_tools는 unknown 유지: 본인 발화는 'GPT Pro 5x and Claude Max 5x' **구독 사실**뿐이고 코딩에 썼다는 행위 발화가 없다(ninjapear는 둘 다 있어 pass였다)."),
"ramsri-portfolio": dict(domain_category="교육", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=72000, ingested_at="2026-08-12",
    normalize_note="본인 발화 범위 '월 $6k~$7k MRR'의 **하한** $6,000 × 12 = $72K를 사용. 헤드라인성 '$6.5K'는 범위 중간값 파생이라 배제. **이 합산액은 1인 매출이 아니다** — Supermeme.ai가 3인 공동창업(Sanjeev NC·Nico Botha·Ramsri)이고 개인 귀속분은 원문에서 분해 불가하다. 분해 가능한 유일한 수치는 Questgen 누적 $150K USD(4년). 2025년 정점 총 ARR $100K에서 현재 연환산 $72~84K로 **하락 추세**. **유지·확장형 — 기원 2022(스코프 창 밖), 창 안 근거는 AiArtist.io 2026-02 단독 런칭 + \"nowadays, I use tools like Claude Code to vibe code and add features\" 현재형 발화**(RESEARCH_PIPELINE.md §0.5 가드레일 2조건 충족, 첫 적용 사례). domain은 매출 앵커인 Questgen(문제 생성) 기준이며 포트폴리오에 이미지·밈 생성이 섞여 있다. 전부 자기보고이며 결제사 검증 없음."),
"jonathan-geiger-portfolio": dict(domain_category="AI 코딩/개발툴", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=92880, ingested_at="2026-08-12",
    normalize_note="2026-07 월매출 $7,740 × 12 (본인 2026-08-01 X 결산). **매각 전 실적이며 현재 런레이트가 아니다** — 2026-08-06 SocialKit 매각으로 잔존 제품은 PostPeer 단독이므로 매각 후 런레이트는 약 $48K/yr($3,998×12) 수준. PostPeer MRR은 자기보고($2,661/112구독, 2026-07-29)와 Polar API 검증($1,989/79구독, 2026-08-11)이 어긋나 단일 값으로 쓸 수 없어 병기했다 — 단가는 $23.8 vs $25.2로 정합하므로 괴리는 구독 건수 정의 차이로 보인다. SocialKit 누적매출 본인 주장 $23,120은 LemonSqueezy API 검증 $14,730과 +57% 어긋나므로 단정 표기 금지. 참고로 총매출 지표에서는 본인 클레임이 검증치보다 낮다(-12%) — '과장'이 아니라 MRR 산정 정의 불일치."),
"sergiu-chiriac-portfolio": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=120000, ingested_at="2026-08-12",
    normalize_note="본인 일반진술 '경상 월 $10K 초과' × 12 = $120K를 하한으로 사용. **2026-07 최고치 $20,500을 연환산하지 않았다** — 일회성 구매 중심이라 월 변동이 크고(본인 발화 \"My revenue varies monthly because most of my products are one-time purchases\") 최고치 연환산은 부풀리기다. 더 중요하게 **이 총액은 제품 매출이 아니다** — 2026-07 구성의 38.5%($7,900)가 제휴 수입이고 $2,500은 제품명 비공개 앱이다. 이름이 특정된 자사 제품 매출은 $9,821(47.9%)에 그친다. 본인 표기 총액 $20,500과 항목 합 $20,221이 $279 어긋나며 원문에 5번째 항목은 없다 — 정상 반올림이 아니고 목표 달성을 위한 상향 유인도 없다($20,221도 이미 본인 $20K 목표 초과). IH 일반진술의 발화 시점은 불확정(게재 2026-08-06이나 본문 'Last month $15.7k'가 7월 결산과 불일치해 작성은 2026-07 이전). 도메인 분류 참고: scope-judge는 '메이커 툴/유통' 신설을 권고했으나 단일 사례 카테고리를 피해 '커머스/마케팅'으로 뒀다 — marc-lou·superx·kleo·launch-fast 등 '인디메이커에게 파는' 사례군을 함께 재분류할 때 반영할 것."),
"ninjapear": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=180000, ingested_at="2026-08-12",
    normalize_note="월 총매출 $15K × 12 (2026-05 실적, 본인 발화). **연환산은 정렬용 기계 계산이며 본인 ARR 주장이 아니다** — 크레딧 종량 충전을 포함한 gross라 MRR이 아니고, 본인이 밝힌 ARR은 2026-03 시점 $66K(실적)와 $1M(목표)뿐. 런칭 2026-01-30이므로 $15K는 4개월차 수치. region '싱가포르'는 Nubela Pte. Ltd. 법인 소재지 기준이며 창업자 본인 거주지 발화는 미확보. 이전 회사 Proxycurl의 ARR $10M은 별건이라 합산하지 않음. 창업자가 이전 exit 2건과 초기 암호화폐 투자로 '수익 압박 없이 무기한 운영 가능'하다고 발화(2026-07) — 매출 램프 해석 시 참고."),
}

def bucket(v):
    if v is None:
        return "unknown"
    if v < 100_000:
        return "<100K"
    if v < 1_000_000:
        return "100K-1M"
    if v < 10_000_000:
        return "1M-10M"
    return "10M+"

out = []
for c in raw:
    e = ENRICH.get(c["id"], {})
    merged = dict(c)
    merged.update(e)
    merged["revenue_bucket"] = bucket(e.get("revenue_annual_usd_est"))
    merged.setdefault("exit_value_usd", None)
    merged.setdefault("funding_usd", None)
    merged.setdefault("valuation_usd", None)
    merged["tool_question_probed"] = c["id"] in TOOL_PROBED
    # 기본값은 최초 일괄 적재일. 이후 추가되는 사례는 ENRICH에 ingested_at을 넣어
    # 실제 반영일로 덮는다 — app.js의 신규 배지가 이 값으로 계산되므로, 전부 같은
    # 날짜면 신규 사례가 방문자에게 새것으로 보이지 않는다.
    merged["ingested_at"] = e.get("ingested_at", "2026-08-10")
    out.append(merged)

with open("data/cases.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(out)} enriched cases to data/cases.json")
missing = [c["id"] for c in out if c["id"] not in ENRICH]
print("Missing enrichment:", missing)
