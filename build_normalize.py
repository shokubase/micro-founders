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
    # 2026-08-13 잔여 후보 5건 3렌즈 검증 통과분.
    # bazzly/jobric/ai-toolbox는 프로브 결과가 unknown이지만 '찾아봤다'는 사실은 기록한다 —
    # 이 플래그는 ai_tools가 채워졌는지가 아니라 우리가 실제로 캐물었는지를 재는 값이다.
    "bazzly", "idm", "jobric", "ai-toolbox", "erik-aronesty-portfolio",
    # 2026-08-13 재심 통과분 — 전부 2026-08-11에 '도구 언급 없음 = fail'로 기각됐던 건이다.
    # 넷 중 셋에서 실제로는 도구 발화가 존재했다(1차 출처를 한 편만 봤던 것이 원인).
    "zigpoll", "setter-ai", "artmvstd", "leadmore-ai",
    # 2026-08-13 차단 소스 재심 통과분. caret은 도구 발화가 전멸했으나 창업자 GitHub
    # 산출물까지 훑어 심사했으므로 probed다 (결과는 unknown).
    "wrestle-ai", "caret", "lunair",
    # 2026-08-13 코퍼스 감사분. 게이트 뒤 섹션 + 본인 X·YouTube까지 훑었다.
    # 결과는 unknown 유지지만 '찾아봤다'는 사실은 기록한다.
    "samuel-rondot-portfolio",
}

