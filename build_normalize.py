import json

raw = json.load(open("data/raw_cases.json", encoding="utf-8"))

# ---- Controlled vocab ----
# domain_category, team_size_bucket, founder_background(dev/non-dev/mixed/unknown),
# founder_experience(first-time/serial/unknown), revenue_annual_usd_est (int or None)

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
    revenue_annual_usd_est=1200000, normalize_note="포트폴리오 월 $100K+ 시기 기준 연환산."),
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
    revenue_annual_usd_est=None, valuation_usd=29300000000,
    normalize_note="매출 비공개, 투자 밸류에이션만 확인됨."),
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
    revenue_annual_usd_est=12000, normalize_note="MRR $1K * 12."),
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
    merged["ingested_at"] = "2026-08-10"
    out.append(merged)

with open("data/cases.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(out)} enriched cases to data/cases.json")
missing = [c["id"] for c in out if c["id"] not in ENRICH]
print("Missing enrichment:", missing)
