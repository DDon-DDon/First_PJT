#!/usr/bin/env python3
"""
Reddit 데이터 수집 스크립트

PRAW (Python Reddit API Wrapper)를 사용하여 Reddit에서 소규모 리테일 관련
pain point 데이터를 수집합니다.

타겟 서브레딧:
- r/retailmanagement
- r/smallbusiness
- r/inventory
- r/retail
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import praw


class RedditCollector:
    """Reddit pain point 데이터 수집기"""

    def __init__(self, output_dir: str):
        """
        Args:
            output_dir: 출력 디렉토리 경로
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Reddit 인스턴스 초기화 (read-only mode)
        # User-Agent는 Reddit API 규정에 따라 설정
        self.reddit = praw.Reddit(
            client_id='anonymous',  # Read-only mode
            client_secret=None,
            user_agent='retail-osa-research:v1.0 (by /u/researcher)'
        )

        print("[OK] Reddit collector initialized (read-only mode)")

    def search_subreddit(
        self,
        subreddit_name: str,
        query: str,
        time_filter: str = 'year',
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        특정 서브레딧에서 키워드 검색

        Args:
            subreddit_name: 서브레딧 이름 (예: 'retailmanagement')
            query: 검색 쿼리
            time_filter: 시간 필터 ('hour', 'day', 'week', 'month', 'year', 'all')
            limit: 최대 결과 수

        Returns:
            검색된 게시물 리스트
        """
        print(f"\n[INFO] Searching r/{subreddit_name} for '{query}'...")

        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []

            for submission in subreddit.search(query, time_filter=time_filter, limit=limit):
                post_data = self._extract_post_data(submission)
                posts.append(post_data)

                # Rate limiting
                time.sleep(0.5)

            print(f"[OK] Found {len(posts)} posts in r/{subreddit_name}")
            return posts

        except Exception as e:
            print(f"[ERROR] Failed to search r/{subreddit_name}: {e}")
            return []

    def get_hot_posts(
        self,
        subreddit_name: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        서브레딧의 인기 게시물 수집

        Args:
            subreddit_name: 서브레딧 이름
            limit: 최대 결과 수

        Returns:
            인기 게시물 리스트
        """
        print(f"\n[INFO] Fetching hot posts from r/{subreddit_name}...")

        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []

            for submission in subreddit.hot(limit=limit):
                post_data = self._extract_post_data(submission)
                posts.append(post_data)

                # Rate limiting
                time.sleep(0.5)

            print(f"[OK] Collected {len(posts)} hot posts from r/{subreddit_name}")
            return posts

        except Exception as e:
            print(f"[ERROR] Failed to fetch hot posts from r/{subreddit_name}: {e}")
            return []

    def _extract_post_data(self, submission) -> Dict[str, Any]:
        """
        Reddit submission에서 필요한 데이터 추출

        Args:
            submission: PRAW submission 객체

        Returns:
            추출된 게시물 데이터
        """
        try:
            # 댓글 수집 (상위 10개)
            submission.comments.replace_more(limit=0)
            top_comments = []

            for comment in submission.comments[:10]:
                if hasattr(comment, 'body'):
                    top_comments.append({
                        'author': str(comment.author) if comment.author else '[deleted]',
                        'body': comment.body,
                        'score': comment.score,
                        'created_utc': datetime.fromtimestamp(comment.created_utc).isoformat()
                    })

            return {
                'post_id': submission.id,
                'title': submission.title,
                'selftext': submission.selftext,
                'author': str(submission.author) if submission.author else '[deleted]',
                'subreddit': str(submission.subreddit),
                'score': submission.score,
                'upvote_ratio': submission.upvote_ratio,
                'num_comments': submission.num_comments,
                'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
                'url': f"https://reddit.com{submission.permalink}",
                'top_comments': top_comments,
                'collected_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"[WARN] Error extracting post data: {e}")
            return {
                'post_id': submission.id if hasattr(submission, 'id') else 'unknown',
                'error': str(e),
                'collected_at': datetime.now().isoformat()
            }

    def collect_retail_pain_points(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        소규모 리테일 pain point 관련 데이터 수집

        Returns:
            서브레딧별 수집 결과
        """
        print("="*60)
        print("Starting Reddit pain point collection")
        print("="*60)

        # 검색 설정
        subreddits = [
            'smallbusiness',
            'retailmanagement',
            'retail',
            'inventory'
        ]

        search_queries = [
            'inventory problem',
            'out of stock',
            'shelf empty',
            'stock count',
            'inventory management pain',
            'manual counting',
            'inventory accuracy'
        ]

        results = {}

        # 각 서브레딧에서 검색
        for subreddit_name in subreddits:
            subreddit_posts = []

            # 각 쿼리로 검색
            for query in search_queries:
                posts = self.search_subreddit(
                    subreddit_name=subreddit_name,
                    query=query,
                    time_filter='year',
                    limit=20
                )
                subreddit_posts.extend(posts)

                # Rate limiting
                time.sleep(1)

            # 중복 제거 (post_id 기준)
            unique_posts = {}
            for post in subreddit_posts:
                if 'post_id' in post and 'error' not in post:
                    unique_posts[post['post_id']] = post

            results[subreddit_name] = list(unique_posts.values())

            print(f"[OK] r/{subreddit_name}: {len(unique_posts)} unique posts")

        return results

    def save_results(
        self,
        results: Dict[str, List[Dict[str, Any]]],
        filename: str = None
    ) -> Path:
        """
        수집 결과 저장 (JSONL 형식)

        Args:
            results: 서브레딧별 수집 결과
            filename: 출력 파일명 (기본값: posts_YYYYMMDD_HHMMSS.jsonl)

        Returns:
            저장된 파일 경로
        """
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"posts_{timestamp}.jsonl"

        output_path = self.output_dir / filename

        # JSONL 형식으로 저장 (한 줄당 하나의 게시물)
        total_posts = 0
        with open(output_path, 'w', encoding='utf-8') as f:
            for subreddit, posts in results.items():
                for post in posts:
                    post['source_subreddit'] = subreddit
                    f.write(json.dumps(post, ensure_ascii=False) + '\n')
                    total_posts += 1

        print("\n" + "="*60)
        print(f"[OK] Results saved to: {output_path}")
        print(f"  Total posts: {total_posts}")
        print(f"  Subreddits: {len(results)}")
        print("="*60)

        return output_path

    def generate_mock_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        테스트용 모의 데이터 생성

        ⚠️ Reddit API authentication이 필요하므로 mock 데이터로 파이프라인 테스트
        실제 수집을 위해서는 Reddit API credentials 필요

        Returns:
            모의 Reddit 게시물 데이터
        """
        print("\n[WARN] Generating mock data - NOT real Reddit posts")
        print("[INFO] This is for testing the pipeline only")
        print("[INFO] For real data, register a Reddit app at: https://www.reddit.com/prefs/apps")

        mock_posts = {
            'smallbusiness': [
                {
                    'post_id': 'mock_reddit_001',
                    'title': 'Struggling with inventory management in my small store',
                    'selftext': 'I run a small convenience store and manually checking shelves every day takes 2-3 hours. Is there any affordable automated solution?',
                    'author': 'small_store_owner',
                    'subreddit': 'smallbusiness',
                    'score': 45,
                    'upvote_ratio': 0.92,
                    'num_comments': 12,
                    'created_utc': '2024-11-25T10:30:00',
                    'url': 'https://reddit.com/r/smallbusiness/mock001',
                    'top_comments': [
                        {
                            'author': 'retail_expert',
                            'body': 'Have you looked into barcode scanners? Still manual but faster than visual counting.',
                            'score': 8,
                            'created_utc': '2024-11-25T11:00:00'
                        }
                    ],
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                },
                {
                    'post_id': 'mock_reddit_002',
                    'title': 'Lost sales due to out-of-stock items',
                    'selftext': 'Customers keep asking for items that are out of stock. By the time I notice and reorder, its too late. How do you track this?',
                    'author': 'frustrated_retailer',
                    'subreddit': 'smallbusiness',
                    'score': 67,
                    'upvote_ratio': 0.95,
                    'num_comments': 18,
                    'created_utc': '2024-10-15T14:20:00',
                    'url': 'https://reddit.com/r/smallbusiness/mock002',
                    'top_comments': [
                        {
                            'author': 'inventory_pro',
                            'body': 'You need real-time tracking. Enterprise solutions cost $10k+ though.',
                            'score': 15,
                            'created_utc': '2024-10-15T15:00:00'
                        }
                    ],
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                }
            ],
            'retail': [
                {
                    'post_id': 'mock_reddit_003',
                    'title': 'Manual stock counting is killing my team morale',
                    'selftext': 'We spend 4+ hours every week doing manual shelf counts. Team hates it, I hate it. Must be a better way in 2024.',
                    'author': 'retail_manager_2024',
                    'subreddit': 'retail',
                    'score': 89,
                    'upvote_ratio': 0.98,
                    'num_comments': 24,
                    'created_utc': '2024-09-10T09:15:00',
                    'url': 'https://reddit.com/r/retail/mock003',
                    'top_comments': [
                        {
                            'author': 'tech_savvy_retailer',
                            'body': 'Camera-based systems exist but theyre expensive and complex to set up.',
                            'score': 12,
                            'created_utc': '2024-09-10T10:00:00'
                        }
                    ],
                    'source': 'mock_data',
                    'collected_at': datetime.now().isoformat()
                }
            ]
        }

        total_posts = sum(len(posts) for posts in mock_posts.values())
        print(f"[OK] Generated {total_posts} mock Reddit posts across {len(mock_posts)} subreddits")

        return mock_posts

    def generate_summary(
        self,
        results: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """
        수집 결과 요약 생성

        Args:
            results: 서브레딧별 수집 결과

        Returns:
            요약 정보
        """
        total_posts = sum(len(posts) for posts in results.values())
        total_comments = sum(
            len(post.get('top_comments', []))
            for posts in results.values()
            for post in posts
        )

        # 키워드별 게시물 수 집계
        keyword_counts = {}
        search_terms = ['inventory', 'stock', 'shelf', 'out of stock', 'count']

        for posts in results.values():
            for post in posts:
                title_lower = post.get('title', '').lower()
                text_lower = post.get('selftext', '').lower()
                combined = title_lower + ' ' + text_lower

                for term in search_terms:
                    if term in combined:
                        keyword_counts[term] = keyword_counts.get(term, 0) + 1

        summary = {
            'collected_at': datetime.now().isoformat(),
            'total_subreddits': len(results),
            'total_posts': total_posts,
            'total_comments': total_comments,
            'posts_by_subreddit': {
                subreddit: len(posts)
                for subreddit, posts in results.items()
            },
            'keyword_mentions': keyword_counts,
            'avg_posts_per_subreddit': round(total_posts / len(results), 2) if results else 0
        }

        return summary


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(description='Reddit pain point 데이터 수집')
    parser.add_argument(
        '--output',
        default='../../data/raw/reddit',
        help='출력 디렉토리'
    )
    parser.add_argument(
        '--subreddit',
        help='특정 서브레딧만 수집 (예: smallbusiness)'
    )
    parser.add_argument(
        '--query',
        help='검색 쿼리 (subreddit과 함께 사용)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='서브레딧당 최대 게시물 수'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        help='모의 데이터 생성 (테스트용)'
    )

    args = parser.parse_args()

    # 수집기 초기화
    collector = RedditCollector(output_dir=args.output)

    # 데이터 수집
    if args.mock:
        # Mock 모드
        print("\n[INFO] Running in MOCK mode - generating test data")
        results = collector.generate_mock_data()
    elif args.subreddit and args.query:
        # 특정 서브레딧 + 쿼리 모드
        posts = collector.search_subreddit(
            subreddit_name=args.subreddit,
            query=args.query,
            limit=args.limit
        )
        results = {args.subreddit: posts}
    else:
        # 전체 pain point 수집 모드
        results = collector.collect_retail_pain_points()

    # 결과 저장
    output_path = collector.save_results(results)

    # 요약 생성 및 출력
    summary = collector.generate_summary(results)
    summary_path = output_path.parent / f"{output_path.stem}_summary.json"

    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Summary saved to: {summary_path}")
    print(f"\nSUMMARY:")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if args.mock:
        print(f"\n[REMINDER] This is MOCK data for testing only")
        print(f"[INFO] For real data, register a Reddit app at: https://www.reddit.com/prefs/apps")


if __name__ == '__main__':
    main()
