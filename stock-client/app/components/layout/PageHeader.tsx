'use client';

import { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  actions?: ReactNode;
}

export default function PageHeader({ title, actions }: PageHeaderProps) {
  return (
    <header className="h-16 flex items-center justify-between px-8 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0">
      <div className="flex items-center gap-4">
        <h2 className="text-xl font-bold">{title}</h2>
      </div>

      {/* Action Slot */}
      <div className="flex items-center gap-4">
        {actions}
      </div>
    </header>
  );
}
