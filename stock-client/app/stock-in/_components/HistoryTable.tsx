// components/HistoryTable.tsx
import { MoreHorizontalIcon, ArrowDownIcon } from 'lucide-react';

const HISTORY_DATA = [
  {
    id: 1,
    type: 'Inbound',
    date: '2024-03-21 14:30',
    reference: 'PO-2024-001',
    quantity: '+50',
    status: 'Completed',
    user: 'Jar Sen'
  },
  {
    id: 2,
    type: 'Outbound',
    date: '2024-03-20 09:15',
    reference: 'SO-2024-089',
    quantity: '-12',
    status: 'Pending',
    user: 'Sarah Kim'
  },
  {
    id: 3,
    type: 'Inbound',
    date: '2024-03-19 16:45',
    reference: 'PO-2024-002',
    quantity: '+120',
    status: 'Cancelled',
    user: 'Jar Sen'
  },
];

export default function HistoryTable() {
  return (
    <section className="mt-12">
      <h3 className="text-xl font-bold text-slate-900 dark:text-white mb-6">Recent History</h3>
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-slate-50 dark:bg-slate-800/50 border-b border-slate-200 dark:border-slate-800">
              <tr>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                  <div className="flex items-center gap-1 cursor-pointer hover:text-primary transition-colors">
                    Date & Time <ArrowDownIcon size={14} />
                  </div>
                </th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Type</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Reference No.</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Quantity</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Status</th>
                <th className="px-6 py-4 text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Operator</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {HISTORY_DATA.map((row) => (
                <tr key={row.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group">
                  <td className="px-6 py-4 text-sm text-slate-600 dark:text-slate-400 font-medium">
                    {row.date}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`text-xs font-bold px-2.5 py-1 rounded-md ${
                      row.type === 'Inbound' 
                        ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' 
                        : 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
                    }`}>
                      {row.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm font-semibold text-slate-900 dark:text-slate-200">
                    {row.reference}
                  </td>
                  <td className={`px-6 py-4 text-sm font-bold ${
                    row.quantity.startsWith('+') ? 'text-blue-600' : 'text-rose-600'
                  }`}>
                    {row.quantity}
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={row.status} />
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-full bg-slate-200 dark:bg-slate-700 flex items-center justify-center text-[10px] font-bold">
                        {row.user.split(' ').map(n => n[0]).join('')}
                      </div>
                      <span className="text-sm text-slate-600 dark:text-slate-400">{row.user}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="p-1 rounded-md hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-400 transition-colors">
                      <MoreHorizontalIcon size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

// 뱃지 프로토타입 쇼케이스를 위한 서브 컴포넌트
function StatusBadge({ status }: { status: string }) {
  const styles = {
    Completed: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800",
    Pending: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 border border-amber-200 dark:border-amber-800",
    Cancelled: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 border border-slate-200 dark:border-slate-700",
  }[status] || "";

  return (
    <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${styles}`}>
      {status}
    </span>
  );
}