# 백필 기록.
#
# samuel-rondot-portfolio (2026-08-13 감사로 갱신 — 아래 옛 판단은 폐기됐다):
#   [폐기] "'Leveraging AI tools to build' 섹션이 IH 페이월 안에 있어 접근 불가,
#          계정 생성은 하지 않으므로 not_attempted" → **계정은 필요 없었다.**
#          raw HTML에 전문이 있다(§"IH 가입 장벽은 렌더링에만 걸린다").
#   [유지] IH 본문의 Claude/Cursor 언급이 전부 제3자 댓글이라는 판단은 맞다.
#          댓글 123건의 작성자 핸들을 전수 추출해도 samuelrdt는 0건이다 —
#          도구 질문은 두 번 왔고 **창업자는 답하지 않았다.** 무응답은 부정이 아니다
#          (faceless-video는 질문에 *답하며* 거부해서 fail이었다).
#   [신규] 게이트 뒤 섹션은 제목과 내용이 반대였다. 제목은 편집자가 붙였고 창업자
#          문장은 전부 가정법이다("If I had to start again today, I would use AI tools
#          heavily... It would have saved me months"). §0.6 테스트 1 적용 결과
#          부정항은 AI 도구가 아니라 "AI가 코딩 학습을 대체한다"는 명제이고,
#          같은 글이 두 섹션 뒤에서 스스로 취소한다("Use AI coding tools to build
#          your MVP fast").
#   [신규] §0.6 테스트 2로 본인 YouTube(@samuelrdt)를 열었더니 **채널 자체가
#          바이브코딩 프로세스 채널**이었다("Built 100% with Capacity.so",
#          "the entire app was built in just a couple of days using AI").
#          단 대상이 데모 앱이고 자사 도구(Capacity.so) 마케팅 맥락이라
#          매출 제품 제작 귀속은 여전히 미확인 → ai_tools는 unknown 유지.

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
    revenue_annual_usd_est=336000, ingested_at="2026-08-13",
    normalize_note="**유지·확장형 — 기원 2017(인스타그램 자동화 서비스, WordPress+인력 대행, 창 밖)이나 매출 축은 창 안이다**: StoryShort 2024-08-06 착수(TrustMRR Stripe 연동 레코드), Capacity ~2024-12 착수(본인 X 2025-12-08 \"@BaptisteStuder_ and I spent a year building\"). 연환산은 IH(2025-12) 본문 1인칭 합계 월 $28K × 12 = $336K. **종전 $360K는 2025-07 시점 $35K를 섞은 범위 상단값이라 폐기했다 — $35K→$28K는 증가가 아니라 감소다.** 범위 표기가 감소 추세를 위장하고 있었다. **단품 검증치:** StoryShort는 Stripe 연동 MRR $21,024 / 최근 30일 $21,117 / 활성구독 376 / 누적 $541,898(TrustMRR, 2026-08-13 갱신). 단가 $55.9로 공개 티어 $39~$199 범위 내 정합. useArtemis·Capacity는 TrustMRR 미등재(404)라 검증치 없음. **X 바이오 수치($15k/$25k/$1.6k)는 IH 기사와 역방향으로 엇갈려(Capacity는 낮고 useArtemis는 높다) 갱신 시점 불명 — 채택하지 않았다.** **[중대] StoryShort가 2025-12-18부터 호가 $1.2M로 매각 리스팅 중이다**(오퍼 20건, 30일 성장 -7.5%) — exit_status 해석 시 반영할 것. **ai_tools 감사 결과(2026-08-13):** IH의 'Leveraging AI tools to build' 섹션은 **제목이 편집자(James Fleischmann) 작성**이고 창업자 문장은 전부 가정법이다(\"If I had to start again today, I would... It would have saved me months\"). §0.6 테스트 1 적용 — 부정항은 AI 도구가 아니라 '**AI가 코딩 학습을 대체한다**'는 명제이고(대비 구조가 `learn to code` ↔ `even with AI coding tools`), 함의의 시간 범위도 \"early on... I didn't know how to code\"인 창 밖 기원기다. 게다가 **같은 글이 두 섹션 뒤에서 스스로 취소한다** — \"Use AI coding tools to build your MVP fast.\" 댓글 123건 작성자를 전수 추출해도 창업자는 0건이라 **도구 질문 2건에 답하지 않았다**(faceless-video는 답하며 거부해서 fail이었다 — 무응답은 부정이 아니다). §0.6 테스트 2로 본인 YouTube(@samuelrdt)를 열었더니 **채널 자체가 바이브코딩 프로세스 채널**이고 1인칭 발화가 다수다(\"Built 100% with Capacity.so\", \"the entire app was built in just a couple of days using AI\"). **그럼에도 ai_tools는 unknown을 유지한다 — 그 발화의 대상이 데모 앱이고 자사 도구 Capacity.so 마케팅 맥락이며, 매출의 90%+를 만드는 StoryShort·useArtemis를 AI 도구로 만들었다는 근거는 없다. 이 사례를 'AI 도구로 만든 매출 제품'으로 과대 서술하지 말 것.** region 확정: X 프로필 location 'Lyon, France' + TrustMRR country FR. **불일치 기록** — IH 본문의 \"I lived in France, right next to the Swiss border\"는 과거형이며 옵티션 시절 거주지다(리옹은 스위스 국경 인접이 아니다)."),
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
"lunair": dict(domain_category="AI 이미지/영상 생성", team_size_bucket="solo",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=100000, ingested_at="2026-08-13",
    normalize_note="본인 발화 ARR $100K를 그대로 사용. **출시 60일차 연환산 런레이트이지 실현 매출이 아니다.** 결제사 검증 없음(TrustMRR 미등재), 약 6개월 된 값이라 현재형 표기 금지. 구독($29.70/월)에 일회성 Top-Up($38.70)이 섞이는 모델이라 ARR 지표 자체가 무르다. **2026-08-10 기각 번복 건이고, 기각 사유였던 '세 갈래 수치 불일치'는 실재하는 모순이 아니라 벤더의 단위 탈락 1건이었다** — 창업자 원문은 전부 ARR인데 재유통되며 'ARR'이 떨어져 '$100k in revenue', 'hit $100k in 60 days', 슬러그 '50k in 30 days'가 됐다. 벤더 블로그는 **같은 글 안에서 자멸한다** — 'in revenue within the first 2 months'라 써놓고 다른 대목에서 'The immediate goal is clear: $100k ARR'이라 쓴다. '$8k MRR'도 $100,000÷12=$8,333 역산 의심. **[혼동 위험 최고] 본인 PH 글의 'A major VC committed $100K based on one deck'는 매출이 아니라 투자 커밋이다 — 매출액과 자릿수가 같으므로 절대 섞지 말 것.** 같은 이유로 **'완전 부트스트랩'이라 쓰면 안 된다**(벤더 CEO의 'fully bootstrapped'가 본인 발화와 충돌하며 본인 1인칭이 상위다). **ai_tools 근거는 벤더 채널이 아니다 — 화자가 아예 없는 런타임 지문이다.** app.lunair.ai 프로덕션 번들(8.0MB)에 `base44.functions.invoke` **157회**, `Base44-App-Id`·`base44_access_token`·`Base44Error` 문자열, HTML의 파비콘·OG가 `base44-prod` 버킷, `data-seo-source=\"builder\"`(오케스트레이터 직접 확인). 보강으로 창업자가 PH 런칭 shoutout에 직접 기입했고 그 시점(2026-02-15)이 벤더 블로그(2026-02-16)보다 **하루 앞선다**. **제품측 AI는 배제했다** — 번들의 InvokeLLM·agents 호출과 영상 생성 엔진은 제품이 AI를 쓰는 것이다. Notion도 제외(운영 도구). **이 창업자는 노코더가 아니다** — '14세부터 프로그래밍', 렌더링 엔진 자체 구현. '개발자가 인프라 층을 AI 빌더에 위임한' 유형으로 읽어야 오분류가 안 난다. **인접 사례 주의: `base44`(Maor Shlomo)가 코퍼스에 있으나 플랫폼 제공자 vs 그 위의 빌더로 층이 다르다. 다만 Maor가 Lunair 홍보 게시물의 화자이기도 하므로 두 사례가 서로의 출처로 순환 인용되지 않게 할 것.** 독립 매체 Calcalist(2026-04-16)는 금액을 일절 확인해주지 않는다."),
