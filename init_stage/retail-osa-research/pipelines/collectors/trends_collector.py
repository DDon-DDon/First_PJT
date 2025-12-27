#!/usr/bin/env python3
"""
Google Trends 데이터 수집 스크립트

키워드 파일에서 키워드를 읽어 Google Trends 데이터를 수집합니다.
- Interest over time (시간별 관심도)
- Related queries (관련 검색어)
- Rising queries (급상승 검색어)
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from pytrends.request import TrendReq


class TrendsCollector:
    """Google Trends 데이터 수집기"""

    def __init__(self, config_path: str, output_dir: str):
        """
        Args:
            config_path: 키워드 설정 파일 경로
            output_dir: 출력 디렉토리 경로
        """
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # pytrends 초기화
        self.pytrends = TrendReq(
            hl='en-US',
            tz=360,
            timeout=(10, 25),
            retries=3,
            backoff_factor=0.5
        )

        # 키워드 로드
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.keywords = self.config['keywords']
        print(f"Loaded {len(self.keywords)} keywords from {self.config_path}")

    def collect_interest_over_time(
        self,
        keyword: str,
        geo: str = '',
        timeframe: str = 'today 12-m'
    ) -> pd.DataFrame:
        """
        특정 키워드의 시간별 관심도 수집

        Args:
            keyword: 검색 키워드
            geo: 지역 코드 (예: 'US', 'KR')
            timeframe: 시간 범위 (예: 'today 12-m', 'today 3-m', 'today 5-y')

        Returns:
            시간별 관심도 데이터프레임
        """
        try:
            self.pytrends.build_payload(
                [keyword],
                cat=0,
                timeframe=timeframe,
                geo=geo,
                gprop=''
            )

            df = self.pytrends.interest_over_time()

            if df.empty:
                print(f"  [WARN] No data for '{keyword}' in {geo or 'Worldwide'}")
                return pd.DataFrame()

            # isPartial 컬럼 제거 (있는 경우)
            if 'isPartial' in df.columns:
                df = df.drop(columns=['isPartial'])

            print(f"  [OK] Collected interest over time for '{keyword}'")
            return df

        except Exception as e:
            print(f"  [ERROR] Error collecting data for '{keyword}': {e}")
            return pd.DataFrame()

    def collect_related_queries(
        self,
        keyword: str,
        geo: str = ''
    ) -> Dict[str, Any]:
        """
        관련 검색어 수집

        Args:
            keyword: 검색 키워드
            geo: 지역 코드

        Returns:
            {'top': DataFrame, 'rising': DataFrame}
        """
        try:
            self.pytrends.build_payload(
                [keyword],
                cat=0,
                timeframe='today 12-m',
                geo=geo,
                gprop=''
            )

            related_queries = self.pytrends.related_queries()

            if keyword not in related_queries:
                print(f"  [WARN] No related queries for '{keyword}'")
                return {'top': pd.DataFrame(), 'rising': pd.DataFrame()}

            result = related_queries.get(keyword, {'top': None, 'rising': None})

            # None 체크 및 DataFrame 변환
            if result['top'] is None:
                result['top'] = pd.DataFrame()
            if result['rising'] is None:
                result['rising'] = pd.DataFrame()

            print(f"  [OK] Collected related queries for '{keyword}'")
            return result

        except Exception as e:
            print(f"  [ERROR] Error collecting related queries for '{keyword}': {e}")
            return {'top': pd.DataFrame(), 'rising': pd.DataFrame()}

    def collect_keyword_data(self, keyword_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        단일 키워드의 모든 트렌드 데이터 수집

        Args:
            keyword_info: 키워드 정보 딕셔너리

        Returns:
            수집된 데이터
        """
        keyword_id = keyword_info['keyword_id']
        keyword_text = keyword_info['text']
        geo = keyword_info.get('geo', '')

        print(f"\nCollecting data for: {keyword_text} (ID: {keyword_id})")

        # Interest over time
        interest_df = self.collect_interest_over_time(keyword_text, geo=geo)

        # Rate limit 방지를 위한 대기
        time.sleep(2)

        # Related queries
        related = self.collect_related_queries(keyword_text, geo=geo)

        # Rate limit 방지를 위한 대기
        time.sleep(2)

        return {
            'keyword_id': keyword_id,
            'keyword_text': keyword_text,
            'geo': geo,
            'category': keyword_info.get('category'),
            'priority': keyword_info.get('priority'),
            'intent': keyword_info.get('intent'),
            'collected_at': datetime.now().isoformat(),
            'interest_over_time': interest_df.to_dict('records') if not interest_df.empty else [],
            'related_queries_top': related['top'].to_dict('records') if not related['top'].empty else [],
            'related_queries_rising': related['rising'].to_dict('records') if not related['rising'].empty else []
        }

    def collect_all(self, priority_filter: int = None) -> List[Dict[str, Any]]:
        """
        모든 키워드 데이터 수집

        Args:
            priority_filter: 우선순위 필터 (예: 5이면 priority >= 5인 키워드만)

        Returns:
            수집된 데이터 리스트
        """
        keywords_to_collect = self.keywords

        if priority_filter:
            keywords_to_collect = [
                kw for kw in self.keywords
                if kw.get('priority', 0) >= priority_filter
            ]
            print(f"\nFiltered to {len(keywords_to_collect)} keywords with priority >= {priority_filter}")

        results = []
        total = len(keywords_to_collect)

        print(f"\n{'='*60}")
        print(f"Starting collection for {total} keywords")
        print(f"{'='*60}")

        for idx, keyword_info in enumerate(keywords_to_collect, 1):
            print(f"\n[{idx}/{total}] Processing...")

            try:
                data = self.collect_keyword_data(keyword_info)
                results.append(data)

                # 진행률 표시
                print(f"Progress: {idx}/{total} ({idx/total*100:.1f}%)")

            except Exception as e:
                print(f"[ERROR] Failed to collect data for {keyword_info['text']}: {e}")
                continue

        return results

    def save_results(self, results: List[Dict[str, Any]], filename: str = None):
        """
        수집 결과 저장

        Args:
            results: 수집된 데이터
            filename: 출력 파일명 (기본값: trends_YYYYMMDD_HHMMSS.json)
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"trends_{timestamp}.json"

        output_path = self.output_dir / filename

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'collected_at': datetime.now().isoformat(),
                'total_keywords': len(results),
                'results': results
            }, f, indent=2, ensure_ascii=False)

        print(f"\n{'='*60}")
        print(f"[OK] Results saved to: {output_path}")
        print(f"  Total keywords collected: {len(results)}")
        print(f"{'='*60}")

        return output_path

    def generate_summary(self, results: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        수집 결과 요약 생성

        Args:
            results: 수집된 데이터

        Returns:
            요약 데이터프레임
        """
        summary_data = []

        for item in results:
            # 최근 평균 관심도 계산 (최근 3개월)
            recent_interest = 0
            if item['interest_over_time']:
                recent_data = item['interest_over_time'][-12:]  # 최근 12주
                if recent_data:
                    values = [d.get(item['keyword_text'], 0) for d in recent_data]
                    recent_interest = sum(values) / len(values) if values else 0

            # 관련 검색어 개수
            top_queries_count = len(item['related_queries_top'])
            rising_queries_count = len(item['related_queries_rising'])

            summary_data.append({
                'keyword_id': item['keyword_id'],
                'keyword': item['keyword_text'],
                'category': item['category'],
                'priority': item['priority'],
                'intent': item['intent'],
                'geo': item['geo'],
                'avg_recent_interest': round(recent_interest, 2),
                'top_queries_count': top_queries_count,
                'rising_queries_count': rising_queries_count,
                'has_rising_trend': rising_queries_count > 0
            })

        return pd.DataFrame(summary_data)


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='Google Trends 데이터 수집')
    parser.add_argument(
        '--config',
        default='../../config/keywords.seed.small_retail_osa.v1.json',
        help='키워드 설정 파일 경로'
    )
    parser.add_argument(
        '--output',
        default='../../data/raw/trends',
        help='출력 디렉토리'
    )
    parser.add_argument(
        '--priority',
        type=int,
        default=None,
        help='최소 우선순위 (예: 5이면 priority >= 5만 수집)'
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help='요약 CSV 파일 생성'
    )

    args = parser.parse_args()

    # 수집기 초기화
    collector = TrendsCollector(
        config_path=args.config,
        output_dir=args.output
    )

    # 데이터 수집
    results = collector.collect_all(priority_filter=args.priority)

    # 결과 저장
    output_path = collector.save_results(results)

    # 요약 생성
    if args.summary or True:  # 항상 요약 생성
        summary_df = collector.generate_summary(results)
        summary_path = output_path.parent / f"{output_path.stem}_summary.csv"
        summary_df.to_csv(summary_path, index=False, encoding='utf-8-sig')
        print(f"[OK] Summary saved to: {summary_path}")

        # 콘솔에 요약 출력
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(summary_df.to_string(index=False))
        if not summary_df.empty and 'avg_recent_interest' in summary_df.columns:
            print(f"\n상위 5개 키워드 (평균 관심도 기준):")
            top5 = summary_df.nlargest(min(5, len(summary_df)), 'avg_recent_interest')
            print(top5[['keyword', 'category', 'avg_recent_interest', 'rising_queries_count']].to_string(index=False))


if __name__ == '__main__':
    main()
