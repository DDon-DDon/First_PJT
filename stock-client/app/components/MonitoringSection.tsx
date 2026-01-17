"use client"
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChevronRight, ClipboardList, Info } from 'lucide-react';

const MonitoringSection = () => {
  const router = useRouter();
  const [activeFilter, setActiveFilter] = useState('HOT');

  const statusData = {
    'HOT': [
      { id: 1, name: '나이키 에어맥스 97', stock: 150, update: '2분 전', msg: '최근 1시간 내 주문 20건' },
      { id: 2, name: '아디다스 삼바 OG', stock: 80, update: '5분 전', msg: '조회수 급상승 중' },
      { id: 5, name: '뉴발란스 530', stock: 210, update: '10분 전', msg: '재입고 알림 신청 폭주' },
      { id: 6, name: '컨버스 척테일러', stock: 45, update: '15분 전', msg: 'SNS 바이럴 상품' },
      { id: 7, name: '크록스 클래식 클로그', stock: 300, update: '20분 전', msg: '여름 시즌 베스트셀러' },
    ],
    'LOW STOCK': [
      { id: 3, name: '애플 에어팟 프로 2', stock: 3, update: '10분 전', msg: '재고 보충 필요 (안전 재고 미달)' },
    ],
    'OUT OF STOCK': [
      { id: 4, name: '소니 WH-1000XM5', stock: 0, update: '1시간 전', msg: '판매 중지됨' },
    ],
  };

  const statuses = [
    { key: 'HOT', label: '인기 급상승', count: 12, color: 'text-red-600', border: 'bg-red-500' },
    { key: 'LOW STOCK', label: '부족', count: 5, color: 'text-orange-600', border: 'bg-orange-500' },
    { key: 'IN STOCK', label: '정상', count: 1240, color: 'text-green-600', border: 'bg-green-500' },
    { key: 'OUT OF STOCK', label: '품절', count: 2, color: 'text-gray-600', border: 'bg-gray-500' },
    { key: 'PENDING ORDER', label: '결제 대기', count: 8, color: 'text-blue-600', border: 'bg-blue-500' },
    { key: 'ORDER COMPLETED', label: '주문 완료', count: 45, color: 'text-indigo-600', border: 'bg-indigo-500' },
  ];

  return (
    <div className="bg-white overflow-hidden mb-8 ">
      {/* 1. 상단 가로 스크롤 탭 메뉴 */}
      <div className="relative border-b border-gray-100 bg-gray-50/30">
        <div className="flex overflow-x-auto no-scrollbar">
          {statuses.map((status) => (
            <button
              key={status.key}
              onClick={() => setActiveFilter(status.key)}
              className={`flex-none min-w-[130px] px-4 py-5 flex flex-col items-center transition-all relative ${activeFilter === status.key ? 'bg-white' : 'hover:bg-gray-100/50'
                }`}
            >
              <span className={`text-[11px] font-bold mb-1 tracking-tight ${activeFilter === status.key ? status.color : 'text-gray-400'}`}>
                {status.label}
              </span>
              <span className={`text-xl font-extrabold ${activeFilter === status.key ? 'text-gray-900' : 'text-gray-600'}`}>
                {status.count}
              </span>
              {/* 활성화 하단 바 */}
              {activeFilter === status.key && (
                <div className={`absolute bottom-0 left-0 right-0 h-[3px] ${status.border}`} />
              )}
            </button>
          ))}
        </div>
      </div>

      {/* 2. 제목 및 툴팁 영역 */}
      <div className="px-6 pt-6 pb-4 flex justify-between items-center bg-white">
        <h4 className="font-bold flex items-center gap-2 text-gray-800 text-base">
          <ClipboardList size={18} className="text-gray-400" />
          {statuses.find(s => s.key === activeFilter)?.label} 상세 현황
        </h4>

        <div className="group relative">
          <div className="p-1.5 hover:bg-gray-100 rounded-full cursor-help transition-colors text-gray-400">
            <Info size={18} />
          </div>
          <div className="absolute right-0 top-9 w-60 p-3 bg-gray-800 text-white text-[11px] rounded-lg opacity-0 group-hover:opacity-100 transition-opacity z-20 pointer-events-none shadow-xl leading-relaxed border border-gray-700">
            이 메뉴는 최근 n개의 태그별 히스토리의 요약을 확인하실 수 있습니다.
            <div className="absolute -top-1 right-3 w-2 h-2 bg-gray-800 rotate-45 border-t border-l border-gray-700"></div>
          </div>
        </div>
      </div>

      {/* 3. 고정 높이 데이터 영역 (세로 스크롤 적용) */}
      <div className="px-6 pb-6 bg-white">
        <div className="h-[256px] overflow-y-auto pr-2 custom-scrollbar">
          {(statusData[activeFilter as keyof typeof statusData] || []).length > 0 ? (
            <div className="space-y-3">
              {statusData[activeFilter as keyof typeof statusData]?.map((item) => (
                <div 
                onClick={() => router.push(`/stocks/${item.id}`)}
                key={item.id} className="flex items-center justify-between p-4 rounded-xl border border-gray-100 bg-white hover:border-green-300 hover:shadow-sm transition-all cursor-pointer group">
                  <div className="flex flex-col">
                    <span className="font-bold text-sm text-gray-800 group-hover:text-green-600 transition-colors">{item.name}</span>
                    <span className="text-[11px] text-gray-500 mt-1 flex items-center gap-1">
                      <span className="w-1 h-1 bg-green-400 rounded-full"></span> {item.msg}
                    </span>
                  </div>
                  <div className="flex items-center gap-6 text-right">
                    <div>
                      <p className="text-[10px] text-gray-400 font-bold uppercase">Stock</p>
                      <p className="font-bold text-sm text-gray-700">{item.stock.toLocaleString()} EA</p>
                    </div>
                    <div className="w-20">
                      <p className="text-[10px] text-gray-400 font-bold uppercase">Time</p>
                      <p className="text-xs text-gray-600">{item.update}</p>
                    </div>
                    <ChevronRight size={16} className="text-gray-300 group-hover:text-green-500 group-hover:translate-x-1 transition-all" />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center border-2 border-dashed border-gray-50 rounded-2xl bg-gray-50/30">
              <div className="p-4 bg-white rounded-full shadow-sm mb-3 text-gray-200">
                <ClipboardList size={40} />
              </div>
              <p className="text-gray-400 text-sm font-medium">현재 '{activeFilter}' 상태의 데이터가 없습니다.</p>
              <p className="text-gray-300 text-xs mt-1">새로운 알림이 발생하면 이곳에 표시됩니다.</p>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #cbd5e1; }
      `}</style>
    </div>
  );
};

export default MonitoringSection;