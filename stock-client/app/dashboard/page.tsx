'use client';

import React from 'react';
import {
    LayoutDashboard, Package, ShoppingCart, BarChart3, Users,
    Settings, Bell, Plus, TrendingUp, TrendingDown,
    AlertCircle, Clock, MoreVertical, Wallet, AlertTriangle, Truck
} from 'lucide-react';
// Recharts 컴포넌트 임포트
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area,
    PieChart, Pie, Cell, Legend
} from 'recharts';

// --- 더미 데이터 ---
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

export default function DashboardPage() {
    return (
        <div className="flex h-screen w-full bg-slate-50 dark:bg-[#101922] text-slate-900 dark:text-white font-sans overflow-hidden">
            {/* Sidebar (생략 - 이전과 동일) */}
            <aside className="w-64 flex flex-col h-full border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0">
                <div className="p-6 pb-2">
                    <div className="flex items-center gap-3">
                        <div className="bg-primary rounded-lg h-10 w-10 flex items-center justify-center text-white">
                            <Package size={24} />
                        </div>
                        <div className="flex flex-col">
                            <h1 className="text-slate-900 dark:text-white text-lg font-bold">StockPilot</h1>
                            <p className="text-slate-500 dark:text-slate-400 text-xs">Admin Dashboard</p>
                        </div>
                    </div>
                </div>
                <nav className="flex-1 px-4 py-4 flex flex-col gap-2">
                    <a className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-primary/10 text-primary font-semibold" href="#"><LayoutDashboard size={20} /> Dashboard</a>
                    <a className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100" href="#"><Package size={20} /> Inventory</a>
                    <a className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-slate-100" href="#"><ShoppingCart size={20} /> Orders</a>
                </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 flex flex-col h-full overflow-hidden">
                {/* Header */}
                <header className="h-16 flex items-center justify-between px-8 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex-shrink-0">
                    <div className="flex items-center gap-4">
                        <h2 className="text-xl font-bold">Inventory Overview</h2>
                    </div>
                    <div className="flex items-center gap-4">
                        <button className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-semibold bg-blue-600">
                            <Plus size={18} /> Create Order
                        </button>
                    </div>
                </header>

                {/* Dashboard Scroll Area */}
                <div className="flex-1 overflow-y-auto p-8">
                    <div className="max-w-7xl mx-auto flex flex-col gap-6">

                        {/* 1. 상단 통계 카드 (이전과 동일) */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                            <StatCard title="Total Inventory Value" value="$124,500" trend="+12%" icon={Wallet} color="blue" />
                            <StatCard title="Total Items" value="1,240" trend="+5%" icon={Package} color="purple" />
                            <StatCard title="Low Stock Items" value="12" trend="-2%" icon={AlertTriangle} color="red" negative />
                            <StatCard title="Pending Orders" value="45" trend="+8%" icon={Truck} color="amber" />
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
                                        <TableRow id="#TR-8832" name="Nike Air Max 270" type="Stock In" qty="+150" status="Completed" />
                                        <TableRow id="#TR-8831" name="Sony WH-1000XM4" type="Stock Out" qty="-12" status="Processing" />
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

// Reusable Components (StatCard 등은 이전 답변의 코드와 동일하게 유지)
function StatCard({ title, value, trend, icon: Icon, color, negative = false }: any) {
    const colorMap: any = {
        blue: "bg-blue-50 text-blue-600",
        purple: "bg-purple-50 text-purple-600",
        red: "bg-red-50 text-red-600",
        amber: "bg-amber-50 text-amber-600",
    };
    return (
        <div className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col justify-between h-32">
            <div className="flex justify-between items-start">
                <div>
                    <p className="text-slate-500 text-sm font-medium">{title}</p>
                    <h3 className="text-2xl font-bold mt-1">{value}</h3>
                </div>
                <div className={`p-2 rounded-lg ${colorMap[color]}`}><Icon size={20} /></div>
            </div>
            <div className="flex items-center gap-1 mt-auto">
                {negative ? <TrendingDown size={14} className="text-red-500" /> : <TrendingUp size={14} className="text-green-600" />}
                <span className={`text-sm font-semibold ${negative ? 'text-red-500' : 'text-green-600'}`}>{trend}</span>
            </div>
        </div>
    );
}

function TableRow({ id, name, type, qty, status }: any) {
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

// Alert 컴포넌트
function AlertItem({ title, message, type }: { title: string; message: string; type: 'error' | 'warning' }) {
    const isError = type === 'error';

    return (
        <div className={`flex gap-3 items-start p-3 rounded-lg border ${isError
            ? 'bg-red-50 dark:bg-red-900/10 border-red-100 dark:border-red-900/20'
            : 'bg-amber-50 dark:bg-amber-900/10 border-amber-100 dark:border-amber-900/20'
            }`}>
            {isError ? (
                <AlertCircle className="text-red-500 mt-0.5" size={18} />
            ) : (
                <Clock className="text-amber-500 mt-0.5" size={18} />
            )}
            <div>
                <p className="text-sm font-semibold text-slate-900 dark:text-white">{title}</p>
                <p className={`text-xs font-medium ${isError ? 'text-red-600' : 'text-amber-600'}`}>
                    {message}
                </p>
            </div>
        </div>
    );
}