// dashboard
"use client"
import Link from 'next/link';
import React, { ReactNode } from 'react';

// 1. Props 인터페이스 정의
export interface DashSummaryProps {
    title: string;      // 카드의 제목 (예: '전체 상품 가치')
    value: string;      // 표시될 금액이나 수량 (예: '₩ 1,250,400,000')
    trend: string;      // 변동 백분율 (예: '2.4%')
    isUp: boolean;      // 상승 여부 (true면 그린/상승화살표, false면 레드/하락화살표)
    icon: ReactNode;    // lucide-react 등의 아이콘 컴포넌트
    routeUrl: string;
}

const DashSummaryCard = ({ title, value, trend, isUp, icon, routeUrl }: DashSummaryProps) => {
    return (
        <Link href={routeUrl.length ? routeUrl : "#"} className="block">
            <div className="
      group bg-white p-6 rounded-l border border-gray-100 shadow-sm
      transition-all duration-200 ease-out cursor-pointer
      hover:-translate-y-0.5 hover:-translate-x-0.5 hover:shadow-lg hover:border-blue-400
    ">
                <div className="flex justify-between items-start mb-4">
                    {/* 아이콘 영역: 호버 시 블루 톤으로 변경 */}
                    <div className="
          p-2 bg-gray-50 rounded-lg text-gray-400 
          transition-colors duration-200 group-hover:bg-blue-50 group-hover:text-blue-500
        ">
                        {icon}
                    </div>

                    {/* 증감 정보 뱃지 */}
                    <span className={`
          text-[11px] font-bold px-2 py-0.5 rounded-full flex items-center gap-0.5
          ${isUp ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'}
        `}>
                        {isUp ? '▲' : '▼'} {trend}
                    </span>
                </div>

                {/* 제목 */}
                <p className="text-sm text-gray-500 mb-1 font-medium group-hover:text-gray-600 transition-colors">
                    {title}
                </p>

                {/* 값 (핵심 지표) */}
                <h2 className="text-2xl font-extrabold text-gray-800 tracking-tight">
                    {value}
                </h2>
            </div>
        </Link>
    );


};

export default DashSummaryCard;