'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Package, 
  ArrowLeftRight, 
  ShoppingCart, 
  LayoutDashboardIcon, 
  Settings2,
  ChevronLeft,
  Truck 
} from 'lucide-react';

export const sidebarNavItems = [
  { label: 'Dashboard', href: '/', icon: LayoutDashboardIcon },
  { label: 'Stocks', href: '/stocks', icon: Package }, 
  { label: 'Transactions', href: '/transactions', icon: ArrowLeftRight },
  { label: 'Audit', href: '/audit', icon: Settings2 },
  { label: 'Orders', href: '/orders', icon: ShoppingCart },
  { label: 'Logistics', href: '/logistics', icon: Truck  },
];
// Delivery History
// Order Status

export default function Sidebar() {
  const pathname = usePathname();
  // 접힘 상태 관리 (기본값: false - 펼쳐짐)
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside className={`
      relative h-full border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0 transition-all duration-300 ease-in-out
      ${isCollapsed ? 'w-20' : 'w-64'}
    `}>
      {/* 접기/펴기 토글 버튼 */}
      <button 
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute -right-3 top-12 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-full p-1 shadow-md hover:text-blue-600 transition-all z-50"
      >
        {isCollapsed ? <ChevronLeft className="rotate-180" size={16} /> : <ChevronLeft size={16} />}
      </button>

      {/* Logo Section */}
      <Link href="/" className="block p-4 mt-2 cursor-pointer hover:opacity-80 transition-opacity">
        <div className={`flex items-center ${isCollapsed ? 'justify-center' : 'gap-3.5'}`}>
          <div className="bg-blue-600 rounded-[12px] h-11 w-11 flex items-center justify-center text-white shadow-sm shadow-blue-500/20 flex-shrink-0">
            <Package size={24} strokeWidth={2.5} />
          </div>

          {!isCollapsed && (
            <div className="flex flex-col gap-0.5 whitespace-nowrap overflow-hidden transition-all">
              <h1 className="text-slate-900 dark:text-white text-xl font-bold leading-tight tracking-tight">
                StockPilot
              </h1>
              <p className="text-slate-500 dark:text-slate-400 text-[13px] font-medium leading-none">
                Admin Dashboard
              </p>
            </div>
          )}
        </div>
      </Link>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 flex flex-col gap-2 mt-4">
        {sidebarNavItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');

          return (
            <Link
              key={item.label}
              href={item.href}
              className={`
                relative flex items-center transition-all duration-200 rounded-lg group
                ${isCollapsed ? 'justify-center px-0 py-2.5' : 'px-3 py-2.5 gap-3'}
                ${isActive
                  ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 font-bold'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                }
              `}
            >
              <Icon size={20} className={isActive ? 'text-blue-600' : ''} />
              
              {!isCollapsed && (
                <span className="font-medium whitespace-nowrap">{item.label}</span>
              )}

              {/* 접혔을 때 호버 툴팁 (선택 사항) */}
              {isCollapsed && (
                <div className="absolute left-full ml-2 px-2 py-1 bg-slate-800 text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-[100]">
                  {item.label}
                </div>
              )}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
