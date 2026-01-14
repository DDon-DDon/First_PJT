'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  Search, 
  Plus, 
  Download, 
  Upload,
  ChevronLeft, 
  ChevronRight,
  MoreVertical,
  Calendar,
  Circle,
  X,
  Check
} from 'lucide-react';

// 1. 더미 데이터 생성 (20개)
const PRODUCT_IMAGE = 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80';
const ALL_DATA = Array.from({ length: 20 }).map((_, i) => ({
  id: `${2024001 + i}`,
  date: `Oct ${24 - (i % 5)}, 2023`,
  productName: i % 3 === 0 ? 'Smart Watch Series 7' : 'Wireless Mouse M30',
  sku: i % 3 === 0 ? 'SW-701-GRY' : 'WM-302-BLK',
  type: i % 2 === 0 ? 'IN' : 'OUT',
  quantity: 12 + i,
  status: i % 4 === 0 ? 'Pending' : 'Completed',
  person: i % 2 === 0 ? 'Alex Morgan' : 'Sarah Connor'
}));

export default function TransactionListPage() {
  const router = useRouter();
  const [currentPage, setCurrentPage] = useState(1);
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const filterRef = useRef<HTMLDivElement>(null);
  const itemsPerPage = 10;
  
  // 필터 태그 상태
  const [filters, setFilters] = useState([
    { id: 'f1', label: 'Stock In' },
    { id: 'f2', label: 'Completed' }
  ]);

  // 드롭다운 외부 클릭 시 닫기
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (filterRef.current && !filterRef.current.contains(event.target as Node)) {
        setIsFilterOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // 페이징 계산
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = ALL_DATA.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(ALL_DATA.length / itemsPerPage);

  // 필터 추가 핸들러
  const addFilter = (label: string) => {
    if (!filters.find(f => f.label === label)) {
      setFilters([...filters, { id: Date.now().toString(), label }]);
    }
    setIsFilterOpen(false);
  };

  const removeFilter = (id: string) => {
    setFilters(filters.filter(f => f.id !== id));
  };

  const handleRowClick = (id: string) => {
    router.push(`/transactions?view=${id}`);
  };

  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header Section: Export / Import (New Record 삭제됨) */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            {/* 밑줄 제거됨 */}
            <h1 className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">Transactions</h1>
            <p className="text-slate-500 dark:text-slate-400 mt-2 font-medium">Real-time inventory movement tracking</p>
          </div>
          <div className="flex gap-3">
            <button className="flex-1 md:flex-none flex items-center justify-center gap-2 px-6 h-[48px] border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold rounded-xl hover:bg-slate-50 transition-all text-sm shadow-sm">
              <Download size={18} /> Export
            </button>
            <button className="flex-1 md:flex-none flex items-center justify-center gap-2 px-6 h-[48px] border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold rounded-xl hover:bg-slate-50 transition-all text-sm shadow-sm">
              <Upload size={18} /> Import
            </button>
          </div>
        </div>

        {/* Search & Filter Bar (Add Filter 드롭다운 구현) */}
        <div className="bg-white dark:bg-slate-900 p-5 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 space-y-4">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
              <input 
                type="text"
                placeholder="Search products, SKUs, or members..."
                className="w-full h-[56px] pl-12 pr-4 bg-slate-50 dark:bg-slate-800/50 border-none rounded-xl focus:ring-2 focus:ring-primary dark:text-white transition-all text-sm"
              />
            </div>
            
            {/* Add Filter 드롭다운 */}
            <div className="relative w-full md:w-auto" ref={filterRef}>
              <button 
                onClick={() => setIsFilterOpen(!isFilterOpen)}
                className="w-full md:w-auto flex items-center justify-center gap-2 px-6 h-[56px] bg-slate-100 dark:bg-slate-800 rounded-xl text-slate-700 dark:text-slate-200 font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-sm border border-transparent"
              >
                <Plus size={18} /> Add Filter
              </button>

              {isFilterOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl z-50 overflow-hidden py-2 animate-in fade-in zoom-in duration-200">
                  <div className="px-4 py-2 text-[11px] font-black text-slate-400 uppercase tracking-widest">Select Filter</div>
                  {['Stock In', 'Stock Out', 'Completed', 'Pending', 'Electronics', 'Warehouse A'].map((label) => (
                    <button
                      key={label}
                      onClick={() => addFilter(label)}
                      className="w-full flex items-center justify-between px-4 py-2.5 text-sm text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
                    >
                      {label}
                      {filters.find(f => f.label === label) && <Check size={14} className="text-primary" />}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Filter Tags */}
          <div className="flex flex-wrap gap-2 pt-1">
            {filters.map((filter) => (
              <div 
                key={filter.id}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-primary/10 border border-primary/20 rounded-lg text-xs font-bold text-primary dark:text-blue-400 transition-all hover:bg-primary/20"
              >
                {filter.label}
                <button onClick={() => removeFilter(filter.id)} className="hover:bg-primary/20 rounded-full p-0.5">
                  <X size={14} />
                </button>
              </div>
            ))}
            {filters.length > 0 && (
              <button onClick={() => setFilters([])} className="text-xs font-bold text-slate-400 hover:text-red-500 px-2 transition-colors">
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Transaction Table */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
                  <th className="px-6 py-4 text-[11px] font-black text-slate-400 uppercase tracking-widest">Product Code</th>
                  <th className="px-6 py-4 text-[11px] font-black text-slate-400 uppercase tracking-widest">Description</th>
                  <th className="px-6 py-4 text-[11px] font-black text-slate-400 uppercase tracking-widest">Type</th>
                  <th className="px-6 py-4 text-[11px] font-black text-slate-400 uppercase tracking-widest text-right">Qty</th>
                  <th className="px-6 py-4 text-[11px] font-black text-slate-400 uppercase tracking-widest text-center">Status</th>
                  <th className="px-6 py-4 text-[11px] font-black text-slate-400 uppercase tracking-widest">User</th>
                  <th className="px-6 py-4"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800 text-sm">
                {currentItems.map((item) => (
                  <tr 
                    key={item.id} 
                    onClick={() => handleRowClick(item.id)}
                    className="hover:bg-blue-50/40 dark:hover:bg-blue-900/5 cursor-pointer transition-colors group"
                  >
                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="flex items-center gap-4">
                        <div className="h-12 w-12 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-700 shadow-sm">
                          <img src={PRODUCT_IMAGE} alt="product" className="h-full w-full object-cover group-hover:scale-110 transition-transform duration-300" />
                        </div>
                        <div className="text-sm font-black text-slate-900 dark:text-white font-mono">{item.sku}</div>
                      </div>
                    </td>
                    
                    <td className="px-6 py-5">
                      <div className="font-bold text-slate-900 dark:text-white group-hover:text-primary transition-colors italic">
                        {item.productName}
                      </div>
                      <div className="text-[11px] text-slate-400 dark:text-slate-500 mt-1 flex items-center gap-1 font-medium">
                        <Calendar size={12} className="opacity-70" /> {item.date}
                      </div>
                    </td>

                    <td className="px-6 py-5 whitespace-nowrap">
                      {item.type === 'IN' ? (
                        <span className="px-2.5 py-1 rounded-md text-[10px] font-black bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400">STOCK IN</span>
                      ) : (
                        <span className="px-2.5 py-1 rounded-md text-[10px] font-black bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-400">STOCK OUT</span>
                      )}
                    </td>

                    <td className="px-6 py-5 text-right whitespace-nowrap font-black text-base">
                      <span className={item.type === 'IN' ? 'text-emerald-600' : 'text-orange-600'}>
                        {item.type === 'IN' ? '+' : '-'}{item.quantity}
                      </span>
                    </td>

                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="flex justify-center">
                        <div className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-bold ${
                          item.status === 'Completed' ? 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                        }`}>
                          <Circle size={6} fill="currentColor" />
                          {item.status}
                        </div>
                      </div>
                    </td>

                    <td className="px-6 py-5 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-[11px] font-black text-slate-500 border-2 border-white dark:border-slate-900">
                          {item.person.charAt(0)}
                        </div>
                        <span className="text-xs font-bold text-slate-600 dark:text-slate-400">{item.person}</span>
                      </div>
                    </td>

                    <td className="px-6 py-5 text-right">
                      <button className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg text-slate-300 transition-colors">
                        <MoreVertical size={18} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="px-6 py-5 bg-slate-50/50 dark:bg-slate-800/30 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <span className="text-xs text-slate-500 dark:text-slate-400 font-bold uppercase tracking-tighter">
              Showing <span className="text-slate-900 dark:text-white px-1">{indexOfFirstItem + 1}-{Math.min(indexOfLastItem, ALL_DATA.length)}</span> of {ALL_DATA.length} records
            </span>
            <div className="flex gap-2">
              <button 
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="h-10 w-10 flex items-center justify-center rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronLeft size={18} />
              </button>
              
              <div className="flex items-center px-4 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl text-xs font-black dark:text-white">
                PAGE {currentPage} / {totalPages}
              </div>

              <button 
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="h-10 w-10 flex items-center justify-center rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}