"wrestle-ai": dict(domain_category="헬스/라이프스타일", team_size_bucket="2-3",
    founder_background="non-developer", founder_experience="first-time",
    revenue_annual_usd_est=180000, ingested_at="2026-08-13",
    normalize_note="**최근 월별 $15K(2026-04) × 12를 썼다 — 정점이 아니라 최근값이다.** 본인 발화로 월별 시계열 전체가 확보된 드문 사례이고 궤적은 첫 달 $17K(2025-10) → $30K(12월) → **$40K 피크(2026-01)** → $28K → $20K → $15K(4월)다. setter-ai와 함께 하락 표본. **후보 최초 기재의 '월 $17,000'을 연환산하지 않았다** — 그건 첫 달 값이고, 더 중요하게 $8,000(월간 구독) + $9,000(그 달 결제된 연간 구독)의 **월 현금 합**이라 ×12하면 연간 플랜분이 매월 재발생한다고 가정하는 이중계상이 된다(연간 $9,000의 월 환산은 ÷12 ≈ $750). **미러 요약이 '첫 달/둘째 달'로 갈렸는데 원문 \"So 17,000 in the first month\"로 해소했다** — caret·artmvstd에 이은 요약 오염 세 번째다. **[내 오류] team_size '1인'이 반박됐다** — 본인 1인칭 \"I want to do this with you will be partners, like 50, 50\"이고 Rork 케이스 스터디도 독립 확인한다. 공동창업자 실명은 두 ASR 미러가 'Kaden Henshall'/'Kate and Henshaw'로 갈려 미확정(§0.6 ASR 규칙). **[내 오류] 'Fiverr 외주 $250'은 용도가 다르다** — 본인 발화는 인플루언서 아웃리치용 VA 채용이고, '프리랜스 개발자 $250'은 벤더(Rork) 서술뿐이다. ai_tools는 Rork 단독 — 본인 \"I built all these apps on Rourke... It's like an AI app builder. Like Replit? Exactly\"이며 ASR 'Rourke'는 패키지명 app.rork.wrestleai·벤더 케이스 스터디로 3중 확정. **ChatGPT는 제외** — 전사의 GPT 언급은 제품 백엔드 모델 질문에 대한 답이다. **Rork 벤더 수치는 본인 발화와 모순되므로 미채택**(벤더는 2026-02를 월 $39.4K라 했으나 본인은 \"it was like 28\"). gross/net 미확정 — \"Apple was holding 17 K that we're gonna get paid out in December\"로 보아 수수료 차감 전일 가능성. **다운로드 17,000건은 매출 $17,000과 자릿수가 같아 혼동 위험이 커 제거했다.** App Store id6753085689는 카피캣 가능성이 높으니 식별자는 id6751189075로 고정할 것. **2026-08-10 기각 번복 건** — 사유가 '원출처 URL 미확인'이었는데 Starter Story 에피소드는 실재했다. 증거 부재가 아니라 조사 미완이었다."),
