#!/bin/bash

# 똔똔 개발 서버 실행 스크립트 (uv 기반)

set -e

echo "🚀 똔똔 개발 서버 시작 중 (using uv)..."

# backend 폴더 위치 파악 (스크립트 기준 상위 폴더)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# backend 폴더로 이동
cd "$BACKEND_DIR"

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. .env.example을 복사합니다..."
    cp .env.example .env
    echo "✅ .env 파일이 생성되었습니다. 필요시 수정해주세요."
fi

echo "✅ 개발 서버를 시작합니다..."
echo "📝 API 문서: http://localhost:8000/docs"
echo "📝 ReDoc: http://localhost:8000/redoc"
echo "💚 Health Check: http://localhost:8000/health"
echo ""

# uv run으로 서버 실행 (환경 자동 관리)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
