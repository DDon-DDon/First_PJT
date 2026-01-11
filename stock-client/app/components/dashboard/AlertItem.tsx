'use client';

import { AlertCircle, Clock } from 'lucide-react';

export type AlertType = 'error' | 'warning';

interface AlertItemProps {
  title: string;
  message: string;
  type: AlertType;
}

export default function AlertItem({ title, message, type }: AlertItemProps) {
  const isError = type === 'error';

  return (
    <div
      className={`flex gap-3 items-start p-3 rounded-lg border ${
        isError
          ? 'bg-red-50 dark:bg-red-900/10 border-red-100 dark:border-red-900/20'
          : 'bg-amber-50 dark:bg-amber-900/10 border-amber-100 dark:border-amber-900/20'
      }`}
    >
      {isError ? (
        <AlertCircle className="text-red-500 mt-0.5" size={18} />
      ) : (
        <Clock className="text-amber-500 mt-0.5" size={18} />
      )}

      <div>
        <p className="text-sm font-semibold text-slate-900 dark:text-white">
          {title}
        </p>
        <p
          className={`text-xs font-medium ${
            isError ? 'text-red-600' : 'text-amber-600'
          }`}
        >
          {message}
        </p>
      </div>
    </div>
  );
}
