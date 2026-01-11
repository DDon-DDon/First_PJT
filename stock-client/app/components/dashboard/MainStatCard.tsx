'use client';

import { TrendingUp, TrendingDown, LucideIcon } from 'lucide-react';

export type StatColor = 'blue' | 'purple' | 'red' | 'amber';

export interface MainStatCardProps {
  title: string;
  value: number;
  trend: string;
  icon: LucideIcon;
  color: StatColor;
  negative?: boolean;
}

const colorMap: Record<StatColor, string> = {
  blue: 'bg-blue-50 text-blue-600',
  purple: 'bg-purple-50 text-purple-600',
  red: 'bg-red-50 text-red-600',
  amber: 'bg-amber-50 text-amber-600',
};

export default function MainStatCard({
  title,
  value,
  trend,
  icon: Icon,
  color,
  negative = false,
}: MainStatCardProps) {
  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between h-32">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-slate-500 text-sm font-medium">{title}</p>
          <h3 className="text-2xl font-bold mt-1">{value}</h3>
        </div>

        <div className={`p-2 rounded-lg ${colorMap[color]}`}>
          <Icon size={20} />
        </div>
      </div>

      <div className="flex items-center gap-1 mt-auto">
        {negative ? (
          <TrendingDown size={14} className="text-red-500" />
        ) : (
          <TrendingUp size={14} className="text-green-600" />
        )}
        <span
          className={`text-sm font-semibold ${
            negative ? 'text-red-500' : 'text-green-600'
          }`}
        >
          {trend}
        </span>
      </div>
    </div>
  );
}
