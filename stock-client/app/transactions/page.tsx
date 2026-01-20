"use client"; // 클라이언트 컴포넌트 선언

import React, { useState, use } from 'react'; // 'use' 추가
import {
  Search, Download, Upload, ChevronLeft,
  ChevronRight, MoreVertical, Filter, X
} from 'lucide-react';

import { useRouter } from 'next/navigation'; // 뒤로가기 기능을 위해 추가

// 1. 더미 데이터 (컴포넌트 외부 배치)
const PRODUCT_IMAGE = 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80';
const ALL_DATA = Array.from({ length: 20 }).map((_, i) => ({
  id: `${2024001 + i}`,
  date: `2023-10-${24 - (i % 5)}`,
  productName: i % 3 === 0 ? '애플워치 시리즈 8 GPS' : '무선 마우스 M30',
  sku: i % 3 === 0 ? 'SW-701-GRY' : 'WM-302-BLK',
  type: i % 2 === 0 ? 'IN' : 'OUT',
  quantity: 10 + i,
  status: i % 4 === 0 ? '대기중' : '완료',
  person: i % 2 === 0 ? '홍길동' : '김철수'
}));

// Props 타입 정의
interface PageProps {
  searchParams: Promise<{ view?: string }>;
}

/**
 * [주의] export default async function 아님! 
 * 클라이언트 컴포넌트는 일반 function이어야 함.
 */
export default function TransactionPage({ searchParams }: PageProps) {
  // 2. Next.js 15 필수: searchParams가 Promise이므로 use()로 풀어서 사용
  const resolvedParams = use(searchParams);
  const viewId = resolvedParams.view;
  const router = useRouter();


  // 3. 이제 클라이언트 훅들을 안전하게 사용 가능
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  const [filters, setFilters] = useState([
    { id: 'f1', label: '입고' },
    { id: 'f2', label: '완료' }
  ]);

  // 페이징 계산
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = ALL_DATA.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(ALL_DATA.length / itemsPerPage);

  const removeFilter = (id: string) => {
    setFilters(filters.filter(f => f.id !== id));
  };

  const handleRowClick = (id: string) => {
    router.push(`/transactions/${id}`);
  };

  return (
    <main className="flex-1 bg-[#f5f6f7] min-h-screen pb-20 overflow-y-auto">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="space-y-5">
          {/* 헤더 섹션 */}
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-slate-900">입출고 이력 관리</h1>
            <div className="flex gap-2">
              <button className="flex items-center gap-1 px-3 h-9 border border-slate-300 bg-white text-sm rounded font-medium shadow-sm hover:bg-slate-50 transition-all">
                <Download size={14} /> 엑셀 다운로드
              </button>
              <button className="flex items-center gap-1 px-3 h-9 border border-slate-300 bg-white text-sm rounded font-medium shadow-sm hover:bg-slate-50 transition-all">
                <Upload size={14} /> 내역 업로드
              </button>
            </div>
          </div>

          {/* 검색 섹션 */}
          <div className="bg-white border border-slate-200 rounded shadow-sm p-6">
            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-4">
                <span className="text-sm font-bold text-slate-700 w-20">검색어</span>
                <div className="relative flex-1 max-w-xl">
                  <input
                    type="text"
                    placeholder="상품명, SKU, 담당자명으로 검색"
                    className="w-full h-10 pl-3 border border-slate-300 rounded focus:border-green-600 outline-none text-sm"
                  />
                  <Search className="absolute right-3 top-2.5 text-slate-400" size={18} />
                </div>
                <button className="px-6 h-10 bg-slate-800 text-white font-bold rounded text-sm hover:bg-slate-700">
                  검색
                </button>
              </div>

              <div className="flex items-center gap-4 pt-4 border-t border-slate-50">
                <span className="text-sm font-bold text-slate-700 w-20 flex items-center gap-1">
                  <Filter size={14} /> 필터
                </span>
                <div className="flex flex-wrap gap-2">
                  {filters.map((f) => (
                    <div key={f.id} className="flex items-center gap-1 px-2 py-1 bg-slate-100 border border-slate-200 rounded text-xs text-slate-600 font-medium">
                      {f.label}
                      <X size={12} className="cursor-pointer hover:text-red-500" onClick={() => removeFilter(f.id)} />
                    </div>
                  ))}
                  <button className="text-xs text-blue-600 font-bold ml-1 hover:underline">+ 상세 필터 추가</button>
                </div>
              </div>
            </div>
          </div>

          {/* 테이블 섹션 */}
          <div className="bg-white border border-slate-200 rounded shadow-sm overflow-hidden">
            <div className="px-6 py-3 border-b border-slate-100 bg-[#fcfcfc] flex justify-between">
              <span className="text-sm text-slate-600">조회 결과 <strong className="text-green-600">{ALL_DATA.length}</strong>건</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="bg-[#f8f9fa] border-b border-slate-200">
                    <th className="px-6 py-3 text-[12px] font-bold text-slate-600">상품코드</th>
                    <th className="px-6 py-3 text-[12px] font-bold text-slate-600">상품정보</th>
                    <th className="px-6 py-3 text-[12px] font-bold text-slate-600 text-center">구분</th>
                    <th className="px-6 py-3 text-[12px] font-bold text-slate-600 text-right">변동수량</th>
                    <th className="px-6 py-3 text-[12px] font-bold text-slate-600 text-center">상태</th>
                    <th className="px-6 py-3 text-[12px] font-bold text-slate-600">처리자</th>
                    <th className="px-6 py-3"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {currentItems.map((item) => (
                    <tr
                      key={item.id}
                      onClick={() => handleRowClick(item.id)}
                      className="hover:bg-slate-50 transition-colors group cursor-pointer"
                    >
                      <td className="px-6 py-4 font-mono text-xs text-slate-500">{item.sku}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <img src={PRODUCT_IMAGE} className="h-10 w-10 rounded border border-slate-200 object-cover" />
                          <div>
                            <div className="font-bold text-slate-800 text-sm">{item.productName}</div>
                            <div className="text-[11px] text-slate-400">{item.date}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-bold ${item.type === 'IN' ? 'bg-blue-50 text-blue-600 border border-blue-100' : 'bg-red-50 text-red-600 border border-red-100'
                          }`}>
                          {item.type === 'IN' ? '입고' : '출고'}
                        </span>
                      </td>
                      <td className={`px-6 py-4 text-right font-bold text-sm ${item.type === 'IN' ? 'text-blue-600' : 'text-red-600'}`}>
                        {item.type === 'IN' ? '+' : '-'}{item.quantity}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="text-[11px] px-2 py-0.5 bg-slate-100 text-slate-600 rounded-full border border-slate-200">
                          {item.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-slate-600 text-xs">{item.person}</td>
                      <td className="px-6 py-4 text-right">
                        <MoreVertical size={16} className="text-slate-300" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* 페이지네이션 */}
            <div className="py-6 flex justify-center items-center gap-1 border-t border-slate-100">
              <button className="p-2 border border-slate-200 rounded hover:bg-slate-50"><ChevronLeft size={16} /></button>
              {[1, 2, 3].map(n => (
                <button
                  key={n}
                  className={`w-9 h-9 text-sm rounded font-bold ${n === currentPage ? 'bg-green-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100 border border-transparent'}`}
                  onClick={(e) => { e.stopPropagation(); setCurrentPage(n); }}
                >
                  {n}
                </button>
              ))}
              <button className="p-2 border border-slate-200 rounded hover:bg-slate-50"><ChevronRight size={16} /></button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}