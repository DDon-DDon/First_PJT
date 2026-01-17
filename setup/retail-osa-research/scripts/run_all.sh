#!/bin/bash
# 전체 파이프라인 실행
set -e

./run_trends.sh
./run_crawl.sh
./run_normalize.sh
./run_analyze.sh
./run_report.sh

echo "Pipeline completed!"
