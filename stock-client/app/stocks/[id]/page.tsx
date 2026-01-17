"use client";
// app/stocks/[id]/page.tsx
import Link from 'next/link';

interface PageProps {
  params: Promise<{ id: string }>;
}
import React, { useState, use } from 'react';
import {
  ChevronLeft, ChevronRight, Edit3, History, Truck,
  Package, Calendar, User, Tag, Hash, ArrowUpRight, ArrowDownRight,
  TrendingDown, Box
} from 'lucide-react';

// --- 샘플 데이터 타입 ---
interface HistoryLog {
  date: string;
  type: '입고' | '출고' | '등록';
  amount: number;
  status: string;
}

export default function ProductDetailView({ params }: PageProps) {
  // 1. Next.js 15 방식에 맞춰 params 언랩
  const resolvedParams = use(params);
  const productId = resolvedParams.id;

  // 2. 이제 useState를 정상적으로 사용할 수 있습니다.
  const [currentImg, setCurrentImg] = useState(0);
  const images = [
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800",
    "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800",
    "https://images.unsplash.com/photo-1586920740199-47ce35183cfd?w=800"
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 pb-20 overflow-y-auto">
      {/* 상단 액션 바 */}
      <div className="sticky top-0 z-30 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-100 dark:border-slate-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <nav className="flex gap-2 text-[11px] text-slate-400 font-bold uppercase tracking-wider">
            <span>Inventory</span>
            <span>/</span>
            <span className="text-blue-600">Product Analysis</span>
          </nav>


          <Link
            key={`go-to-edit`}
            href={`/stocks/${productId}/edit`}
            className="block" // Link가 전체 영역을 차지하도록 설정
          >
            <button className="flex items-center gap-2 px-4 py-2 bg-slate-900 dark:bg-blue-600 text-white rounded-lg text-sm font-bold hover:opacity-90 transition-all">
              <Edit3 size={16} />
              상품 정보 수정
            </button>
          </Link>


        </div>
      </div>

      <main className="max-w-6xl mx-auto px-6 pt-10">
        <div className="grid grid-cols-12 gap-12">

          {/* 좌측: 상품 이미지 캐로셀 (디자인 핵심) */}
          <div className="col-span-12 lg:col-span-6 space-y-4">
            <div className="relative aspect-square rounded-2xl overflow-hidden bg-slate-100 group">
              <img
                src={images[currentImg]}
                alt="Product"
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <div className="absolute inset-0 flex items-center justify-between px-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <button onClick={() => setCurrentImg(0)} className="p-2 bg-white/50 backdrop-blur-md rounded-full hover:bg-white"><ChevronLeft /></button>
                <button onClick={() => setCurrentImg(1)} className="p-2 bg-white/50 backdrop-blur-md rounded-full hover:bg-white"><ChevronRight /></button>

              </div>
            </div>
            <div className="flex gap-4">
              {images.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentImg(i)}
                  className={`w-20 h-20 rounded-lg overflow-hidden border-2 transition-all ${currentImg === i ? 'border-blue-600' : 'border-transparent opacity-50'}`}
                >
                  <img src={img} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          </div>

          {/* 우측: 핵심 정보 섹션 */}
          <div className="col-span-12 lg:col-span-6 space-y-8">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold text-blue-600 uppercase tracking-tighter">APPLE</span>
                <span className="text-slate-300">|</span>
                <span className="text-sm text-slate-500">Wearables</span>
              </div>
              <h1 className="text-3xl font-bold text-slate-900 dark:text-white leading-tight">
                애플 워치 시리즈 8 GPS 41mm<br />스타라이트 알루미늄 케이스
              </h1>
            </div>

            {/* 가격 정보 카드 */}
            <div className="bg-slate-50 dark:bg-slate-900/50 rounded-2xl p-6 border border-slate-100 dark:border-slate-800">
              <div className="grid grid-cols-2 gap-8">
                <div>
                  <label className="text-[11px] font-bold text-slate-400 uppercase mb-1 block">주문가 (단위 유닛)</label>
                  <p className="text-2xl font-black text-slate-900 dark:text-white">$399.00</p>
                </div>
                <div>
                  <label className="text-[11px] font-bold text-slate-400 uppercase mb-1 block">출하 가격</label>
                  <p className="text-2xl font-black text-emerald-600">$450.00</p>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 flex items-center gap-1">
                  <TrendingDown size={14} /> 가격 할인 정책
                </span>
                <span className="text-xs font-bold text-rose-600 bg-rose-50 px-2 py-1 rounded">Spring Sale (-10%)</span>
              </div>
            </div>

            {/* 재고 상태 요약 */}
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 border border-slate-100 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900 shadow-sm">
                <div className="flex items-center gap-2 text-slate-400 mb-2">
                  <Box size={16} />
                  <span className="text-xs font-bold uppercase">현재 수량</span>
                </div>
                <p className="text-xl font-bold text-blue-600">3,420 <span className="text-xs text-slate-400 font-medium">Units</span></p>
              </div>
              <div className="p-4 border border-slate-100 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900 shadow-sm">
                <div className="flex items-center gap-2 text-slate-400 mb-2">
                  <TrendingDown size={16} />
                  <span className="text-xs font-bold uppercase">최근 입출고</span>
                </div>
                <p className="text-xl font-bold text-rose-600">-24 <span className="text-xs text-slate-400 font-medium">Units</span></p>
              </div>
            </div>

            {/* 메타데이터 상세 */}
            <div className="grid grid-cols-2 gap-y-4 text-sm border-t border-slate-100 dark:border-slate-800 pt-6">
              <MetaRow icon={<Hash size={14} />} label="SKU" value="APL-W8-GPS-STRLIGHT" />
              <MetaRow icon={<Calendar size={14} />} label="등록일" value="2024-01-16" />
              <MetaRow icon={<User size={14} />} label="등록자" value="Alex Morgan" />
              <MetaRow icon={<Tag size={14} />} label="카테고리" value="Electronics" />
            </div>
          </div>
        </div>

        {/* 하단: 히스토리 테이블 섹션 */}
        <div className="mt-20 space-y-12">
          {/* 11. 입출고 이력 */}
          <section className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <History className="text-blue-600" /> 제품 입출고 이력
              </h3>
              <button className="text-xs font-bold text-slate-400 hover:text-blue-600">전체보기</button>
            </div>
            <div className="overflow-hidden border border-slate-100 dark:border-slate-800 rounded-2xl shadow-sm">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 dark:bg-slate-900 border-b border-slate-100 dark:border-slate-800">
                  <tr>
                    <th className="px-6 py-4 font-bold text-slate-500">날짜</th>
                    <th className="px-6 py-4 font-bold text-slate-500">유형</th>
                    <th className="px-6 py-4 font-bold text-slate-500">수량 변화</th>
                    <th className="px-6 py-4 font-bold text-slate-500">상태</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  <HistoryTableRow date="2024-05-20 14:30" type="출고" amount={-2} status="검수 완료" />
                  <HistoryTableRow date="2024-05-18 09:15" type="입고" amount={150} status="입고 완료" />
                  <HistoryTableRow date="2024-05-15 11:20" type="등록" amount={0} status="신규 상품 등록" />
                </tbody>
              </table>
            </div>
          </section>

          {/* 12. 택배사 운송 이력 */}
          <section className="space-y-6">
            <h3 className="text-xl font-bold flex items-center gap-2">
              <Truck className="text-blue-600" /> 택배사 운송 이력
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <LogisticsCard carrier="CJ대한통운" trackNum="5682-1923-XXXX" status="배송완료" lastDate="2024-05-21" />
              <LogisticsCard carrier="한진택배" trackNum="1022-4412-XXXX" status="배송중" lastDate="2024-05-22" />
              <LogisticsCard carrier="우체국택배" trackNum="6033-2190-XXXX" status="간선하차" lastDate="2024-05-22" />
            </div>
          </section>
        </div>
      </main>

      {/* 플로팅 액션 버튼 */}
      <div className="fixed bottom-8 right-8 flex flex-col gap-3">
        <button className="w-14 h-14 bg-blue-600 text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 transition-transform">
          <History size={24} />
        </button>
      </div>
    </div>
  );
};

