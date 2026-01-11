import json
import os
import sys
from pathlib import Path

# 프로젝트 루트를 path에 추가
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app

def generate_openapi():
    """FastAPI 앱에서 OpenAPI JSON 스펙을 추출하여 파일로 저장합니다."""
    openapi_data = app.openapi()
    
    # docs 폴더 생성
    output_dir = Path(__file__).parent.parent / "docs" / "api"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "openapi.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ OpenAPI spec generated at: {output_path}")

if __name__ == "__main__":
    generate_openapi()
