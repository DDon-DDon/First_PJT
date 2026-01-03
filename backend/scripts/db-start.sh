#!/bin/bash

# 똔똔 PostgreSQL 데이터베이스 시작 스크립트

set -e

echo "🚀 똔똔 PostgreSQL 데이터베이스 시작 중..."

# Docker가 실행 중인지 확인
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker가 실행되고 있지 않습니다. Docker를 먼저 실행해주세요."
    exit 1
fi

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# Docker Compose로 PostgreSQL 실행
docker-compose up -d postgres

echo "⏳ PostgreSQL 헬스체크 대기 중..."

# PostgreSQL이 준비될 때까지 대기
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if docker-compose exec -T postgres pg_isready -U donedone > /dev/null 2>&1; then
        echo "✅ PostgreSQL이 준비되었습니다!"
        echo ""
        echo "📊 연결 정보:"
        echo "  Host: localhost"
        echo "  Port: 5432"
        echo "  Database: donedone"
        echo "  User: donedone"
        echo "  Password: donedone123"
        echo ""
        echo "🔗 Connection String:"
        echo "  postgresql+asyncpg://donedone:donedone123@localhost:5432/donedone"
        echo ""
        echo "💡 로그 확인: docker-compose logs -f postgres"
        echo "💡 중지: docker-compose down"
        echo "💡 pgAdmin: http://localhost:5050 (admin@donedone.local / admin)"
        exit 0
    fi

    attempt=$((attempt + 1))
    echo "  대기 중... ($attempt/$max_attempts)"
    sleep 2
done

echo "❌ PostgreSQL 시작 실패 (타임아웃)"
docker-compose logs postgres
exit 1