"caret": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="4+",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=60000, ingested_at="2026-08-13",
    normalize_note="본인 발화 ARR $60K를 그대로 사용($60,000 × 1,350 = ₩81,000,000으로 자체 정합, 뉴스레터 부제 '3개월 만에 ARR 8,000만원'과 일치). **이 사례는 요약 모델이 죽였다가 살아난 건이다** — 기각 사유가 '6만인지 60만인지 확인 필요'였고 원문은 6만이었다. **요약 fetch가 자릿수를 10배 바꿨고 그 모순 때문에 15개월간 rejected였다.** 같은 날 artmvstd(댓글→창업자 1인칭)와 wrestle-ai(첫 달→둘째 달)에서도 요약 오염이 나왔다. **[가장 중요한 교정] 후보 최초 기재의 '바이브코딩으로 만든'은 근거가 없어 제거했다.** 인터뷰의 바이브코딩 발화는 사내 실험이다 — \"일부러 코드 하나도 안쓰고... 1시간 시간 제한 걸어놓고... 해커톤을 열어보려고\"에서 '일부러'·'시도'·'1시간 제한'·'해커톤' 네 표지가 전부 기본 워크플로로부터의 이탈을 가리키고, 질문 자체도 '팀이 자주 쓰는 AI 서비스'였지 제작 과정을 묻지 않았다. **단 §0.6 기준 부정 발화는 아니다** — '코드 하나도 안 쓰고'의 부정항은 직접 타이핑한 코드이며 오히려 '평소엔 사람이 코드를 쓴다'를 전제한다. 'Cursor for Email'도 이메일 제품 비유이지 도구 사용이 아니다. **도구 근거는 기사가 아니라 창업자 GitHub 산출물에서 나왔다** — 공동창업자 레포 hiddenest/awake는 README가 \"only while supported AI coding tools are actively progressing\"이고 claude-code·codex·cursor-agent·opencode를 감시 대상으로 명시한다(2026-07). CEO 레포 therne/opengmail에는 CLAUDE.md→AGENTS.md 에이전트 규칙 파일이 있다(2026-08). **발화 프로브가 전멸해도 산출물 프로브가 남는다**는 것이 이 건의 수확이다. **그럼에도 ai_tools는 unknown** — 그 산출물은 전부 2026년 Aside 시기이고 Caret 본체(2025-02, 2주 제작) 귀속은 미확인이다. team_size_bucket '4+'는 코퍼스 6건(cursor·lovable·bolt-new·cal-ai·quicktables·kleo)과 같은 층이며, 이 사례는 YC F25·프리시드 15억 원으로 아카이브 내 대형 층에 속한다. region은 setter-ai 선례대로 복합 표기(한국인 창업팀, 법인 At Your Side Inc. 샌프란시스코). **수치는 2025년 미팅노트 시기 스냅샷이고 제품은 이후 AI 브라우저 Aside로 피벗했다** — 현행 런레이트로 읽으면 안 된다. 2025-05 이후 15개월간 갱신 수치 없음. **동명이인 주의: 한국의 캐럿티브(Carrative)가 만든 오픈소스 바이브코딩 툴 '캐럿'은 전혀 다른 제품이며 검색에서 상위에 뜬다.**"),
"zigpoll": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=1500000, ingested_at="2026-08-13",
    normalize_note="본인이 직접 말한 런레이트 $1.5M을 그대로 사용($125K MRR × 12와 일치). **유지·확장형 — 기원 2018(창 밖, Shopify 앱 출시 2019-04-23), 창 안 근거는 Claude Code 에이전트 코딩 루프 1인칭 발화(2026-05-28) + MCP 플러그인 2026-02·OpenClaw 플러그인 2026-07·synthetic survey 기능 2026.** §0.5 두 번째 적용 사례다. **이 건은 2026-08-11에 잘못 기각됐다가 2026-08-13 재심에서 번복됐다** — 기각 근거였던 '본인 명시적 부정'이 문맥 오독이었다. 문제의 문장 \"I built the first version of Zigpoll myself with a code editor, not a budget\"는 섹션 제목이 **Funding himself**이고 인접 절이 전부 자본이다(\"cost far more time than money\", \"Nights and weekends were the real currency\", \"I've never taken outside money\", \"no VC, no angel\"). **부정된 항은 예산이지 AI 도구가 아니며 문장에 AI를 지시하는 토큰이 하나도 없다.** 더 결정적으로 5주 전 팟캐스트에 긍정 발화가 있었다 — \"take those trends and then pipe them through directly to Cloud Code in order to create action items and then execute on those action items... **You don't have to write the code anymore.**\" ('Cloud Code'는 음성 전사 산물이며 Claude Code다 — MCP와 병치, 자사 문서가 지원 클라이언트로 'Claude Code (CLI)' 명기, 본인 레포에 .claude-plugin 존재로 3중 확정.) **§0.5 조건 2가 최약 고리다** — GitHub 산출물이 기존 제품의 신규 표면이지 ramsri의 AiArtist.io 같은 독립 신규 제품이 아니고, 코어는 2019년 Express/Mongo 그대로라 리라이트도 아니다. 통과시킨 근거는 트윗 한 줄이 아니라 체계적 개발 루프이고 2026 상반기 +44% 성장이 그 루프와 동시대라는 점이다. **수치는 편집부 인포박스('Revenue $125K a month')가 아니라 본문 1인칭 문장에서 취했다** — 이 건은 두 값이 일치하지만 출처는 본문이어야 한다(rightblogger·ai-toolbox 선례). 전부 자기보고이며 결제사 검증 없음. region은 데이터 브로커 검색 요약뿐이라 미확정."),
