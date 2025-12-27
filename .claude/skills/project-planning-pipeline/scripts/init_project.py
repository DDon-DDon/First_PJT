#!/usr/bin/env python3
"""
프로젝트 기획 파이프라인 폴더 구조 초기화 스크립트

사용법:
    python init_project.py <project_name> [--domain <domain_name>] [--path <output_path>]

예시:
    python init_project.py retail-osa-research --domain small_retail_osa --path ./projects
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def create_directory_structure(base_path: Path, project_name: str, domain: str):
    """프로젝트 디렉토리 구조 생성"""

    directories = [
        "config/schema",
        "data/raw/trends",
        "data/raw/crawl",
        "data/normalized",
        "data/features",
        "data/reports",
        "pipelines/collectors/scrapy_spiders/research_scraper/spiders",
        "pipelines/normalizers",
        "pipelines/analyzers",
        "pipelines/reporters/templates",
        "scripts",
        "logs",
    ]

    project_path = base_path / project_name

    for directory in directories:
        (project_path / directory).mkdir(parents=True, exist_ok=True)
        print(f"Created: {project_path / directory}")

    return project_path


def create_config_files(project_path: Path, domain: str):
    """설정 파일 생성"""

    # keywords.seed.json
    keywords_config = {
        "version": "v1",
        "domain": domain,
        "keywords": [
            {
                "keyword_id": f"kw_{domain}_example",
                "text": "example keyword",
                "lang": "en",
                "geo": "KR",
                "tags": ["example"],
                "intent": "problem_space",
                "priority": 3,
                "created_at": datetime.now().isoformat()
            }
        ]
    }

    with open(project_path / f"config/keywords.seed.{domain}.v1.json", "w", encoding="utf-8") as f:
        json.dump(keywords_config, f, indent=2, ensure_ascii=False)

    # sources.v1.json
    sources_config = {
        "version": "v1",
        "sources": [
            {
                "source_id": "src_google_trends",
                "type": "api_like",
                "base_url": "https://trends.google.com/trends/",
                "allowed": True,
                "notes": "Use trends web UI or pseudo API"
            },
            {
                "source_id": "src_example_blog",
                "type": "web",
                "base_url": "https://example.com/blog/",
                "allowed": "unknown",
                "notes": "Check ToS/robots before crawling"
            }
        ]
    }

    with open(project_path / "config/sources.v1.json", "w", encoding="utf-8") as f:
        json.dump(sources_config, f, indent=2, ensure_ascii=False)

    # crawl_policies.v1.json
    crawl_policies = {
        "version": "v1",
        "policies": {
            "default_delay": 2,
            "concurrent_requests": 8,
            "retry_times": 3,
            "robotstxt_obey": True,
            "user_agent": "ResearchBot/1.0 (+research@example.com)"
        },
        "compliance_checklist": [
            "robots.txt 확인",
            "ToS(이용약관) 검토",
            "수집 목적/범위 문서화",
            "rate limit 설정",
            "PII 최소 수집"
        ]
    }

    with open(project_path / "config/crawl_policies.v1.json", "w", encoding="utf-8") as f:
        json.dump(crawl_policies, f, indent=2, ensure_ascii=False)

    print("Created config files")


def create_scrapy_settings(project_path: Path):
    """Scrapy 설정 파일 생성"""

    settings_content = '''# Scrapy settings for research_scraper project

BOT_NAME = "research_scraper"

SPIDER_MODULES = ["research_scraper.spiders"]
NEWSPIDER_MODULE = "research_scraper.spiders"

# Crawl responsibly
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 8

# Feed exports
FEEDS = {
    "../../data/raw/crawl/%(name)s.jsonl": {
        "format": "jsonlines",
        "encoding": "utf8",
        "overwrite": False,
    }
}

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "../../logs/scrapy.log"
'''

    settings_path = project_path / "pipelines/collectors/scrapy_spiders/research_scraper/settings.py"
    with open(settings_path, "w", encoding="utf-8") as f:
        f.write(settings_content)

    # items.py
    items_content = '''import scrapy


class DocItem(scrapy.Item):
    """크롤링된 문서 아이템"""
    doc_id = scrapy.Field()
    source_id = scrapy.Field()
    url = scrapy.Field()
    retrieved_at = scrapy.Field()
    title = scrapy.Field()
    published_at = scrapy.Field()
    author = scrapy.Field()
    language = scrapy.Field()
    content_text = scrapy.Field()
    keyword_refs = scrapy.Field()
    tags = scrapy.Field()
'''

    items_path = project_path / "pipelines/collectors/scrapy_spiders/research_scraper/items.py"
    with open(items_path, "w", encoding="utf-8") as f:
        f.write(items_content)

    # __init__.py files
    init_paths = [
        "pipelines/collectors/scrapy_spiders/research_scraper/__init__.py",
        "pipelines/collectors/scrapy_spiders/research_scraper/spiders/__init__.py",
    ]
    for init_path in init_paths:
        (project_path / init_path).touch()

    print("Created Scrapy settings")


def create_script_files(project_path: Path):
    """실행 스크립트 생성"""

    scripts = {
        "run_all.sh": '''#!/bin/bash
# 전체 파이프라인 실행
set -e

./run_trends.sh
./run_crawl.sh
./run_normalize.sh
./run_analyze.sh
./run_report.sh

echo "Pipeline completed!"
''',
        "run_trends.sh": '''#!/bin/bash
# 트렌드 데이터 수집
cd ../pipelines/collectors
python trends_collector.py
''',
        "run_crawl.sh": '''#!/bin/bash
# 웹 크롤링 실행
cd ../pipelines/collectors/scrapy_spiders
scrapy crawl blogs_spider
''',
        "run_normalize.sh": '''#!/bin/bash
# 데이터 정규화
cd ../pipelines/normalizers
python normalize_docs.py
python dedupe_urls.py
python extract_evidence_cards.py
''',
        "run_analyze.sh": '''#!/bin/bash
# 분석 실행
cd ../pipelines/analyzers
python pain_point_mining.py
python keyword_trend_scoring.py
''',
        "run_report.sh": '''#!/bin/bash
# 리포트 생성
cd ../pipelines/reporters
python build_reports.py
'''
    }

    for filename, content in scripts.items():
        script_path = project_path / "scripts" / filename
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(content)
        script_path.chmod(0o755)

    print("Created script files")


def create_readme(project_path: Path, project_name: str, domain: str):
    """README.md 생성"""

    readme_content = f'''# {project_name}

데이터 기반 프로젝트 기획 검증 파이프라인

## 도메인
- **Domain**: {domain}
- **생성일**: {datetime.now().strftime("%Y-%m-%d")}

## 폴더 구조
```
{project_name}/
├── config/          # 설정 파일 (키워드, 소스, 크롤링 정책)
├── data/
│   ├── raw/         # 원본 데이터
│   ├── normalized/  # 정규화된 데이터
│   ├── features/    # 분석 결과
│   └── reports/     # 생성된 리포트
├── pipelines/       # 데이터 처리 파이프라인
├── scripts/         # 실행 스크립트
└── logs/            # 로그 파일
```

## 실행 방법
```bash
cd scripts
./run_all.sh
```

## 참고
- [분석 방법론](../references/analysis_methodology.md)
- [기술 구현 가이드](../references/tech_implementation_guide.md)
'''

    with open(project_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("Created README.md")


def main():
    parser = argparse.ArgumentParser(description="프로젝트 기획 파이프라인 초기화")
    parser.add_argument("project_name", help="프로젝트 이름")
    parser.add_argument("--domain", default="default_domain", help="도메인 이름")
    parser.add_argument("--path", default=".", help="출력 경로")

    args = parser.parse_args()

    base_path = Path(args.path)
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"Initializing project: {args.project_name}")
    print(f"Domain: {args.domain}")
    print(f"Path: {base_path}")
    print("-" * 40)

    project_path = create_directory_structure(base_path, args.project_name, args.domain)
    create_config_files(project_path, args.domain)
    create_scrapy_settings(project_path)
    create_script_files(project_path)
    create_readme(project_path, args.project_name, args.domain)

    print("-" * 40)
    print(f"✅ Project initialized at: {project_path}")
    print(f"   Next: Edit config/keywords.seed.{args.domain}.v1.json")


if __name__ == "__main__":
    main()