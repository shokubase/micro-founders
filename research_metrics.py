#!/usr/bin/env python3
"""리서치 파이프라인 측정 지표.

"왜 사례가 N건뿐인가"를 손계산하지 않기 위한 스크립트.
핵심은 재포획률 — 새 실행에서 마주친 리드 중 이미 DB/큐에 있던 비율이다.
이 값이 높으면 그 층(stratum)은 포화된 것이고, 스코프 규칙을 완화해도
얻는 게 적다. 성장은 재포획률이 낮은 새 층에서 나온다.

사용법:
    python3 research_metrics.py                          # 코퍼스 현황만
    python3 research_metrics.py leads.txt                # + 재포획률 (한 줄에 리드 1건)
    python3 research_metrics.py leads.txt --as-of 2026-08-11
                                                         # 그 날짜 이후 발견된 후보를
                                                         # 인덱스에서 제외 (사후 재현용)
    python3 research_metrics.py --check "Setter AI"      # 리드 1건 중복 대조

--as-of가 왜 필요한가: 실행이 끝나고 신규 후보를 커밋한 뒤에 재포획률을 재면
그 후보들이 이미 인덱스에 있어서 항상 100%가 나온다. 실행 시작 시점의 코퍼스를
기준으로 재려면 그 실행에서 발견된 후보(discovered_at >= 기준일)를 빼야 한다.
"""
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
CASES = ROOT / "data" / "cases.json"
CANDIDATES = ROOT / "data" / "candidates"

# region 문자열이 정규화돼 있지 않아(예: "네덜란드 (발리 거주 노마드)" vs
# "네덜란드 (발리 거주)") 층 라벨로 쓰려면 앞부분 국가명만 떼어내야 한다.
_REGION_TRIM = re.compile(r"[(（].*$")


def norm_region(v):
    if not v or v == "unknown":
        return "unknown"
    base = _REGION_TRIM.sub("", str(v)).strip()
    base = base.replace(" 추정", "").strip()
    # "영국(Rob) / 프랑스(Tibo)" 같은 복수 표기는 첫 번째 국가로 귀속
    if "/" in base:
        base = base.split("/")[0].strip()
    return base or "unknown"


def norm_key(s):
    """제품명·창업자명 대조용 키. 대소문자·공백·기호·유니코드 폭 차이를 흡수."""
    s = unicodedata.normalize("NFKC", str(s)).lower()
    return re.sub(r"[^a-z0-9가-힣]", "", s)


def load():
    cases = json.loads(CASES.read_text())
    cands = []
    for f in sorted(CANDIDATES.glob("*.json")):
        cands.append(json.loads(f.read_text()))
    return cases, cands


def build_index(cases, cands, as_of=None):
    """리드 대조용 인덱스: 정규화 키 -> 소속(사례 id / 후보 상태).

    as_of가 주어지면 그 날짜 이후 발견된 후보는 제외한다 — 실행 시작 시점의
    코퍼스를 복원해 재포획률을 사후에도 정직하게 재기 위한 것.
    """
    if as_of:
        cands = [c for c in cands if (c.get("discovered_at") or "") < as_of]
    idx = {}

    def add(key, label):
        if key and len(key) >= 3:
            idx.setdefault(key, label)

    for c in cases:
        label = f"case:{c['id']}"
        add(norm_key(c["id"]), label)
        add(norm_key(c.get("product", "")), label)
        for f in c.get("founders") or []:
            add(norm_key(f), label)
    for c in cands:
        label = f"candidate:{c['id']}({c['status']})"
        add(norm_key(c["id"]), label)
        case = c.get("case") or {}
        add(norm_key(case.get("product", "")), label)
        for f in case.get("founders") or []:
            add(norm_key(f), label)
    return idx


def match_lead(lead, idx):
    """리드 문자열이 기존 항목과 겹치는지. 부분일치 허용(제품명이 문장에 섞여 옴)."""
    k = norm_key(lead)
    if not k:
        return None
    if k in idx:
        return idx[k]
    for key, label in idx.items():
        if key in k or k in key:
            return label
    return None