// --- 서브 컴포넌트 ---

const MetaRow = ({ icon, label, value }: { icon: any, label: string, value: string }) => (
  <div className="flex items-center gap-3">
    <div className="text-slate-400">{icon}</div>
    <div>
      <p className="text-[10px] font-bold text-slate-400 uppercase leading-none mb-1">{label}</p>
      <p className="font-semibold text-slate-700 dark:text-slate-300">{value}</p>
    </div>
  </div>
);

const HistoryTableRow = ({ date, type, amount, status }: HistoryLog) => (
  <tr className="hover:bg-slate-50 dark:hover:bg-slate-900/50 transition-colors">
    <td className="px-6 py-4 text-slate-500 font-medium">{date}</td>
    <td className="px-6 py-4">
      <span className={`px-2 py-1 rounded text-[11px] font-bold ${type === '입고' ? 'bg-blue-50 text-blue-600' : type === '출고' ? 'bg-rose-50 text-rose-600' : 'bg-slate-100 text-slate-600'
        }`}>{type}</span>
    </td>
    <td className="px-6 py-4 font-bold">
      {amount > 0 ? <span className="text-blue-600">+{amount}</span> : amount < 0 ? <span className="text-rose-600">{amount}</span> : '-'}
    </td>
    <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{status}</td>
  </tr>
);

const LogisticsCard = ({ carrier, trackNum, status, lastDate }: any) => (
  <div className="p-5 border border-slate-100 dark:border-slate-800 rounded-2xl bg-white dark:bg-slate-900 shadow-sm">
    <div className="flex justify-between items-start mb-4">
      <div className="bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-[10px] font-bold text-slate-500">{carrier}</div>
      <span className="text-[11px] font-bold text-blue-600">{status}</span>
    </div>
    <p className="text-sm font-bold text-slate-800 dark:text-white mb-1">{trackNum}</p>
    <p className="text-[11px] text-slate-400">마지막 위치: {lastDate}</p>
  </div>
);

