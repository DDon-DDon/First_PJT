#!/bin/bash

# 똔똔 개발 서버 실행 스크립트

set -e

echo "🚀 똔똔 개발 서버 시작 중..."

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# 가상환경 활성화 확인
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  가상환경이 활성화되지 않았습니다."
    echo "💡 활성화 방법: source backend/.venv/Scripts/activate"
    echo ""
    echo "자동으로 활성화를 시도합니다..."
    source backend/.venv/Scripts/activate || {
        echo "❌ 가상환경 활성화 실패"
        exit 1
    }
fi

# backend 폴더로 이동
cd backend

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

# Uvicorn으로 서버 실행 (Hot Reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
