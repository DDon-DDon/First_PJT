#!/bin/bash
# 데이터 정규화
cd ../pipelines/normalizers
python normalize_docs.py
python dedupe_urls.py
python extract_evidence_cards.py
