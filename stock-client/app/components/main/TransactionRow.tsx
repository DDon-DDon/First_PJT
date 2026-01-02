'use client';

import { MoreVertical } from 'lucide-react';

export interface TransactionItem {
  id: string;
  name: string;
  type: 'Stock In' | 'Stock Out';
  qty: number;
  status: 'Completed' | 'Pending' | 'Failed' | 'Processing';
}

export default function TransactionRow({ id, name, type, qty, status }: TransactionItem) {
    return (
        <tr className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
            <td className="px-6 py-4 font-medium">{id}</td>
            <td className="px-6 py-4">{name}</td>
            <td className="px-6 py-4">
                <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${type.includes('In') ? 'bg-green-100 text-green-700 dark:bg-green-900/30' : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30'}`}>
                    {type}
                </span>
            </td>
            <td className="px-6 py-4 font-semibold">{qty}</td>
            <td className={`px-6 py-4 font-medium ${status === 'Completed' ? 'text-green-600' : 'text-amber-600'}`}>{status}</td>
            <td className="px-6 py-4 text-right">
                <button className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
                    <MoreVertical size={18} />
                </button>
            </td>
        </tr>
    );
}
