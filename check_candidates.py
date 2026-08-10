"""후보 큐 검사: data/candidates/*.json 스키마 검증 + 기존 DB와 중복 검사.

사용: python3 check_candidates.py  (문제 없으면 exit 0)
"""
import json
import re
import sys
from pathlib import Path

CANDIDATES_DIR = Path("data/candidates")
CASES_FILE = Path("data/cases.json")

VALID_STATUS = {"pending_verification", "verified", "approved", "rejected", "merged"}
REQUIRED_TOP = {"id", "status", "discovered_at", "discovery_source", "case", "verification"}
REQUIRED_CASE = {"id", "founders", "product", "domain", "one_liner", "team_size",
                 "region", "revenue", "revenue_date", "exit_status", "stack",
                 "ai_tools", "founder_background", "business_model", "sources", "confidence"}
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []
warnings = []

existing_ids = set()
existing_products = set()
if CASES_FILE.exists():
    for c in json.load(open(CASES_FILE, encoding="utf-8")):
        existing_ids.add(c["id"])
        existing_products.add(c["product"].strip().lower())

candidate_files = sorted(CANDIDATES_DIR.glob("*.json")) if CANDIDATES_DIR.exists() else []
seen_ids = set()

for path in candidate_files:
    name = path.name
    try:
        cand = json.load(open(path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{name}: JSON 파싱 실패 — {e}")
        continue

    missing = REQUIRED_TOP - cand.keys()
    if missing:
        errors.append(f"{name}: 최상위 필드 누락 {sorted(missing)}")
        continue

    cid = cand["id"]
    if not ID_RE.match(cid):
        errors.append(f"{name}: id '{cid}' 는 kebab-case가 아님")
    if path.stem != cid:
        errors.append(f"{name}: 파일명과 id '{cid}' 불일치")
    if cid in seen_ids:
        errors.append(f"{name}: 후보 큐 내 id 중복")
    seen_ids.add(cid)

    if cand["status"] not in VALID_STATUS:
        errors.append(f"{name}: status '{cand['status']}' 는 허용값 아님 {sorted(VALID_STATUS)}")

    case = cand["case"]
    case_missing = REQUIRED_CASE - case.keys()
    if case_missing:
        errors.append(f"{name}: case 필드 누락 {sorted(case_missing)}")
    if case.get("id") != cid:
        errors.append(f"{name}: case.id 가 최상위 id와 불일치")

    # 기존 DB와 중복 (merged는 반영 완료 상태이므로 중복이 정상)
    if cand["status"] != "merged":
        if cid in existing_ids:
            errors.append(f"{name}: id '{cid}' 가 이미 data/cases.json에 존재")
        product = str(case.get("product", "")).strip().lower()
        if product and product in existing_products:
            warnings.append(f"{name}: 제품명 '{case['product']}' 이 기존 사례와 유사 — 중복 확인 필요")

    # 검증 상태 정합성
    ver = cand["verification"]
    if cand["status"] in {"verified", "approved", "merged"}:
        if not ver.get("verified_at"):
            errors.append(f"{name}: status={cand['status']} 인데 verification.verified_at 없음")
        if not ver.get("primary_sources"):
            errors.append(f"{name}: status={cand['status']} 인데 primary_sources 비어 있음")
    if cand["status"] == "rejected" and not ver.get("notes"):
        errors.append(f"{name}: rejected 인데 사유(verification.notes) 없음")

print(f"후보 {len(candidate_files)}건 검사")
for w in warnings:
    print(f"  WARN: {w}")
for e in errors:
    print(f"  ERROR: {e}")
if errors:
    sys.exit(1)
print("OK")
