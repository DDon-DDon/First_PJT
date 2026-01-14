'use client';

import Link from 'next/link';
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  LucideIcon,
  LayoutList,
  ArrowLeftRight
} from 'lucide-react';

export interface SidebarNavItem {
  label: string;
  href: string;
  icon: LucideIcon;
}

// --- 더미 데이터 ---

export const sidebarNavItems: SidebarNavItem[] = [
  // {
  //   label: 'Dashboard',
  //   href: '/',
  //   icon: LayoutDashboard,
  // },  
  {
    label: 'Stock View',
    href: '/',
    icon: LayoutList,
  },  
  {
    label: 'transactions',
    href: '/transactions',
    icon: ArrowLeftRight,  
  },
  {
    label: 'Inventory',
    href: '/inventory',
    icon: Package,
  },
  {
    label: 'Orders',
    href: '/orders',
    icon: ShoppingCart,
  },
];

export interface SidebarProps {
  items: SidebarNavItem[];
}

export default function Sidebar() {
  return (
    <aside className="w-64 flex flex-col h-full border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0">
      {/* Logo */}
      <div className="p-6 pb-2">
        <div className="flex items-center gap-3">
          <div className="bg-primary rounded-lg h-10 w-10 flex items-center justify-center text-black">
            <Package size={24} />
          </div>
          <div className="flex flex-col">
            <h1 className="text-slate-900 dark:text-white text-lg font-bold">
              StockPilot
            </h1>
            <p className="text-slate-500 dark:text-slate-400 text-xs">
              Admin Dashboard
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 flex flex-col gap-2">
        {sidebarNavItems.map((item) => {
          const Icon = item.icon;

          return (
            <Link
              key={item.label}
              href={item.href}
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