"setter-ai": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=80328, ingested_at="2026-08-13",
    normalize_note="**Stripe API 검증 MRR $6,694 × 12.** 이 코퍼스에서 드물게 결제사 검증치를 그대로 쓴 건이다. **정점 대비 하락 사례** — 2025-07 $10K(자기보고) → 2026-08 $6,694(검증). 누적 $206,042(30개월)는 MRR과 병렬 표기 금지. 산술 교차검증: 2024-02 창업 후 30개월 누적 $206K는 '2024-08 붕괴($10K→$0, 약 $5,000 분쟁 포함) → 2025 $10K 회복 → 2026 $7K대' 궤적과 정합하며 **오히려 과거 $10K 주장을 뒷받침한다**. 유보: TrustMRR은 연결된 Stripe 계정만 반영하므로 별도 인보이스 셋업비($4k 등)가 있으면 검증치가 하한이다. **서술 주의 — '부분적 AI 보조'이지 'AI가 만든 제품'이 아니다.** 창업자는 13세부터 독학한 CS 전공 엔지니어이고 도구 발화가 나온 바로 그 영상에서 회의를 표한다: \"I've been partly vibe coding, partly using my own brain to implement that feature\" 직후 \"it doesn't really feel faster to do something if you vibe code\", \"I find it more enjoyable to just use my own brain.\" **사용을 긍정하면서 효용을 유보한 것이므로 zigpoll형 부정이 아니고 규칙상 pass다.** 코퍼스에 드문 유형이라 오히려 수집 가치가 있다. **2026-08-11 기각 번복 건** — 1회차는 borderline을 fail로 처리한 게 아니라 조사 범위 부족이었다(IH 기사 1편만 보고 창업자 YouTube 62편·GitHub·Substack을 열지 않았다). ai_tools에 'vibe coding'은 넣지 않았다(작업 방식이지 도구명이 아니다). v0도 제외 — 개인 사이드 앱(protein tracker)이지 Setter AI가 아니다. region은 1인칭 자기신고만 채택했고 Tracxn의 '오스트리아'는 발화와 모순되어 미채택. **별칭 워치리스트: Timo의 Jinni AI, Josef의 cardghost.com·LinkedIn 확장은 별도 사례이며 귀속 금지.**"),
"artmvstd": dict(domain_category="교육", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=264000, ingested_at="2026-08-13",
    normalize_note="MRR $22K × 12 (2025-12 자기보고). **gross/net 미상** — 스토어 수수료 15~30%와 UA 지출 차감 여부 불명이라 연환산은 상한으로 읽어야 한다. **8개월 된 값이고 2026년 수치는 미확인**(x.com이 HTTP 402로 차단 — 도구 한계이지 증거 부재가 아니다). $7K(2025-10) → $22K(2025-12) 3개월 3배는 학습 앱 시즌성으로 설명 가능하나 미검증. **2026-08-11 기각 번복 건이고, 기각 논거의 사실관계 자체가 틀렸다** — '광고 수익 모델이라 기존 사례군과 결이 다름'이라 적었으나 **광고 모델이 아니다**(본인 발화 \"95% of all subs are weekly\", \"more than 80% of revenue comes from subscriptions\"; Play 리스팅에 'Contains ads' 라벨 없음). 오인의 출처는 **IH 댓글 작성자 Lupus3000의 발언**(\"I went the publisher route... CAS runs the stack for me\")을 창업자 발언으로 옮긴 것이고, 그렇게 된 경로는 **요약 모델이 그 댓글을 창업자 1인칭처럼 돌려준 것**이다. 후보 파일의 stack 'CAS(광고 미디에이션)'도 같은 출처라 삭제했다. **화자 확인은 raw HTML 작성자 필드로만 할 것.** 도구 근거는 팟캐스트 1인칭 발화 — \"I just copy the project. So it's almost 90% of the same code... Then I asked Chad GPT corser to go through and then change it from chemistry to math\"(아이디어→앱스토어 제출 2시간). **Cursor는 ai_tools에 넣지 않았다** — 자막의 'corser'/'course store'가 Cursor의 ASR 오인식일 개연성은 높으나(같은 의미 자리에서 두 번 독립 오인식) 자동자막 판독만으로 도구명을 굳히지 않는다. ChatGPT는 같은 자막 내 'chat GPT' 정상 표기가 반복돼 확정. **미해결: 16:15·23:51 오디오 직접 청취.** region은 1인칭 확정(\"I'm based in Latia... Latvian EU account\"), 매출 단위 EUR 혼용과도 정합. founded_year 2025는 포트폴리오 전환 시점(본인 \"in February of this year\" 발화, 2025-12 기준)이며 개발자 활동 기원은 그 이전 — 다만 매출을 내는 산출물 30개가 전부 2025년 신규라 §0.5 표기는 불필요."),
