// pages/MainPage.tsx
import Sidebar, { SidebarNavItem } from './components/dashboard/Sidebar';
import { StockHeader } from './components/stock/StockHeader';
import { StockFilters } from './components/stock/StockFilters';
import { StockGrid } from './components/stock/StockGrid';

export default function MainPage() {
  return (
    <div className="flex h-screen w-full bg-slate-50 dark:bg-[#101922] text-slate-900 dark:text-white font-sans overflow-hidden">
      {/* Side Bar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* 모듈화된 컴포넌트들 */}
        <StockHeader />
        <StockFilters />
        <StockGrid />
      </main>

      {/* Floating AI Button (선택사항) */}
      <button className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold shadow-2xl hover:scale-110 transition-transform z-50">
        AI
      </button>
    </div>
  );
}