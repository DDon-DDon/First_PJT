# retail-osa-research

데이터 기반 프로젝트 기획 검증 파이프라인

## 도메인
- **Domain**: small_retail_osa
- **생성일**: 2025-12-28

## 폴더 구조
```
retail-osa-research/
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
