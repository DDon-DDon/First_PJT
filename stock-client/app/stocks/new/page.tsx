'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
    ArrowLeft, Upload, Save, Package, BadgePercent, Coins,
    Calendar as CalendarIcon, User, FileText, ChevronDown, Plus, Minus, X
} from 'lucide-react';
import Link from 'next/link';

export default function NewProductPage() {
    const router = useRouter();

    // 상태 관리
    const [currency, setCurrency] = useState('KRW');
    const [regDate, setRegDate] = useState(new Date().toISOString().split('T')[0]);
    const [stockQty, setStockQty] = useState(0);
    const [minOrder, setMinOrder] = useState(1);
    const [isMemoOpen, setIsMemoOpen] = useState(false);
    const [memo, setMemo] = useState('');

    // 카운터 핸들러
    const handleCount = (type: 'stock' | 'unit', op: 'plus' | 'minus') => {
        if (type === 'stock') {
            setStockQty(prev => op === 'plus' ? prev + 1 : Math.max(0, prev - 1));
        } else {
            setMinOrder(prev => op === 'plus' ? prev + 1 : Math.max(1, prev - 1));
        }
    };

    return (
        <main className="flex-1 overflow-y-auto bg-slate-50 dark:bg-[#101922] relative">
            <div className="max-w-[1100px] mx-auto px-8 py-8">

                {/* 헤더 영역 */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-4">
                        <Link href="/stocks" className="p-2 hover:bg-white dark:hover:bg-slate-800 rounded-full border border-transparent hover:border-slate-200 transition-all">
                            <ArrowLeft size={20} />
                        </Link>
                        <div>
                            <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">Add New Stock</h2>
                        </div>
                    </div>
                    <div className="flex items-center gap-3">
                        <button
                            onClick={() => setIsMemoOpen(true)}
                            className="cursor-pointer flex items-center gap-2 px-6 py-2.5 bg-gray-500 text-white font-bold rounded-full hover:bg-gray-600 shadow-lg shadow-gray-500/20 transition-all"
                        >
                            <FileText size={18} /> {memo ? 'Memo' : 'Memo'}
                        </button>
                        <button className="cursor-pointer flex items-center gap-2 px-6 py-2.5 bg-blue-600 text-white font-bold rounded-full hover:bg-blue-700 shadow-lg shadow-blue-500/20 transition-all">
                            <Save size={18} /> Save Item
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    <div className="lg:col-span-2 flex flex-col gap-6">

                        {/* 기본 정보 */}
                        <section className="bg-white dark:bg-slate-900 p-7 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                            <div className="flex items-center gap-2 mb-6 text-blue-600">
                                <Package size={20} strokeWidth={2.5} />
                                <h3 className="font-bold text-lg">기본 정보</h3>
                            </div>
                            <div className="grid grid-cols-1 gap-6">
                                <div>
                                    <label className="block text-[13px] font-bold text-slate-500 mb-2 ml-1">상품명</label>
                                    <input type="text" placeholder="상품 이름을 입력하세요" className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500/20" />
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-[13px] font-bold text-slate-500 mb-2 ml-1">상품 코드 (SKU)</label>
                                        <input type="text" placeholder="SKU-0000" className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl outline-none" />
                                    </div>
                                    <div>
                                        <label className="block text-[13px] font-bold text-slate-500 mb-2 ml-1">주문 번호 (Ref.)</label>
                                        <input type="text" placeholder="REF-0000" className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl outline-none" />
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* 가격 및 수량 (카운터 유닛 적용) */}
                        <section className="bg-white dark:bg-slate-900 p-7 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                            <div className="flex items-center gap-2 mb-6 text-emerald-600">
                                <Coins size={20} strokeWidth={2.5} />
                                <h3 className="font-bold text-lg">상품 정보 설정</h3>
                            </div>

                            <div className="flex flex-col gap-6">
                                {/* 행 1: 제품 가격 (통화 선택 + 금액 한 행 배치) */}
                                <div>
                                    <label className="block text-[13px] font-bold text-slate-500 mb-2 ml-1">제품 가격</label>
                                    <div className="flex gap-2">
                                        <div className="relative">
                                            <select
                                                value={currency}
                                                onChange={(e) => setCurrency(e.target.value)}
                                                className="appearance-none pl-4 pr-10 py-3 bg-slate-100 dark:bg-slate-800 border-none rounded-2xl font-bold text-sm outline-none cursor-pointer h-full"
                                            >
                                                <option value="KRW">₩ KRW</option>
                                                <option value="USD">$ USD</option>
                                            </select>
                                            <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                                        </div>
                                        <input
                                            type="number"
                                            placeholder="0"
                                            className="flex-1 px-4 py-3 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl outline-none font-semibold focus:ring-2 focus:ring-emerald-500/20"
                                        />
                                    </div>
                                </div>

                                {/* 행 2: 시즌 할인 정책 (수직으로 다음 행 배치) */}
                                <div>
                                    <label className="block text-[13px] font-bold text-slate-500 mb-2 ml-1">시즌 할인 정책</label>
                                    <div className="relative">
                                        <select className="w-full appearance-none pl-11 pr-4 py-3 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl outline-none font-medium cursor-pointer focus:ring-2 focus:ring-emerald-500/20">
                                            <option value="">할인 정책 선택</option>
                                            <option value="10">시즌 오프 (10%)</option>
                                            <option value="20">블랙 프라이데이 (20%)</option>
                                            <option value="30">창고 대개방 (30%)</option>
                                        </select>
                                        <BadgePercent size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                                        <ChevronDown size={16} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
                                    </div>
                                </div>

                                {/* 행 3: 상품 수량 및 계수 유닛 (가로 병렬 유지) */}
                                <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-50 dark:border-slate-800">
                                    {[
                                        { label: '상품 수량', val: stockQty, type: 'stock' },
                                        { label: '계수 유닛 (Min Order)', val: minOrder, type: 'unit' }
                                    ].map((item) => (
                                        <div key={item.type}>
                                            <label className="block text-[13px] font-bold text-slate-500 mb-2 ml-1">{item.label}</label>
                                            <div className="flex items-center justify-between p-2 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl">
                                                <button
                                                    onClick={() => handleCount(item.type as any, 'minus')}
                                                    className="p-2 hover:bg-white dark:hover:bg-slate-700 rounded-xl transition-all shadow-sm"
                                                >
                                                    <Minus size={16} />
                                                </button>
                                                <span className="font-bold text-lg">{item.val}</span>
                                                <button
                                                    onClick={() => handleCount(item.type as any, 'plus')}
                                                    className="p-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-all shadow-md shadow-blue-500/20"
                                                >
                                                    <Plus size={16} />
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </section>
                    </div>

                    {/* 오른쪽 컬럼 */}
                    <div className="flex flex-col gap-6">
                        <section className="bg-white dark:bg-slate-900 p-7 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm text-center">
                            <h3 className="font-bold text-lg mb-4 text-left">상품 이미지</h3>
                            <div className="aspect-square w-full bg-slate-50 dark:bg-slate-800/50 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl flex flex-col items-center justify-center gap-4 cursor-pointer hover:bg-blue-50/50 transition-all group">
                                <div className="p-4 bg-white dark:bg-slate-900 rounded-2xl shadow-sm text-slate-400 group-hover:text-blue-500 transition-all"><Upload size={16} /></div>
                                <p className="text-sm font-bold text-slate-700 dark:text-slate-200">클릭 또는 드래그</p>
                            </div>
                        </section>

                        <section className="bg-slate-900 text-white p-7 rounded-xl">
                            <h3 className="font-bold text-[11px] uppercase tracking-widest text-slate-400 mb-6">Metadata</h3>
                            <div className="space-y-6">
                                <div>
                                    <label className="block text-[10px] text-slate-400 font-bold mb-2 uppercase">Registered By</label>
                                    <div className="relative">
                                        <select className="w-full appearance-none bg-slate-800 border-none rounded-xl px-10 py-3 text-sm font-bold outline-none cursor-pointer">
                                            <option>Alex Morgan</option>
                                            <option>Jordan Smith</option>
                                            <option>Sarah Connor</option>
                                        </select>
                                        <User size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-blue-400" />
                                        <ChevronDown size={14} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-[10px] text-slate-400 font-bold mb-2 uppercase">Registration Date</label>
                                    <div className="relative">
                                        <input type="date" value={regDate} onChange={(e) => setRegDate(e.target.value)} className="w-full bg-slate-800 border-none rounded-xl px-10 py-3 text-sm font-bold outline-none cursor-pointer [color-scheme:dark]" />
                                        <CalendarIcon size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-orange-400 pointer-events-none" />
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                </div>
            </div>

            {/* 메모 등록 다이얼로그 (Portal 대용) */}
            {isMemoOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-200">
                    <div className="bg-white dark:bg-slate-900 w-full max-w-lg rounded-3xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden">
                        <div className="flex items-center justify-between p-6 border-b border-slate-100 dark:border-slate-800">
                            <h3 className="font-bold text-xl flex items-center gap-2">
                                <FileText className="text-blue-600" size={20} /> Product Memo
                            </h3>
                            <button onClick={() => setIsMemoOpen(false)} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-all"><X size={20} /></button>
                        </div>
                        <div className="p-6">
                            <textarea
                                value={memo}
                                onChange={(e) => setMemo(e.target.value)}
                                rows={6}
                                placeholder="내부 전달 사항이나 메모를 입력하세요..."
                                className="w-full p-4 bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500/20"
                            />
                        </div>
                        <div className="p-6 bg-slate-50 dark:bg-slate-800/50 flex justify-end gap-3">
                            <button onClick={() => setIsMemoOpen(false)} className="px-5 py-2.5 font-bold text-slate-500 hover:text-slate-700">Cancel</button>
                            <button onClick={() => setIsMemoOpen(false)} className="px-6 py-2.5 bg-blue-600 text-white font-bold rounded-full hover:bg-blue-700 shadow-lg shadow-blue-500/20">Save Memo</button>
                        </div>
                    </div>
                </div>
            )}
        </main>
    );
}