"leadmore-ai": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=360000, ingested_at="2026-08-13",
    normalize_note="**월 $30K × 12 = $360K를 사용했고, 더 최근의 'ARR $1M'을 정렬용 값으로 쓰지 않았다.** 이유는 본인이 밝힌 산출법 때문이다 — \"The $1M ARR is based on a run rate calculation: **revenue from a recent day multiplied by 365**.\" 크레딧 종량제라 일 매출 분산이 구독제보다 크고 **기준일 선택 편향이 구조적**이다. sergiu에서 최고월($20,500) 연환산을 거부한 것과 같은 처리. 참고로 $30K/월 ≈ $986/일 → $1M/365 ≈ $2,740/일로 **2개월에 2.8배**인데, 본인이 동인 3개(지역별 가격제 폐지, 첫 구매 $9.9 인하, AEO 붐)를 제시하나 결제사 검증은 없다. **2026-08-11 기각 번복 건.** 기각 근거 둘 다 무효였다 — (1) '도구 언급 전무'는 현행 기준에서 borderline이고 (2) '대기업 엔지니어 출신이라 비개발자 유형이 아님'은 배제 사유가 아니다(코퍼스 51건 중 developer 배경이 최다이고 erik-aronesty는 25년차 CTO다). **[내 오류] ARR $1M을 '2차 출처 주장'으로 배제한 것도 오판정이었다** — 본인 IH 게시물이고 산출법까지 자진 공개했다. **본인 표기 착오 1건 기록**: 2026-02 글이 \"went from zero to around $30K ARR\"라 쓰는데 그 글 제목은 \"$30K MRR in 4 Months\"다. 12월 값은 월 $30K가 맞고 2월 글의 'ARR'이 오기다 — 그대로 옮기면 $30K ARR → $1M ARR(33배)이라는 허구가 만들어진다. **ai_tools unknown 유지** — 본인 발화에 'vibe coding'이 긍정 맥락으로 있으나(\"With vibe coding today, you can often ship a very basic MVP in one or two weeks\") **'you can'의 일반론이라 자기 빌드 귀속이 아니다**(bazzly는 \"Being a technical founder, AI gave me a big advantage\"로 1인칭 자기귀속이었다). region unknown 유지 — X가 '주로 중국어'라는 언급만으로 국가 단정 금지, X·LinkedIn 전부 HTTP 차단으로 미열람. **별건 리드: Vismore(vismore.ai, AEO 플랫폼)는 같은 창업자의 다른 제품이므로 별도 사례로 큐잉할 것.**"),
"bazzly": dict(domain_category="커머스/마케팅", team_size_bucket="2-3",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=90000, ingested_at="2026-08-13",
    normalize_note="본인 발화 월 총 $7.5K × 12 = $90K. **MRR이 아니다** — 본인이 구성을 스스로 분해했다: 경상 $5K + 플랫폼 내 일회성 결제 $2.5K. 연매출 추정에는 일회성도 실제 유입이므로 포함했으나 MRR로 표기하면 안 된다(ai-toolbox 라이프타임 배제 규칙과 같은 취지). 결제사 검증이 오히려 자기보고보다 **높다** — Stripe API 기준 MRR $6,781(본인 주장 $5K 대비 +36%), 지난 30일 $8,614. 과장 방향이 아니므로 $90K는 부풀린 값이 아니다. 괴리 원인은 MRR 정의 차이로 보인다(jonathan-geiger와 동일 유형). **ARPU 역산 함정 기록**: 검증 MRR $6,781 ÷ 활성구독 62 = $109.4로 단일 플랜 $99를 넘는데, 내가 처음 내린 '연간 플랜이나 상위 티어' 설명은 **틀렸다** — Bazzly에는 $99/월 단일 플랜만 있고 연간·상위 티어가 없다. 올바른 독법은 TrustMRR의 MRR 필드가 일회성 결제를 섞어 계산한다는 것, 즉 **애그리게이터의 MRR 정의 ≠ 창업자의 MRR 정의**다. team_size는 '2인'이나 지분 50% 파트너의 실명이 미공개이며 역할 분해도 확보되지 않았다. ai_tools unknown 유지 — 본인이 AI 활용을 긍정하지만 도구명을 특정하지 않았고, leadverse에 적용한 기준(구독 사실만으로는 부족)을 여기에도 동일하게 적용했다. **북마케도니아는 이 아카이브 첫 발칸 사례**다."),
