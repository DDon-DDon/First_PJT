// components/StockFilters.tsx
import { Search, Grid, List } from 'lucide-react';

export function StockFilters() {
  return (
    <section className="px-8 pb-6">
      <div className="flex flex-wrap items-center gap-3 bg-white dark:bg-slate-900 p-3 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
        {/* 검색창의 넓이를 고정하거나 적절히 제한 */}
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
          <input
            className="w-full pl-11 pr-4 py-2 bg-slate-50 dark:bg-slate-800/50 border-none rounded-xl text-sm outline-none focus:ring-2 focus:ring-blue-500/50"
            placeholder="Search products..."
            type="text"
          />
        </div>
        
        <div className="flex items-center gap-2 ml-auto">
          {/* Select Box들을 조금 더 작고 깔끔하게 */}
          {['All Categories', 'Status', 'Price'].map((label) => (
            <select key={label} className="bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-xl text-xs font-medium px-3 py-2 outline-none">
              <option>{label}</option>
            </select>
          ))}
          <div className="h-6 w-px bg-slate-200 dark:bg-slate-700 mx-1" />
          <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-lg">
             <button className="p-1.5 text-blue-600 bg-white dark:bg-slate-700 rounded shadow-sm"><Grid size={16} /></button>
             <button className="p-1.5 text-slate-400 hover:text-slate-600"><List size={16} /></button>
          </div>
        </div>
      </div>
    </section>
  );
}