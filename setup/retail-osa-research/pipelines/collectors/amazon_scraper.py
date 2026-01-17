#!/usr/bin/env python3
"""
Amazon 리뷰 데이터 수집 스크립트

⚠️ 주의사항:
1. Amazon의 Terms of Service를 준수해야 합니다
2. robots.txt를 확인하고 존중해야 합니다
3. 적절한 rate limiting을 사용해야 합니다 (최소 2-3초)
4. User-Agent를 명시해야 합니다
5. 상업적 사용 시 Amazon Product Advertising API 사용 권장

법적 고려사항:
- 개인 연구/교육 목적: 일반적으로 허용
- 상업적 사용: Amazon API 사용 필수
- 대량 스크래핑: 금지될 수 있음

대안:
- Amazon Product Advertising API (공식)
- 공개 데이터셋 활용
- Kaggle 등에서 Amazon 리뷰 데이터셋 찾기

타겟 제품:
- Inventory management hardware
- Shelf cameras
- Barcode scanners
- Smart shelf systems
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup


class AmazonScraper:
    """Amazon 리뷰 데이터 수집기"""

    def __init__(self, output_dir: str):
        """
        Args:
            output_dir: 출력 디렉토리 경로
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.base_url = "https://www.amazon.com"

        # HTTP 세션 설정
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

        # Rate limiting 설정 (초) - Amazon은 엄격하므로 더 긴 delay
        self.request_delay = 3

        print("[OK] Amazon scraper initialized")
        print("[WARN] Make sure to comply with Amazon's Terms of Service")
        print("[INFO] Consider using Amazon Product Advertising API instead")

    def check_robots_txt(self) -> str:
        """
        robots.txt 확인

        Returns:
            robots.txt 내용
        """
        try:
            robots_url = f"{self.base_url}/robots.txt"
            response = self.session.get(robots_url, timeout=10)
            response.raise_for_status()

            print(f"[OK] Retrieved robots.txt from {robots_url}")
            return response.text

        except Exception as e:
            print(f"[ERROR] Failed to retrieve robots.txt: {e}")
            return ""

    def search_products(
        self,
        query: str,
        category: str = None
    ) -> List[Dict[str, str]]:
        """
        제품 검색

        Args:
            query: 검색 쿼리
            category: 카테고리 (optional)

        Returns:
            검색된 제품 리스트 (ASIN, 제목, URL)
        """
        print(f"\n[INFO] Searching Amazon for: {query}")

        # ⚠️ 실제 구현 시 Amazon API 사용 권장
        print(f"[WARN] This is a placeholder - use Amazon API for production")

        products = []

        return products

    def collect_product_reviews(
        self,
        asin: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        특정 제품의 리뷰 수집

        Args:
            asin: Amazon Standard Identification Number
            limit: 최대 리뷰 수

        Returns:
            수집된 리뷰 리스트
        """
        print(f"\n[INFO] Collecting reviews for ASIN: {asin}")

        reviews = []

        # ⚠️ 실제 구현 시 주의사항:
        # 1. robots.txt 확인
        # 2. rate limiting 준수 (최소 2-3초)
        # 3. CAPTCHA 처리 필요할 수 있음
        # 4. IP 차단 위험 있음
        # 5. Amazon API 사용 강력 권장

        print(f"[WARN] Actual scraping may violate Amazon ToS")
        print(f"[INFO] Use Amazon Product Advertising API instead")

        return reviews

    def parse_review_html(self, html: str) -> Dict[str, Any]:
        """
        리뷰 HTML 파싱

        Args:
            html: 리뷰 HTML 문자열

        Returns:
            파싱된 리뷰 데이터
        """
        soup = BeautifulSoup(html, 'lxml')

        review_data = {
            'review_id': None,
            'asin': None,
            'title': None,
            'rating': None,
            'body': None,
            'verified_purchase': False,
            'helpful_count': 0,
            'reviewer_name': None,
            'review_date': None,
            'collected_at': datetime.now().isoformat()
        }

        # 실제 파싱 로직은 Amazon HTML 구조에 따라 구현
        # Amazon은 자주 HTML 구조를 변경하므로 유지보수 어려움

        return review_data

    def generate_mock_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        테스트용 모의 데이터 생성

        ⚠️ 실제 데이터 수집 전까지 사용
        실제 수집 시에는 Amazon API 사용 또는 공개 데이터셋 활용

        Returns:
            모의 리뷰 데이터
        """
        print("\n[WARN] Generating mock data - NOT real Amazon reviews")
        print("[INFO] This is for testing the pipeline only")

        mock_reviews = {
            'inventory_scanner_general': [
                {
                    'review_id': 'mock_amz_001',
                    'asin': 'B0MOCK001',
                    'product_name': 'Wireless Barcode Scanner',
                    'title': 'Good scanner but needs better software',
                    'rating': 4.0,
                    'body': 'The hardware is solid but the inventory tracking software is basic. Would love automated shelf monitoring instead of manual scanning.',
                    'verified_purchase': True,
                    'helpful_count': 45,
                    'reviewer_name': 'Small Store Owner',
                    'review_date': '2024-11-20',
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                },
                {
                    'review_id': 'mock_amz_002',
                    'asin': 'B0MOCK001',
                    'product_name': 'Wireless Barcode Scanner',
                    'title': 'Time-consuming to scan every item',
                    'rating': 3.0,
                    'body': 'Works fine but still requires manual scanning of every shelf. Takes too much time for daily inventory checks.',
                    'verified_purchase': True,
                    'helpful_count': 32,
                    'reviewer_name': 'Convenience Store Manager',
                    'review_date': '2024-10-15',
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                },
                {
                    'review_id': 'mock_amz_003',
                    'asin': 'B0MOCK002',
                    'product_name': 'Smart Shelf Sensor',
                    'title': 'Expensive for small stores',
                    'rating': 3.5,
                    'body': 'The technology is impressive but the price per shelf is too high for independent retailers. Needs more affordable option.',
                    'verified_purchase': True,
                    'helpful_count': 28,
                    'reviewer_name': 'Retail Entrepreneur',
                    'review_date': '2024-09-30',
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                },
                {
                    'review_id': 'mock_amz_004',
                    'asin': 'B0MOCK002',
                    'product_name': 'Smart Shelf Sensor',
                    'title': 'Installation is complicated',
                    'rating': 3.0,
                    'body': 'Good concept but installation requires technical expertise. Not practical for small business owners to set up themselves.',
                    'verified_purchase': True,
                    'helpful_count': 19,
                    'reviewer_name': 'Store Owner',
                    'review_date': '2024-08-12',
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                }
            ]
        }

        print(f"[OK] Generated {sum(len(reviews) for reviews in mock_reviews.values())} mock reviews")

        return mock_reviews

    def save_results(
        self,
        results: Dict[str, List[Dict[str, Any]]],
        filename: str = None
    ) -> Path:
        """
        수집 결과 저장

        Args:
            results: 제품별 리뷰 리스트
            filename: 출력 파일명 (기본값: reviews_YYYYMMDD_HHMMSS.json)

        Returns:
            저장된 파일 경로
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"reviews_{timestamp}.json"

        output_path = self.output_dir / filename

        total_reviews = sum(len(reviews) for reviews in results.values())

        output_data = {
            'collected_at': datetime.now().isoformat(),
            'source': 'amazon',
            'total_products': len(results),
            'total_reviews': total_reviews,
            'data': results
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        print("\n" + "="*60)
        print(f"[OK] Results saved to: {output_path}")
        print(f"  Total products: {len(results)}")
        print(f"  Total reviews: {total_reviews}")
        print("="*60)

        return output_path


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='Amazon 리뷰 데이터 수집')
    parser.add_argument(
        '--output',
        default='../../data/raw/amazon',
        help='출력 디렉토리'
    )
    parser.add_argument(
        '--asin',
        help='특정 제품만 수집 (ASIN)'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='모의 데이터 생성 (테스트용)'
    )

    args = parser.parse_args()

    # 수집기 초기화
    scraper = AmazonScraper(output_dir=args.output)

    # robots.txt 확인
    robots = scraper.check_robots_txt()
    print("\n[INFO] Amazon robots.txt preview:")
    print("-" * 60)
    print(robots[:500] if robots else "Could not retrieve robots.txt")
    print("-" * 60)

    # 데이터 수집
    if args.mock:
        print("\n[INFO] Running in MOCK mode - generating test data")
        results = scraper.generate_mock_data()
    elif args.asin:
        reviews = scraper.collect_product_reviews(args.asin)
        results = {args.asin: reviews}
    else:
        # 기본 모드: mock 데이터 생성
        print("\n[WARN] No ASIN specified, generating mock data")
        print("[INFO] Use --mock flag explicitly or provide --asin")
        results = scraper.generate_mock_data()

    # 결과 저장
    output_path = scraper.save_results(results)

    print(f"\n[OK] Collection complete!")
    print(f"\n[IMPORTANT] For production use:")
    print("  1. Use Amazon Product Advertising API")
    print("  2. Or use publicly available datasets:")
    print("     - Kaggle Amazon Reviews")
    print("     - Amazon Customer Reviews Dataset (AWS)")
    print("  3. Respect Amazon's Terms of Service")


if __name__ == '__main__':
    main()
