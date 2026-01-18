'use client';

import Link from 'next/link';
import { Sparkles, Hourglass } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-white px-6 text-center">
      {/* 아이콘 */}
      <div className="mb-6 flex items-center gap-2 text-green-400">
        <Hourglass size={32}/>
      </div>

      {/* 메인 메시지 */}
      <h1 className="mb-3 text-2xl font-semibold text-gray-900">
        서비스 준비중입니다.
      </h1>

      {/* 서브 메시지 */}
      <p className="mb-8 max-w-md text-sm leading-relaxed text-gray-500">
        보다 나은 서비스 제공을 위하여 페이지 준비중에 있습니다.
        <br />
        빠른 시일 내에 준비하여 찾아뵙겠습니다.
      </p>

      {/* 액션 */}
      <Link
        href="/"
        className="rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800"
      >
        홈으로 돌아가기
      </Link>
    </div>
  );
}
