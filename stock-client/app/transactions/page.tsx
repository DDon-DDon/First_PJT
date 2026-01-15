// app/transactions/page.tsx
// import Sidebar, { SidebarNavItem } from '../components/Sidebar';
import HistoryTable from '../components/HistoryTable';
import TransactionDetail from './_components/TransactionDetail';
import TransactionView from "./_components/TransactionView"

import { PackageSearch } from 'lucide-react'; // 아이콘 추가

// Props 타입을 Promise로 감싸줍니다.
export default async function TransactionPage({
  searchParams,
}: {
  searchParams: Promise<{ view?: string }>;
}) {
  // searchParams를 await로 기다려서 가져옵니다. (Next.js 15 필수사항)
  const { view: viewId } = await searchParams;

  return (
    <main className="flex-1 overflow-y-auto">
      {/* max-w를 조정하고 px를 메인과 통일 (px-6 ~ px-8) */}
      <div className="max-w-[1600px] mx-auto px-8 py-8">
        <nav className="flex items-center gap-2 text-sm text-slate-500 mb-6">
          <span>Stock</span>
          <span className="mx-2 opacity-50">/</span>
          <span className="text-slate-900 dark:text-slate-200 font-medium">Transactions</span>
        </nav>
        {/* Form Section */}
        {viewId ? (
          <>
            <div className="animate-in fade-in slide-in-from-top-4 duration-500">
              <TransactionDetail productId={viewId} />
            </div>
            <HistoryTable />
          </>
        ) : (
          <TransactionView />
        )}
      </div>
    </main>
  );
}