"idm": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=20000, ingested_at="2026-08-13",
    normalize_note="월 25만엔 × 12 = 300만엔, 1 USD≈150 JPY 적용 → 약 $20,000. **이 아카이브 첫 일본 사례.** 하한을 택했다 — 더 최근 자가공개(2026-04)는 「月30万円弱のMRR」이지만 '弱'(미달)이라 점값이 없고, 2025-10의 25만엔은 명시 수치다. **원문 단어가 「収益化」다** — 売上도 MRR도 아니므로 gross/net이 확정되지 않는다. 매출로 단정하지 말 것. **[내 오류 기록] 후보 최초 기재의 「約25万円」 인용은 지정된 출처에 그 문자열이 없었다** — 서로 다른 두 note 기사를 섞었다. 실제 문장은 「月に25万円程度の収益化ができています」다. 또한 내가 '2차 출처'로 격하했던 30만엔 기술은 **같은 창업자 본인의 글**이므로 1차다. team_size_bucket solo는 iDM 제품 기준이며 **법인 전체 기준이 아니다** — 株式会社bubekichi는 스쿨 ShiftB·vibely·JS Gym 등을 병행하므로 순수 1인 회사가 아니다. 도구는 본인이 Claude Code·Cursor를 명시 발화했다."),
"jobric": dict(domain_category="생산성/업무도구 SaaS", team_size_bucket="solo",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=39600, ingested_at="2026-08-13",
    normalize_note="MRR $3,300 × 12 = $39.6K. **런칭 2개월차 수치의 연환산이라 런레이트 신뢰도가 낮다** — 2026-05-01 출시 후 2개월 미만이며 코호트 유지율 관측 구간이 없다. 두 시점(2026-06-26 IH, 2026-07-14 인터뷰)에서 같은 $3,300이 반복돼 **성장이 정체했거나 창업자가 같은 수치를 재사용했을 가능성**이 있는데 원문으로 구분 불가하다. ARPU 역산 $3,300÷80≈$41은 $29/$49 두 티어 사이라 정합한다. team_size_bucket은 solo — 프랙셔널 자문 4인을 더해 본인이 'six people'이라 표현하나 상시 인력이 아니고 본인 스스로 \"not everyone writes code\"라 단서를 달았다. region unknown 유지: eastbayexpress(베이에어리어) 기사가 유일한 지리 단서인데 본인 자기신고가 아니고 인용된 인물이 창업자인지도 확정되지 않았다 — 추정으로 채우지 않는다. ai_tools unknown: 스택은 상세히 공개하나 코딩 도구 발화가 없다."),
"ai-toolbox": dict(domain_category="AI 코딩/개발툴", team_size_bucket="2-3",
    founder_background="developer", founder_experience="first-time",
    revenue_annual_usd_est=120000, ingested_at="2026-08-13",
    normalize_note="'5-figure MRR'의 **하한** $10,000 × 12 = $120K. 범위 중간값($55K/월)을 쓰면 안 된다 — 창업자는 자릿수만 말했다. **IH 인포박스의 '>$10K a month'는 창업자 발화가 아니다**: 같은 박스가 공동창업 2인 사례를 'Founder: Adi Leviim' 단수로 적고 있어 편집부 메타데이터 필드임이 박스 내부 모순으로 증명된다 — rightblogger(인칭으로 식별)에 이은 편집부 필드 식별 두 번째 기법. **라이프타임·AppSumo 일회성 매출은 MRR에 합산 금지**이며 경상/일회성 구성비는 미공개다. **ai_tools unknown이지만 명시적 부정은 아니다** — 8개 면을 훑어 도구 언급을 찾지 못했고 기술 담당(Mohammad El-Esawi) 프로필을 별도 확인했다(rightblogger에서 유통 담당만 보고 borderline을 낸 전례를 피하기 위함). Adi Leviim이 자기 에세이에서 Claude Code 사용을 공개하지만 용도를 '초고 편집'으로 한정 명시하므로 **제품 코드 근거로 전용할 수 없다**. IH 본문의 'TypeScript with no UI framework'는 번들 크기 아키텍처 선택이며 저술 방식 진술이 아니다 — zigpoll의 도구 명시 부정과 성격이 다르다. **[내 오류] 'Infi Developments 기성 개발사' 우려는 반박됐다** — 두 창업자가 제품 출시와 같은 달(2024-09) 세운 자기 법인이다. **[내 오류] '인스타 팔로워 50만 유통 승계' 가설도 1차 출처에 없다** — IH 제목의 'existing user bases'는 개인 팔로워가 아니라 호스트 마켓플레이스의 기성 사용자 기반이며(본문 'searching a store with hundreds of millions of users, and we paid \\$5 to be in it') 실명 채널은 크롬 웹스토어 검색·서브레딧·AppSumo다. **'$15K+ MRR' 수치는 이 사례에 귀속 금지** — 별개 제품 Landy AI(3인) 것이다. 리브랜딩 alias 유지: ChatGPT Toolbox → AI Toolbox(2026-04). superpower-chatgpt는 유사 제품이나 2022년 말 제작으로 스코프 창 밖이어서 기각된 별건이다."),
