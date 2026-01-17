#!/usr/bin/env python3
"""
G2 리뷰 데이터 수집 스크립트

⚠️ 주의사항:
1. 이 스크립트는 연구/교육 목적으로만 사용되어야 합니다
2. G2의 Terms of Service를 준수해야 합니다
3. robots.txt를 확인하고 존중해야 합니다
4. 적절한 rate limiting을 사용해야 합니다
5. 상업적 사용 전 G2의 승인이 필요할 수 있습니다

대안:
- G2 API 사용 (유료)
- 공개 데이터셋 활용
- 직접 리뷰 요청

타겟 제품 카테고리:
- Inventory Management Software
- Retail Analytics
- Shelf Monitoring Solutions
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, quote

import requests
from bs4 import BeautifulSoup


class G2Scraper:
    """G2 리뷰 데이터 수집기"""

    def __init__(self, output_dir: str):
        """
        Args:
            output_dir: 출력 디렉토리 경로
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.base_url = "https://www.g2.com"

        # HTTP 세션 설정
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (research bot for academic purposes)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
        })

        # Rate limiting 설정 (초)
        self.request_delay = 3

        print("[OK] G2 scraper initialized")
        print("[WARN] Make sure to comply with G2's Terms of Service")

    def check_robots_txt(self) -> str:
        """
        robots.txt 확인

        Returns:
            robots.txt 내용
        """
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            response.raise_for_status()

            print(f"[OK] Retrieved robots.txt from {robots_url}")
            return response.text

        except Exception as e:
            print(f"[ERROR] Failed to retrieve robots.txt: {e}")
            return ""

    def search_products(
        self,
        category: str,
        query: str = None
    ) -> List[Dict[str, Any]]:
        """
        제품 검색

        Args:
            category: 카테고리 (예: 'inventory-management')
            query: 검색 쿼리 (optional)

        Returns:
            검색된 제품 리스트
        """
        print(f"\n[INFO] Searching G2 for category: {category}")

        # ⚠️ 실제 구현 시 G2 API 사용 또는 승인 필요
        # 여기서는 데이터 구조만 정의

        products = []

        # 예시 데이터 구조
        # 실제로는 HTML 파싱 또는 API 호출 필요
        print(f"[WARN] This is a placeholder - actual scraping requires authorization")

        return products

    def collect_product_reviews(
        self,
        product_slug: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        특정 제품의 리뷰 수집

        Args:
            product_slug: G2 제품 slug (예: 'shopify')
            limit: 최대 리뷰 수

        Returns:
            수집된 리뷰 리스트
        """
        print(f"\n[INFO] Collecting reviews for product: {product_slug}")

        reviews = []

        # ⚠️ 실제 구현 시 주의사항:
        # 1. robots.txt 확인
        # 2. rate limiting 준수
        # 3. ToS 확인
        # 4. JavaScript 렌더링 필요 시 Selenium 사용

        print(f"[WARN] Actual scraping requires G2 authorization")
        print(f"[INFO] Consider using G2 API or public datasets instead")

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

        # 예시 파싱 로직 (실제 HTML 구조에 맞게 수정 필요)
        review_data = {
            'review_id': None,
            'title': None,
            'rating': None,
            'pros': None,
            'cons': None,
            'body': None,
            'reviewer_role': None,
            'company_size': None,
            'industry': None,
            'posted_date': None,
            'verified': False,
            'helpful_count': 0,
            'collected_at': datetime.now().isoformat()
        }

        # 실제 파싱 로직은 G2의 HTML 구조에 따라 구현
        # 예시:
        # review_data['title'] = soup.find('h3', class_='review-title').text.strip()

        return review_data

    def collect_inventory_management_reviews(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        인벤토리 관리 소프트웨어 리뷰 수집

        Returns:
            제품별 리뷰 리스트
        """
        print("="*60)
        print("Starting G2 review collection for inventory management")
        print("="*60)

        # 타겟 제품 목록 (예시)
        target_products = [
            'shopify',
            'lightspeed-retail',
            'square-pos',
            'vend',
            'cin7'
        ]

        results = {}

        for product_slug in target_products:
            print(f"\n[INFO] Processing: {product_slug}")

            # ⚠️ 실제 수집은 승인 후 구현
            reviews = self.collect_product_reviews(product_slug, limit=50)
            results[product_slug] = reviews

            # Rate limiting
            time.sleep(self.request_delay)

        return results

    def generate_mock_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        테스트용 모의 데이터 생성

        ⚠️ 실제 데이터 수집 전까지 사용
        실제 수집 시에는 이 메서드를 제거하고 실제 스크래핑 로직 사용

        Returns:
            모의 리뷰 데이터
        """
        print("\n[WARN] Generating mock data - NOT real G2 reviews")
        print("[INFO] This is for testing the pipeline only")

        mock_reviews = {
            'inventory_management_general': [
                {
                    'review_id': 'mock_001',
                    'product_name': 'Generic Inventory Software',
                    'title': 'Good but expensive for small retail',
                    'rating': 3.5,
                    'pros': 'Good features, reliable',
                    'cons': 'Too expensive for small stores, complex setup',
                    'body': 'The software works well but pricing is aimed at large retailers. Small businesses struggle with the cost.',
                    'reviewer_role': 'Store Owner',
                    'company_size': '1-10 employees',
                    'industry': 'Retail',
                    'posted_date': '2024-11-15',
                    'verified': True,
                    'helpful_count': 12,
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                },
                {
                    'review_id': 'mock_002',
                    'product_name': 'Generic Inventory Software',
                    'title': 'Manual counting still required',
                    'rating': 3.0,
                    'pros': 'Integration with POS',
                    'cons': 'Still need manual shelf checks, no automated detection',
                    'body': 'We still have to manually count shelves every day. The system does not detect out-of-stock automatically.',
                    'reviewer_role': 'Operations Manager',
                    'company_size': '11-50 employees',
                    'industry': 'Convenience Store',
                    'posted_date': '2024-10-22',
                    'verified': True,
                    'helpful_count': 8,
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
            'source': 'g2',
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

    parser = argparse.ArgumentParser(description='G2 리뷰 데이터 수집')
    parser.add_argument(
        '--output',
        default='../../data/raw/g2',
        help='출력 디렉토리'
    )
    parser.add_argument(
        '--product',
        help='특정 제품만 수집 (G2 slug)'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='모의 데이터 생성 (테스트용)'
    )

    args = parser.parse_args()

    # 수집기 초기화
    scraper = G2Scraper(output_dir=args.output)

    # robots.txt 확인
    robots = scraper.check_robots_txt()
    print("\n[INFO] Please review robots.txt before proceeding:")
    print("-" * 60)
    print(robots[:500] if robots else "Could not retrieve robots.txt")
    print("-" * 60)

    # 데이터 수집
    if args.mock:
        print("\n[INFO] Running in MOCK mode - generating test data")
        results = scraper.generate_mock_data()
    elif args.product:
        reviews = scraper.collect_product_reviews(args.product)
        results = {args.product: reviews}
    else:
        results = scraper.collect_inventory_management_reviews()

    # 결과 저장
    output_path = scraper.save_results(results)

    print(f"\n[OK] Collection complete!")
    print(f"\n[REMINDER] If using real data:")
    print("  1. Ensure you have authorization from G2")
    print("  2. Respect rate limits and ToS")
    print("  3. Consider using G2 API for commercial use")


if __name__ == '__main__':
    main()
