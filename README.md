# FDA Drug Label Data Pipeline

openFDA API를 활용하여 의약품 라벨 데이터를 수집하고, 필요한 필드를 추출하여 JSON 파일로 저장하는 Python 기반 데이터 수집 실습 프로젝트입니다.

## 1. 프로젝트 개요

FDA에서 제공하는 공개 의약품 라벨 데이터를 수집하고, 원본 데이터 보존과 데이터 구조화 과정을 경험하는 것을 목표로 합니다.

**데이터 처리 흐름**

`openFDA API → Python requests → raw.json → 데이터 변환 → labels.json`

## 2. 기술 스택

- Python
- requests
- JSON
- pathlib

## 3. 데이터 수집

**사용 API**

https://api.fda.gov/drug/label.json

**검색 조건**

- 신청번호: NDA 또는 BLA
- 라벨 효력 발생일(`effective_time`): 2026-10-01 ~ 2026-10-31
- 수집 건수: 최대 3건
- HTTP 메서드: GET

Python의 `requests` 라이브러리를 사용하여 API를 호출합니다.

## 4. 데이터 저장 및 변환

### 원본 데이터 저장

API 응답에서 `results` 데이터를 추출하고, 수집 조건과 수집 시각을 `collection_meta`에 기록하여 `data/raw.json`에 저장합니다.

원본 데이터를 보존함으로써 API를 재호출하지 않고도 데이터 변환 작업을 다시 수행할 수 있도록 구성했습니다.
