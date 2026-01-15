'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation'; // 현재 경로 확인용
import { Package, LayoutList, ArrowLeftRight, ShoppingCart, LayoutDashboardIcon } from 'lucide-react';

export const sidebarNavItems = [
  { label: 'Dashboard', href: '/', icon: LayoutDashboardIcon },
  { label: 'Stock View', href: '/stocks', icon: LayoutList },
  { label: 'Transactions', href: '/transactions', icon: ArrowLeftRight },
  { label: 'Inventory', href: '/inventory', icon: Package },
  { label: 'Orders', href: '/orders', icon: ShoppingCart },
];

export default function Sidebar() {
  const pathname = usePathname(); // 현재 URL 경로를 가져옴

  return (
    <aside className="w-64 flex flex-col h-full border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0">
      {/* Logo Section */}
      <Link href="/" className="block p-6 cursor-pointer hover:opacity-80 transition-opacity">
        <div className="flex items-center gap-3.5">
          {/* 로고 아이콘 컨테이너 */}
          <div className="bg-blue-600 rounded-[12px] h-11 w-11 flex items-center justify-center text-white shadow-sm shadow-blue-500/20">
            <Package size={24} strokeWidth={2.5} />
          </div>

          <div className="flex flex-col gap-0.5">
            <h1 className="text-slate-900 dark:text-white text-xl font-bold leading-tight tracking-tight">
              StockPilot
            </h1>
            <p className="text-slate-500 dark:text-slate-400 text-[13px] font-medium leading-none">
              Admin Dashboard
            </p>
          </div>
        </div>
      </Link>
      <nav className="flex-1 px-4 py-4 flex flex-col gap-2">
        {sidebarNavItems.map((item) => {
          const Icon = item.icon;
          // 현재 경로와 메뉴의 href가 같은지 확인
          const isActive =
            pathname === item.href ||
            pathname.startsWith(item.href + '/');

          return (
            <Link
              key={item.label}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition ${isActive
                ? 'bg-slate-100 dark:bg-slate-800 text-blue-600 dark:text-blue-400 font-bold' // 활성화 스타일
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                }`}
            >
              <Icon size={20} className={isActive ? 'text-blue-600' : ''} />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
