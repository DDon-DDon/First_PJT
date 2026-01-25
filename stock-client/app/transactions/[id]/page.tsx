'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation'; // 뒤로가기 기능을 위해 추가
import { Toaster, toast } from 'react-hot-toast';

import {
    PlusIcon,
    MinusIcon,
    User,
    CheckCircle2,
    Package,
    TrendingUp,
    ChevronDown,
    ArrowLeft
} from 'lucide-react';

import ImagePreviewDialog from '../../components/ImagePreviewDialog';
import HistoryTable from '@/app/components/HistoryTable';

interface StockTransactionsProps {
    productId?: string;
}

const PRODUCT_IMAGES = [
    'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80',
    'https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=800&q=80',
    'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&q=80'
];

const STAFF_LIST = [
    { id: 's1', name: 'Alex Morgan' },
    { id: 's2', name: 'Sarah Connor' },
    { id: 's3', name: 'John Doe' },
    { id: 's4', name: 'Jane Smith' }
];  

const STOCK_REASONS = [
    '구매 주문', // purchase order
    '재고 조정', // inventory adjustment
    '고객 반품',  // customer return
    '기타'      // others
];

export default function TransactionDetail({ productId }: StockTransactionsProps) {
    const router = useRouter();

    const [quantity, setQuantity] = useState(50);
    const [openPreview, setOpenPreview] = useState(false);
    const [transactionType, setTransactionType] = useState<'in' | 'out'>('in');

    const [currentImgIdx, setCurrentImgIdx] = useState(0); // 캐러셀 상태

    const currentStock = 3420;
    const handleIncrease = () => setQuantity(prev => prev + 1);
    const handleDecrease = () => setQuantity(prev => (prev > 0 ? prev - 1 : 0));

    const product = {
        name: "애플 워치 시리즈 8 GPS 41mm 스타라이트 알루미늄 케이스",
        brand: "APPLE",
        category: "Wearables",
        sku: "APL-W8-GPS-STRLIGHT",
        lastInbound: "2024-03-21"
    };

    return (
        <main className="flex-1 overflow-y-auto">
            <Toaster position="bottom-right" /> {/* 토스트가 나올 자리 */}
            {/* max-w를 조정하고 px를 메인과 통일 (px-6 ~ px-8) */}
            <div className="max-w-[1600px] mx-auto px-8 py-8">
                <div className="max-w-[1200px] mx-auto space-y-10 animate-in fade-in duration-500">
                    {/* 상단 네비게이션 및 타입 선택 */}
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                        <div className="flex items-center gap-4">
                            <button
                                className="p-2.5 hover:bg-slate-100 rounded-full transition-colors text-slate-500"
                                onClick={() => router.back()}
                            >
                                <ArrowLeft size={22} />
                            </button>
                            <div>
                                <h2 className="text-sm font-bold text-blue-600 uppercase tracking-tight">{product.brand}</h2>
                                <h1 className="text-2xl font-black text-slate-900 leading-tight">재고 입출고 처리</h1>
                            </div>
                        </div>

                        {/* 입고/출고 스위치 (이미지 상단 탭 스타일 반영) */}
                        <div className="inline-flex p-1 bg-slate-100 rounded-xl w-fit">
                            <button
                                onClick={() => {
                                    setTransactionType('in')
                                }}
                                className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${transactionType === 'in' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                            >
                                재고 입고
                            </button>
                            <button
                                onClick={() => {
                                    setTransactionType('out')
                                }}
                                className={`px-6 py-2 rounded-lg text-sm font-bold transition-all ${transactionType === 'out' ? 'bg-white text-rose-600 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
                            >
                                재고 출고
                            </button>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                        {/* 좌측: 상품 이미지 및 썸네일 (첨부 이미지 스타일) */}
                        <div className="lg:col-span-5 space-y-6">
                            <div
                                className="aspect-square bg-slate-50 rounded-[2.5rem] overflow-hidden border border-slate-100 shadow-inner flex items-center justify-center cursor-zoom-in group relative"
                                onClick={() => setOpenPreview(true)}
                            >
                                <img src={PRODUCT_IMAGES[currentImgIdx]} alt="Product" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                                <div className="absolute bottom-6 right-6 bg-white/80 backdrop-blur px-3 py-1.5 rounded-full text-[10px] font-bold text-slate-500 border border-slate-200 shadow-sm">
                                    클릭하여 확대
                                </div>
                            </div>
                            <div className="flex gap-4 justify-center lg:justify-start">
                                {PRODUCT_IMAGES.map((img, i) => (
                                    <div
                                        key={i}
                                        className={`w-20 h-20 rounded-2xl border-2 transition-all overflow-hidden ${i === currentImgIdx ? 'border-blue-500 ring-4 ring-blue-50' : 'border-slate-100 opacity-50'}`}
                                        onClick={() => setCurrentImgIdx(i)}
                                    >
                                        <img src={img} className="w-full h-full object-cover" />
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* 우측: 정보 및 트랜잭션 폼 */}
                        <div className="lg:col-span-7 space-y-8">
                            {/* 상품 제목 섹션 */}
                            <div className="space-y-3 pb-6 border-b border-slate-100">
                                <div className="flex items-center gap-2 text-xs font-bold text-slate-400">
                                    <span>{product.category}</span>
                                    <span className="w-1 h-1 rounded-full bg-slate-300"></span>
                                    <span>SKU: {product.sku}</span>
                                </div>
                                <h2 className="text-3xl font-black text-slate-900 leading-snug">
                                    {product.name}
                                </h2>
                            </div>

                            {/* 핵심 지표 (현 재고 / 변동 예정) */}
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-white border border-slate-100 rounded-3xl p-6 shadow-sm space-y-3">
                                    <div className="flex items-center gap-2 text-slate-400">
                                        <Package size={18} />
                                        <span className="text-xs font-bold uppercase tracking-wider">현재 재고</span>
                                    </div>
                                    <div className="flex items-baseline gap-1">
                                        <span className="text-3xl font-black text-slate-900">{currentStock.toLocaleString()}</span>
                                        <span className="text-xs font-bold text-slate-400">UNITS</span>
                                    </div>
                                </div>
                                <div className={`border rounded-3xl p-6 shadow-sm space-y-3 transition-colors ${transactionType === 'in' ? 'bg-blue-50/50 border-blue-100' : 'bg-rose-50/50 border-rose-100'}`}>
                                    <div className="flex items-center gap-2 text-slate-400">
                                        <TrendingUp size={18} />
                                        <span className="text-xs font-bold uppercase tracking-wider">처리 후 예상</span>
                                    </div>
                                    <div className="flex items-baseline gap-1">
                                        <span className={`text-3xl font-black ${transactionType === 'in' ? 'text-blue-600' : 'text-rose-600'}`}>
                                            {(transactionType === 'in' ? currentStock + quantity : currentStock - quantity).toLocaleString()}
                                        </span>
                                        <span className="text-xs font-bold text-slate-400">UNITS</span>
                                    </div>
                                </div>
                            </div>

                            {/* 입력 폼 그리드 */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* 수량 조절기 */}
                                <div className="space-y-3">
                                    <label className="text-xs font-black text-slate-400 uppercase ml-1">수량 설정</label>
                                    <div className="flex items-center h-16 bg-slate-50 rounded-2xl border border-slate-100 p-2">
                                        <button onClick={handleDecrease} className="h-full w-12 flex items-center justify-center bg-white rounded-xl shadow-sm hover:bg-slate-50 transition-colors">
                                            <MinusIcon size={20} className="text-slate-600" />
                                        </button>
                                        <div className="flex-1 text-center text-xl font-black text-slate-900">
                                            {quantity}
                                        </div>
                                        <button onClick={handleIncrease} className="h-full w-12 flex items-center justify-center bg-white rounded-xl shadow-sm hover:bg-slate-50 transition-colors">
                                            <PlusIcon size={20} className="text-slate-600" />
                                        </button>
                                    </div>
                                </div>

                                {/* 담당자 선택 */}
                                <div className="space-y-3">
                                    <label className="text-xs font-black text-slate-400 uppercase ml-1">담당자</label>
                                    <div className="relative">
                                        <User size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                                        <select className="w-full h-16 pl-12 pr-10 bg-slate-50 border border-slate-100 rounded-2xl appearance-none font-bold text-slate-700 focus:ring-2 focus:ring-blue-500 transition-all">
                                            {
                                                STAFF_LIST .map(staff => (
                                                    <option key={staff.id}>{staff.name}</option>
                                                ))
                                            }
                                        </select>
                                        <ChevronDown size={18} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
                                    </div>
                                </div>

                                {/* 사유/참조 */}
                                <div className="md:col-span-2 space-y-3">
                                    <label className="text-xs font-black text-slate-400 uppercase ml-1">입출고 사유 및 참조번호</label>
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                        <select className="h-14 px-4 bg-white border border-slate-200 rounded-xl font-bold text-slate-700">
                                            {
                                                STOCK_REASONS.map((reason, idx) => (
                                                    <option key={idx}>{reason}</option>
                                                ))
                                            }
                                        </select>
                                        <input
                                            type="text"
                                            placeholder="참조 번호를 입력하세요 (예: PO-123)"
                                            className="h-14 px-4 bg-white border border-slate-200 rounded-xl font-medium focus:ring-2 focus:ring-blue-500 outline-none"
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* 최종 확인 버튼 */}
                            <div className="pt-6 flex gap-4">
                                <button 
                                    onClick={()=>{
                                        toast.success(`재고 ${transactionType === 'in' ? '입고' : '출고'}가 완료되었습니다!`);
                                    }}
                                    className={`flex-1 h-16 rounded-2xl flex items-center justify-center gap-3 text-white font-black text-lg shadow-lg shadow-blue-200 transition-transform active:scale-95 ${transactionType === 'in' ? 'bg-blue-600' : 'bg-rose-600 shadow-rose-200'}`}>
                                    <CheckCircle2 size={24} />
                                    {transactionType === 'in' ? '입고 완료하기' : '출고 완료하기'}
                                </button>
                                <button 
                                    onClick={() => router.back()}
                                    className="px-8 h-16 bg-slate-100 rounded-2xl font-bold text-slate-500 hover:bg-slate-200 transition-colors">
                                    취소
                                </button>
                            </div>
                        </div>
                    </div>
                    <HistoryTable />
                    {openPreview && (
                        <ImagePreviewDialog
                            imgUrl={PRODUCT_IMAGES[currentImgIdx]}
                            isOpen={openPreview}
                            onClose={() => setOpenPreview(false)}
                        />
                    )}
                </div>
            </div>
        </main>
    );
}