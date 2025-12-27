#!/bin/bash
# 분석 실행
cd ../pipelines/analyzers
python pain_point_mining.py
python keyword_trend_scoring.py
