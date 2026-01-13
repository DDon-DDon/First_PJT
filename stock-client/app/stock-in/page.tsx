// app/stock-in/page.tsx
import Sidebar, { SidebarNavItem } from '../components/Sidebar';
import InboundForm from './_components/InboundForm';
import HistoryTable from './_components/HistoryTable';
import { PackageSearch } from 'lucide-react'; // 아이콘 추가

// Props 타입을 Promise로 감싸줍니다.
export default async function StockInboundPage({
    searchParams,
}: {
    searchParams: Promise<{ view?: string }>;
}) {
    // searchParams를 await로 기다려서 가져옵니다. (Next.js 15 필수사항)
    const { view: viewId } = await searchParams;

    return (
        <div className="flex h-screen w-full bg-slate-50 dark:bg-[#101922] text-slate-900 dark:text-white font-sans overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto">
                <div className="max-w-7xl mx-auto p-8">
                    <nav className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 mb-6">
                        <span>Product</span>
                        <span className="mx-2 opacity-50">/</span>
                        <span className="text-slate-900 dark:text-slate-200 font-medium">Inbound</span>
                    </nav>

                    <header className="mb-8">
                        <h2 className="text-3xl font-bold text-slate-900 dark:text-white">Stock Inbound</h2>
                    </header>

                    {/* Form Section */}
                    {viewId ? (
                        <>
                            <div className="animate-in fade-in slide-in-from-top-4 duration-500">
                                <InboundForm productId={viewId} />
                            </div>

                            <HistoryTable />
                        </>
                    ) : (
                        <div className="mb-12 flex flex-col items-center justify-center p-16 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-3xl bg-white/30 dark:bg-slate-900/30 backdrop-blur-sm animate-in fade-in zoom-in-95 duration-500">
                            <div className="w-20 h-20 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center mb-6 text-blue-600 dark:text-blue-400">
                                <PackageSearch size={40} />
                            </div>
                            <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">입고 대상이 선택되지 않았습니다</h3>
                            <p className="text-slate-500 dark:text-slate-400 text-center max-w-md mb-8 leading-relaxed">
                                새로운 재고를 등록하거나 수량을 보정하려면 아래 히스토리 목록에서 제품을 선택해 주세요.
                            </p>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}