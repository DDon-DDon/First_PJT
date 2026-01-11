// components/StockFilters.tsx
import { Search, Grid, List } from 'lucide-react';

export function StockFilters() {
  return (
    <section className="px-8 pb-6 flex-shrink-0">
      <div className="flex flex-wrap items-center gap-4 bg-white dark:bg-slate-900 p-4 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800">
        <div className="relative flex-1 min-w-[300px]">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input
            className="w-full pl-12 pr-4 py-2.5 border-none rounded-lg focus:ring-2 focus:ring-blue-500/20 text-sm outline-none"
            placeholder="Search products, SKU or category..."
            type="text"
          />
        </div>
        <div className="flex items-center gap-3">
          <select className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500/20">
            <option>All Categories</option>
            <option>Wearables</option>
            <option>Computers</option>
            <option>Electronics</option>
          </select>
          <select className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500/20">
            <option>Status</option>
            <option>In Stock</option>
            <option>Low Stock</option>
            <option>Out of Stock</option>
          </select>
          <select className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm px-4 py-2 outline-none focus:ring-2 focus:ring-blue-500/20">
            <option>Price</option>            
            <option>$0 - $100</option>
            <option>$100 - $500</option>
            <option>$500+</option>
          </select>          
          <div className="h-8 w-px bg-slate-200 dark:bg-slate-700 mx-2" />
          <button className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
            <Grid size={20} />
          </button>
          <button className="p-2 text-slate-400 hover:text-blue-600 transition-colors">
            <List size={20} />
          </button>
        </div>
      </div>
    </section>
  );
}