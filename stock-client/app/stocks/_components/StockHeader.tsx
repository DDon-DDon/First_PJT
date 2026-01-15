// components/StockHeader.tsx
import Link from 'next/link';
import { Upload, Plus } from 'lucide-react';

// TODO : Stock > View 이런 구조이므로, props로 부모 컴포넌트로부터 값을 가져오도록 구조 변경 예정.

export function StockHeader() {
  return (
    <header className="px-8 pt-8 pb-6 flex-shrink-0">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <nav className="flex items-center text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
            <span>Stock</span>
            <span className="mx-2 opacity-50">/</span>
            <span className="text-blue-600 dark:text-blue-400">View</span>
          </nav>
          <h2 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Stock View</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Manage and track your inventory levels in real-time.</p>
        </div>
        <div className="flex items-center gap-2">
          {/* 머터리얼의 'Outlined Button' 스타일 */}
          <button className="flex items-center gap-2 px-4 py-2 text-sm bg-transparent text-slate-700 dark:text-slate-200 font-bold rounded-full border border-slate-300 dark:border-slate-600 hover:bg-slate-100 transition-all">
            <Upload size={16} /> Import
          </button>
          {/* 머터리얼의 'Filled Button' 스타일 */}
          <Link
            href="/stocks/new"
            className="flex items-center gap-2 px-5 py-2.5 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all"
          >
            <Plus size={18} /> Add Product
          </Link>
        </div>
      </div>
    </header>
  );
}