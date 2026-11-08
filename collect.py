import requests
import json
from pathlib import Path
from datetime import datetime, timezone

# 1. API 주소
url = "https://api.fda.gov/drug/label.json"

# 2. 검색 조건
params = {
    "search": (
        "effective_time:[20261001 TO 20261031] "
        "AND (openfda.application_number:NDA* "
        "OR openfda.application_number:BLA*)"
    ),
    "limit": 3
}

# 3. HTTP GET 요청
response = requests.get(
    url,
    params=params,
    timeout=15
)

# 4. 응답 확인
print("요청 URL:", response.url)
print("HTTP 상태 코드:", response.status_code)

# 5. 오류가 있으면 예외 발생
response.raise_for_status()

# 6. JSON 응답을 Python 객체로 변환
data = response.json()

# 7. 수집 결과 확인
results = data.get("results", [])

print("수집 건수:", len(results))

for label in results:
    print("------------------")
    print("SET ID:", label.get("set_id"))
    print("버전:", label.get("version"))
    print("날짜:", label.get("effective_time"))
    print("신청번호:", label.get("openfda", {}).get("application_number"))

# 8. 수집 시각 기록 (UTC)
collected_at = datetime.now(timezone.utc).isoformat()

# 9. 원본 저장 구조
raw_data = {
    "collection_meta": {
        "source": "openFDA",
        "url": response.url,
        "collected_at": collected_at,
        "search": params["search"],
        "limit": params["limit"],
        "result_count": len(results)
    },
    "results": results
}

# 10. data 폴더 생성
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# 11. JSON 파일 저장
output_path = data_dir / "raw.json"

with output_path.open("w", encoding="utf-8") as f:
    json.dump(
        raw_data,
        f,
        ensure_ascii=False,
        indent=2
    )

print("원본 저장 완료:", output_path)
