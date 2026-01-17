"use client"
import React, { useState } from 'react';
import {
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  AreaChart, Area, BarChart, Bar, ComposedChart
} from 'recharts';
import { ChevronDown } from 'lucide-react';

// 데이터 구조 정의
const trendData = [
  { name: '05/16', price: 4200, count: 2400, newItem: 120, transaction: 450 },
  { name: '05/17', price: 3800, count: 2100, newItem: 80, transaction: 380 },
  { name: '05/18', price: 5100, count: 2800, newItem: 150, transaction: 520 },
  { name: '05/19', price: 4800, count: 2600, newItem: 110, transaction: 410 },
  { name: '05/20', price: 6200, count: 3200, newItem: 190, transaction: 680 },
  { name: '05/21', price: 5800, count: 3100, newItem: 140, transaction: 590 },
  { name: '05/22', price: 6500, count: 3400, newItem: 170, transaction: 720 },
];

const chartConfigs = {
  price: { label: '전체 재고 자산 변동 (원화)', color: '#00C73C', type: 'area', dataKey: 'price' },
  count: { label: '전체 재고 자산 개수 추이', color: '#0075FF', type: 'area', dataKey: 'count' },
  newItem: { label: '일일 신규 등록 건 수', color: '#8884d8', type: 'bar', dataKey: 'newItem' },
  transaction: { label: '일일 신규 재고 트랜잭션 수', color: '#FFBB28', type: 'bar', dataKey: 'transaction' },
};

const InventoryTrendChart = () => {
  const [selectedKey, setSelectedKey] = useState<keyof typeof chartConfigs>('price');
  const currentConfig = chartConfigs[selectedKey];

  return (
    <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-gray-100 min-h-[450px]">
      {/* 헤더 및 선택 상자 */}
      <div className="flex justify-between items-center mb-8">
        <h3 className="text-lg font-bold text-gray-800">재고 관리 변동 추이</h3>
        
        <div className="relative inline-block">
          <select
            value={selectedKey}
            onChange={(e) => setSelectedKey(e.target.value as any)}
            className="appearance-none bg-gray-50 border border-gray-200 text-gray-700 text-xs font-bold py-2 pl-4 pr-10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer transition-all"
          >
            <option value="price">재고 자산 가치 (원화)</option>
            <option value="count">재고 자산 개수</option>
            <option value="newItem">신규 등록 건 수</option>
            <option value="transaction">재고 트랜잭션 수</option>
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-400">
            <ChevronDown size={14} />
          </div>
        </div>
      </div>

      {/* 그래프 영역 */}
      <div className="h-[320px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          {currentConfig.type === 'area' ? (
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={currentConfig.color} stopOpacity={0.15} />
                  <stop offset="95%" stopColor={currentConfig.color} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F0F0F0" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#999' }} dy={10} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#999' }} />
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
              />
              <Area 
                type="monotone" 
                dataKey={currentConfig.dataKey} 
                stroke={currentConfig.color} 
                fillOpacity={1} 
                fill="url(#colorGradient)" 
                strokeWidth={3}
                animationDuration={1000}
              />
            </AreaChart>
          ) : (
            <BarChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F0F0F0" />
              <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#999' }} dy={10} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 11, fill: '#999' }} />
              <Tooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                cursor={{ fill: '#F9FAFB' }}
              />
              <Bar 
                dataKey={currentConfig.dataKey} 
                fill={currentConfig.color} 
                radius={[6, 6, 0, 0]} 
                barSize={32}
                animationDuration={1000}
              />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default InventoryTrendChart;