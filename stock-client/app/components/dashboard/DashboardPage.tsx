'use client';

import {
    Package, 
  Wallet, AlertTriangle, Truck
} from 'lucide-react';
// Recharts 컴포넌트 임포트
import {
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area,
  PieChart, Pie, Cell, Legend
} from 'recharts';

import AlertItem from './AlertItem'
import TransactionRow, { TransactionItem } from './TransactionRow';
import MainStatCard, { MainStatCardProps } from "./MainStatCard"


// dummy data!
const lineData = [
  { name: 'Week 1', value: 400000 },
  { name: 'Week 2', value: 800000 },
  { name: 'Week 3', value: 600000 },
  { name: 'Week 4', value: 1200000 },
];

const categoryData = [
  { name: 'Electronics', value: 40, color: '#137fec' },
  { name: 'Home', value: 20, color: '#22d3ee' },
  { name: 'Clothing', value: 15, color: '#a855f7' },
  { name: 'Others', value: 25, color: '#e2e8f0' },
];

// stat dummy
const statCardData: MainStatCardProps[] = [
  {
    title: 'Total Inventory Value',
    value: 12450,
    trend: '+12%',
    icon: Wallet,
    color: 'blue',
  },
  {
    title: 'Total Items',
    value: 1240,
    trend: '+5%',
    icon: Package,
    color: 'purple',
  },
  {
    title: 'Low Stock Items',
    value: 12,
    trend: '-2%',
    icon: AlertTriangle,
    color: 'red',
    negative: true,
  },
  {
    title: 'Pending Orders',
    value: 45,
    trend: '+8%',
    icon: Truck,
    color: 'amber',
  },
];

// table dummy
const tableData: TransactionItem[] = [
  {
    id: '#TR-8832',
    name: 'Nike Air Max 270',
    type: 'Stock In',
    qty: 150,
    status: 'Completed',
  },
  {
    id: '#TR-8831',
    name: 'Adidas Ultraboost 22',
    type: 'Stock Out',
    qty: 40,
    status: 'Completed',
  },
  {
    id: '#TR-8830',
    name: 'New Balance 990v5',
    type: 'Stock In',
    qty: 80,
    status: 'Pending',
  },
  {
    id: '#TR-8829',
    name: 'Puma RS-X',
    type: 'Stock Out',
    qty: 25,
    status: 'Failed',
  },
  {
    id: '#TR-8828',
    name: 'Nike Dunk Low',
    type: 'Stock In',
    qty: 200,
    status: 'Completed',
  },
  {
    id: '#TR-8827',
    name: 'Asics Gel-Kayano 30',
    type: 'Stock In',
    qty: 60,
    status: 'Pending',
  },
  {
    id: '#TR-8826',
    name: 'Reebok Club C 85',
    type: 'Stock Out',
    qty: 30,
    status: 'Completed',
  },
  {
    id: '#TR-8825',
    name: 'Converse Chuck 70',
    type: 'Stock Out',
    qty: 55,
    status: 'Pending',
  },
];


export default function DashboardPage() { 
    return (

                <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto flex flex-col gap-6">

            {/* 1. 상단 통계 카드 (이전과 동일) */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {statCardData.map((item) => (
                <MainStatCard key={item.title} {...item} />
              ))}
            </div>

            {/* 2. 차트 및 알림 섹션 세로 배치 구조 */}
            <div className="flex flex-col gap-6">

              {/* 상단: 메인 라인 차트 (한 행 전체 차지) */}
              <div className="bg-white dark:bg-slate-900 rounded-xㅡ border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-slate-900 dark:text-white text-lg font-bold">Inventory Valuation History</h3>
                    <p className="text-slate-500 dark:text-slate-400 text-sm">Last 30 Days trend</p>
                  </div>
                  <select className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-sm rounded-lg px-3 py-2 outline-none">
                    <option value="weekly">Weekly View</option>
                    <option value="monthly">Monthly View</option>
                    <option value="yearly">Yearly View</option>
                  </select>
                </div>
                <div className="w-full h-60">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={lineData}>
                      <defs>
                        <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#137fec" stopOpacity={0.1} />
                          <stop offset="95%" stopColor="#137fec" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                      <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#94a3b8' }} dy={10} />
                      <YAxis hide />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff' }} />
                      <Area type="monotone" dataKey="value" stroke="#137fec" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* 하단: 도넛 차트와 경고창 1:1 배치 */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                {/* Stock by Category (도넛 차트) */}
                <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm flex flex-col items-center">
                  <h3 className="text-slate-900 dark:text-white text-lg font-bold mb-4 self-start">Stock by Category</h3>
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={categoryData}
                          cx="50%"
                          cy="50%"
                          innerRadius={70}
                          outerRadius={90}
                          paddingAngle={8}
                          dataKey="value"
                        >
                          {categoryData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="grid grid-cols-2 gap-4 mt-4 w-full px-4">
                    {categoryData.map((item) => (
                      <div key={item.name} className="flex items-center justify-between text-sm border-b border-slate-100 dark:border-slate-800 pb-1">
                        <div className="flex items-center gap-2">
                          <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></span>
                          <span className="text-slate-600 dark:text-slate-400">{item.name}</span>
                        </div>
                        <span className="font-bold">{item.value}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Alerts Section (경고창) */}
                <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 flex flex-col">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-slate-900 dark:text-white text-lg font-bold">Alerts</h3>
                    <span className="text-xs bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 px-2 py-1 rounded-full font-bold">
                      3 Critical
                    </span>
                  </div>
                  <div className="flex flex-col gap-4 overflow-y-auto">
                    <AlertItem title="MacBook Pro M2" message="Stock Critical: Only 2 left" type="error" />
                    <AlertItem title="Shipment #4022" message="Delayed by 2 days" type="warning" />
                    <AlertItem title="Sony WH-1000XM4" message="Reorder point reached" type="warning" />
                    <AlertItem title="Logitech MX Master" message="Incoming stock confirmed" type="warning" />
                  </div>
                </div>
              </div>
            </div>

            {/* Table Section */}
            <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
              <div className="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-800">
                <h3 className="text-slate-900 dark:text-white text-lg font-bold">Recent Transactions</h3>
                <button className="text-blue-600 text-sm font-semibold hover:underline">View All</button>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 text-xs uppercase font-semibold">
                    <tr>
                      <th className="px-6 py-4">Transaction ID</th>
                      <th className="px-6 py-4">Item Name</th>
                      <th className="px-6 py-4">Type</th>
                      <th className="px-6 py-4">Quantity</th>
                      <th className="px-6 py-4">Status</th>
                      <th className="px-6 py-4 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 dark:divide-slate-800 text-sm text-slate-700 dark:text-slate-300">
                    {tableData.map((item) => (
                      <TransactionRow
                        key={item.id}
                        id={item.id}
                        name={item.name}
                        type={item.type}
                        qty={item.qty}
                        status={item.status}
                      />
                    ))}


                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

    )

}