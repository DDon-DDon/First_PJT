#!/bin/bash

# 똔똔 PostgreSQL 데이터베이스 중지 스크립트

set -e

echo "🛑 똔똔 PostgreSQL 데이터베이스 중지 중..."

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# Docker Compose로 PostgreSQL 중지
docker-compose down

echo "✅ PostgreSQL이 중지되었습니다."
echo ""
echo "💡 데이터는 보존되어 있습니다. 다시 시작하려면: ./scripts/db-start.sh"
echo "💡 데이터까지 삭제하려면: docker-compose down -v"