"erik-aronesty-portfolio": dict(domain_category="커머스/마케팅", team_size_bucket="solo",
    founder_background="developer", founder_experience="serial",
    revenue_annual_usd_est=180000, ingested_at="2026-08-13",
    normalize_note="월 $15K × 12 = $180K. **경고 3중**: (1) 본인이 \"Most of that is not recurring\"이라 명시했으므로 MRR로 읽으면 안 된다 (2) 매출 70%가 여행 업종이라 계절성이 크다 (3) OnwardTravel이 $16 정액이나 '전액 발권은 선택'이어서 **대금 통과분 포함 여부(gross/net)가 원문에서 확정되지 않는다**. TrustMRR 미등재로 결제사 대조 불가. **[내 오류 — 산술 스크리닝 4연속 적중] 후보 최초 기재의 제품별 금액 $10.5K/$3K/$1.5K는 원문에 존재하지 않는다** — 창업자는 비율(70%/20%/10%)만 말했고 그 금액들은 총액×비율 파생값이다. '약 30개 중 매출 기여 3개'도 오류로, 실제 발화는 30개 이상에서 월 매출이 발생하며 상위 3개가 90%를 차지한다는 것이다. **개발도구 vs 런타임 쟁점 해소**: '런타임 나열' 가설의 근거였던 동거 항목 BoxPDF·LakeQL이 실은 본인 자작 OSS라 그 목록은 잡탕이고 동거 사실이 근거가 못 된다. 제작 역할을 못박는 1인칭 발화가 둘 있다 — \"Now, I can talk into my phone to launch a beta\" / \"An agent will build it in 20 minutes and provide it.\" 반대로 'Hermes+Gpt5.6 makes all the decisions'와 Logtura 로그 감시는 **운영 런타임이므로 ai_tools에서 제외**했다(섞으면 'AI를 씀 vs AI로 만듦' 구분선이 데이터에서 뭉개진다). 'Claude'를 Claude Code로 승격하지 않았다 — 원문이 분해하지 않는다. **founded_year 2026 확정**: 본인 '지난 4개월' 발화 창 안에 자작 라이브러리 repo 생성일 3건이 전부 들어온다(boxpdf 2026-05-14, boxpdf-html 05-17, lakeql 06-13). **스코프 포함 근거**: §0.4 기준은 도구·팀규모·수익화 세 개뿐이고 '수요 창출'은 없다. 코퍼스에 이미 수요편승형(Nomad List/RemoteOK, AI Directories, 실검 위젯)이 있으며, 잔존 트래픽 있는 폐기 도메인 인수가 수지 맞는 건 재구축 비용이 0에 수렴할 때뿐이라 오히려 바이브코딩 네이티브 전략이다. 회색지대(OnwardTravel)도 dreamgf·deep-personality·gendy 선례대로 게재하되 서술은 엄격 중립으로 — 홍보 동사 금지, 'dummy ticket'을 설명절 없이 쓰지 말 것(실체는 실제 PNR 홀드이며 위조 문서가 아니다), **합법이라고 단정하지 말 것**(관할·항공사 정책마다 다르다). natlawreview는 독립 보도가 아니라 자사 배포 보도자료여서 출처에서 뺐다. **별칭 워치리스트(재유입 방지)**: Q32 LLC / OnwardTravel / DirtSignal / PrismClip / BrandMochi / Free Birds Magazine — 개별 사이트가 단독 리드로 잡히면 신규가 아니라 이 사례다. 단 BizSnipe.com은 본인 제품인지 이용 툴인지 불명이라 귀속 금지. **승인자 플래그**: 매출 70%가 단일 업종에 묶여 항공사 정책·결제사 제한 변경 시 수치가 급변한다."),
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
