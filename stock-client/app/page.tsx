// app/page.tsx
/*
import DashboardPage from "./components/dashboard/DashboardPage"

export default function MainPage() {
  return (
    <>
      <DashboardPage/>
    </>
  );
}
*/

"use client";
import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend, AreaChart, Area
} from 'recharts';
import { AlertCircle, ArrowUpRight, ChevronRight, Package, DollarSign, Bell } from 'lucide-react';
import MonitoringSection from "./components/MonitoringSection"
import DashSummaryCard, { DashSummaryProps } from "./components/DashSummaryCard"
import DashTransactionTable from "./components/DashTransactionTable"
import InventoryTrendChart from './components/InventoryTrendChart';

//
// 데이터를 배열로 관리하여 유지보수성 향상
const summaryItems: DashSummaryProps[] = [
  {
    title: "전체 상품 가치",
    value: "₩ 1,250,400,000",
    trend: "2.4%",
    isUp: true,
    icon: <DollarSign size={20} />,
    routeUrl: "#"
  },
  {
    title: "전체 재고 개수",
    value: "45,230 EA",
    trend: "1.2%",
    isUp: false,
    icon: <Package size={20} />,
    routeUrl: "/stocks"
  },
  {
    title: "재고 변경 이력",
    value: "128 건",
    trend: "5.0%",
    isUp: true,
    icon: <AlertCircle size={20} />,
    routeUrl: "/transactions"
  },
  {
    title: "평균 회전율",
    value: "85%",
    trend: "0.5%",
    isUp: true,
    icon: <ArrowUpRight size={20} />,
    routeUrl: "#"
  }
];

const categoryData = [
  { name: '의류', value: 400 },
  { name: '가전', value: 300 },
  { name: '식품', value: 300 },
  { name: '뷰티', value: 200 },
];

const COLORS = ['#00C73C', '#0075FF', '#FFBB28', '#FF8042'];

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-[#f4f7f9] p-8 font-sans text-[#333] overflow-y-auto">
      {/* 상단 헤더 */}
      <header className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">재고 현황 대시보드</h1>
        </div>
        <div className="text-sm text-gray-400">최근 업데이트: 2024-05-22 14:30</div>
      </header>

      {/* 1 & 2. 요약 카드 섹션 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {summaryItems.map((item, index) => (
          <DashSummaryCard key={index} {...item} />
        ))}
      </div>

      {/* 3. 상태 모니터링 뷰 */}
      <div className="bg-white p-6 shadow-sm rounded-l mb-8">
        <h3 className="text-lg font-semibold mb-4">재고 상태 모니터링</h3>
        <MonitoringSection />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* 5. 재고 시스템 변동 추이 (시계열) */}
        <InventoryTrendChart />

        {/* 6. 상품 카테고리 도넛 그래프 */}
        <div className="bg-white p-6 rounded-l shadow-sm border border-gray-100">
          <h3 className="text-lg font-semibold mb-6">카테고리별 분포</h3>
          <div className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={categoryData} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-20">
        {/* 7. 재고 트랜잭션 테이블 */}
        {/* <div className="lg:col-span-2 bg-white rounded-l shadow-sm border border-gray-100 overflow-hidden">
          <div className="p-6 border-b border-gray-50 flex justify-between items-center">
            <h3 className="text-lg font-semibold">최근 재고 트랜잭션</h3>
            <button className="text-sm text-green-600 font-medium">전체보기</button>
          </div>
          <table className="w-full text-left text-sm">
            <thead className="bg-gray-50 text-gray-500 uppercase">
              <tr>
                <th className="px-6 py-3 font-medium">상품명</th>
                <th className="px-6 py-3 font-medium">변동 유형</th>
                <th className="px-6 py-3 font-medium">수량</th>
                <th className="px-6 py-3 font-medium">일시</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              <TransactionRow name="나이키 에어맥스" type="입고" amount="+50" date="2024-05-22 14:00" />
              <TransactionRow name="삼성 갤럭시 S24" type="출고" amount="-2" date="2024-05-22 13:45" />
              <TransactionRow name="애플 맥북 프로" type="주문완료" amount="-1" date="2024-05-22 12:30" />
            </tbody>
          </table>
        </div> */}
        <DashTransactionTable/>

        {/* 4. 최근 알람 히스토리 */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-lg font-bold flex items-center gap-2 text-gray-800">
              <Bell size={18} className="text-green-600" /> 알람 히스토리
            </h3>

            {/* 자세히보기 버튼: 호버 시 파란색 강조 */}
            <button className="text-xs text-gray-400 font-medium flex items-center gap-0.5 transition-colors duration-200 hover:text-[#0075FF] group/more">
              자세히보기
              <ChevronRight size={14} className="transition-transform duration-200 group-hover/more:translate-x-0.5" />
            </button>
          </div>

          <div className="space-y-5">
            <AlarmItem
              title="재고 부족 알림"
              desc="아이폰 15 케이스 재고가 3개 남았습니다."
              time="5분 전"
              type="warn"
            />
            <AlarmItem
              title="신규 입고 확인"
              desc="물류 센터에 의류 신상품 100건이 입고되었습니다."
              time="1시간 전"
              type="info"
            />
            <AlarmItem
              title="품절 발생"
              desc="블루투스 이어폰 화이트 모델이 품절되었습니다."
              time="3시간 전"
              type="error"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// --- 서브 컴포넌트들 ---


const TransactionRow = ({ name, type, amount, date }: any) => (
  <tr className="hover:bg-gray-50 transition-colors">
    <td className="px-6 py-4 font-medium">{name}</td>
    <td className="px-6 py-4">
      <span className={`px-2 py-1 rounded text-xs ${type === '입고' ? 'bg-blue-50 text-blue-600' : 'bg-gray-100 text-gray-600'}`}>{type}</span>
    </td>
    <td className="px-6 py-4 font-semibold">{amount}</td>
    <td className="px-6 py-4 text-gray-400">{date}</td>
  </tr>
);

const AlarmItem = ({ title, desc, time, type }: any) => (
  <div className="border-l-4 border-green-500 pl-4 py-1">
    <h4 className="text-sm font-semibold">{title}</h4>
    <p className="text-xs text-gray-500 mb-1">{desc}</p>
    <span className="text-[10px] text-gray-400">{time}</span>
  </div>
);

export default Dashboard;