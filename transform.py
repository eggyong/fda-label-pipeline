import json
from pathlib import Path

# 리스트를 문자열로 변환하고 누락값을 처리
def join_list(value):
    if isinstance(value, list):
        return " | ".join(str(item) for item in value)
    return value if isinstance(value, str) else ""

# YYYYMMDD 형식을 YYYY.MM.DD로 변환
def format_date(value):
    if isinstance(value, str) and len(value) == 8 and value.isdigit():
        return f"{value[:4]}.{value[4:6]}.{value[6:8]}"
    return ""

# FDA 라벨 1건에서 필요한 필드만 추출
def transform_label(label):
    openfda = label.get("openfda") or {}

    return {
        "application_number": join_list(
            openfda.get("application_number")
        ),
        "set_id": label.get("set_id") or "",
        "version": label.get("version") or "",
        "effective_time": format_date(
            label.get("effective_time")
        ),
        "brand_name": join_list(openfda.get("brand_name")),
        "generic_name": join_list(openfda.get("generic_name")),
        "manufacturer_name": join_list(openfda.get("manufacturer_name")),
        "indications_and_usage": join_list(label.get("indications_and_usage"))
    }


def main():
    data_dir = Path("data")

    with (data_dir / "raw.json").open("r", encoding="utf-8") as f:
        raw_data = json.load(f)
    
    # 리스트 컴프리헨션
    labels = [
        transform_label(label)
        for label in raw_data["results"]
    ]

    with (data_dir / "labels.json").open("w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False, indent=2)

    print(f"가공 완료: {len(labels)}건")
    print("저장 위치:", data_dir / "labels.json")


if __name__ == "__main__":
    main()