def corpus_report(cases, cands):
    print(f"=== 코퍼스 현황 ===")
    print(f"사례 {len(cases)}건 / 후보 {len(cands)}건")

    st = Counter(c["status"] for c in cands)
    print(f"후보 상태: {dict(st.most_common())}")

    print("\n--- 층(지역) 분포 ---")
    reg = Counter(norm_region(c.get("region")) for c in cases)
    for r, n in reg.most_common():
        print(f"  {r:<12} {n}")

    print("\n--- ai_tools 결측 ---")
    missing = [c["id"] for c in cases
               if not c.get("ai_tools") or c.get("ai_tools") == ["unknown"]]
    print(f"  {len(missing)}/{len(cases)}건: {', '.join(missing)}")

    print("\n--- confidence ---")
    print(f"  {dict(Counter(c.get('confidence') for c in cases).most_common())}")

    print("\n--- 기각 사유 분포 ---")
    lens = Counter()
    for c in cands:
        if c["status"] != "rejected":
            continue
        for item in (c.get("verification") or {}).get("checklist_passed") or []:
            if item.endswith(":fail"):
                lens[item] += 1
    print(f"  {dict(lens.most_common()) if lens else '(기각 후보 없음)'}")


def recapture_report(leads, idx, n1):
    print(f"\n=== 재포획률 ===")
    hits, misses = [], []
    for lead in leads:
        m = match_lead(lead, idx)
        (hits if m else misses).append((lead, m))

    n2 = len(leads)
    m = len(hits)
    print(f"이번 실행 고유 리드 {n2}건 / 재포획 {m}건 / 신규 {len(misses)}건")
    if n2:
        print(f"재포획률 {m / n2:.0%}")

    rate = m / n2 if n2 else 0

    if m == n2:
        print("전부 재포획 — 이 층은 포화. 새 층(언어권/소스)으로 옮길 것")
    elif m < 3 or rate < 0.2:
        # Lincoln-Petersen은 두 표본이 '같은 모집단'에서 나왔을 때만 성립한다.
        # 겹침이 거의 없다는 건 추정 정밀도가 낮다는 뜻이 아니라, 애초에
        # 다른 모집단을 보고 있다는 신호일 가능성이 크다 (예: 영어권 DB vs
        # 일본어권 리드 — 2026-08-12 실행에서 m=1로 440건이라는 무의미한 값이
        # 나왔고, 그 1건마저 일본 매체의 해외 사례 재요약이었다).
        print(f"재포획 {m}건뿐 — 모집단 추정 생략.")
        print("  * 겹침이 이만큼 적으면 같은 모집단이 아닐 가능성이 크다.")
        print("  * 새 층을 연 것이라면 정상. 그 층 안에서 표본이 쌓인 뒤 다시 재라.")
    else:
        # 유명 사례일수록 양쪽에 잡혀 중복이 부풀므로 이 값은 하한이다.
        est = n1 * n2 / m
        print(f"모집단 추정(하한) ≈ {est:.0f}건  [n1={n1}, n2={n2}, m={m}]")
        print("  * 동일 포획확률 가정이 깨져 실제값은 이보다 큼. 층별로 따로 셀 것")

    if misses:
        print("\n신규 리드:")
        for lead, _ in misses:
            print(f"  + {lead}")
    if hits:
        print("\n재포획 리드:")
        for lead, label in hits:
            print(f"  = {lead}  ->  {label}")


def main():
    argv = sys.argv[1:]
    cases, cands = load()

    # --check: 리드 1건 중복 대조 (Stage 1에서 검증 낭비를 막는 용도)
    if argv and argv[0] == "--check":
        if len(argv) < 2:
            print("사용법: research_metrics.py --check \"제품명 또는 창업자명\"",
                  file=sys.stderr)
            return 2
        idx = build_index(cases, cands)
        for lead in argv[1:]:
            hit = match_lead(lead, idx)
            print(f"{lead}  ->  {hit or 'NEW (기존 항목과 겹치지 않음)'}")
        return 0

    as_of = None
    if "--as-of" in argv:
        i = argv.index("--as-of")
        if i + 1 >= len(argv):
            print("--as-of 뒤에 날짜(YYYY-MM-DD)가 필요하다", file=sys.stderr)
            return 2
        as_of = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]

    corpus_report(cases, cands)

    if argv:
        path = Path(argv[0])
        if not path.exists():
            print(f"\n리드 파일 없음: {path}", file=sys.stderr)
            return 1
        leads = [l.strip() for l in path.read_text().splitlines()
                 if l.strip() and not l.startswith("#")]
        if as_of:
            print(f"\n(기준일 {as_of} — 그 이후 발견 후보는 인덱스에서 제외)")
        recapture_report(leads, build_index(cases, cands, as_of), len(cases))
    else:
        print("\n(리드 파일을 인자로 주면 재포획률도 계산)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
