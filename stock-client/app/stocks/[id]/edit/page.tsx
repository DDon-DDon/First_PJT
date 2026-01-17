"use client";
import Link from 'next/link';
import React, { useState, use } from 'react';

interface PageProps {
    // 경로에 [id]가 포함되어 있으므로 동일하게 접근 가능합니다.
    params: Promise<{ id: string }>;
}

import {
    Save, X, Upload, DollarSign, Truck,
    Info, FileText, Plus, ChevronRight, Image as ImageIcon, Trash2,
    Calendar, User, Package, Building2
} from 'lucide-react';


// 샘플용
const tempImages = [
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800",
    "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800",
    "https://images.unsplash.com/photo-1586920740199-47ce35183cfd?w=800"
];

export default function EditProductPage({ params }: PageProps) {
    // 1. Next.js 15 방식에 맞춰 params 언랩
    const resolvedParams = use(params);
    const productId = resolvedParams.id;

    const [activeTab, setActiveTab] = useState('basic');
    const menuItems = [
        { id: 'basic', label: '기본 정보', icon: <Info size={18} /> },
        { id: 'pricing', label: '가격 및 재고', icon: <DollarSign size={18} /> },
        { id: 'logistics', label: '물류 및 파트너', icon: <Truck size={18} /> },
        { id: 'description', label: '상품 설명', icon: <FileText size={18} /> },
        { id: 'images', label: '상품 이미지', icon: <ImageIcon size={18} /> },
    ];

    return (
        <div className="flex flex-col min-h-screen bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100">

            {/* 1. 상단바 (화면 가로 전체 점유) */}
            <header className="h-16 w-full border-b border-slate-200 dark:border-slate-800 flex items-center justify-between px-6 bg-white dark:bg-slate-900 sticky top-0 z-50">
                <div className="flex items-center gap-4">
                    <div className="bg-blue-600 p-1.5 rounded text-white">
                        <Plus size={18} />
                    </div>
                    <h1 className="text-lg font-bold tracking-tight">상품 수정하기</h1>
                </div>

                <div className="flex items-center gap-2">

                    <Link
                        key={`go-to-stocks`}
                        href={`/stocks/`}
                        className="block" // Link가 전체 영역을 차지하도록 설정
                    >
                        <button className="px-4 py-2 text-sm font-medium text-slate-500 hover:bg-slate-100 rounded-lg transition-colors">
                            취소
                        </button>
                    </Link>

                    <button className="px-4 py-2 text-sm font-bold bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-sm transition-all flex items-center gap-2">
                        <Save size={16} /> 상품 정보 저장
                    </button>
                </div>
            </header>

            <div className="flex flex-1 overflow-hidden">
                {/* 2. 사이드바 (사이드에 착 붙음) */}
                <aside className="w-64 border-r border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 shrink-0 overflow-y-auto">
                    <nav className="p-4 space-y-1">
                        {menuItems.map((item) => (
                            <button
                                key={item.id}
                                onClick={() => setActiveTab(item.id)}
                                className={`w-full flex items-center justify-between px-4 py-3 rounded-lg text-sm font-semibold transition-all ${activeTab === item.id
                                    ? 'bg-white dark:bg-slate-800 text-blue-600 shadow-sm border border-slate-200 dark:border-slate-700'
                                    : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
                                    }`}
                            >
                                <div className="flex items-center gap-3">
                                    {item.icon}
                                    {item.label}
                                </div>
                                {activeTab === item.id && <ChevronRight size={14} />}
                            </button>
                        ))}
                    </nav>
                </aside>

                {/* 3. 메인 입력 영역 */}
                <main className="flex-1 overflow-y-auto bg-white dark:bg-slate-950 p-8">
                    <div className="max-w-4xl mx-auto md:mx-0">

                        {/* 탭 1: 기본 정보 (1, 2, 3, 4번 항목) */}
                        {activeTab === 'basic' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-left-2 duration-300">
                                <h3 className="text-xl font-bold">기본 정보</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                                    <Input label="* 상품명" placeholder="정확한 상품명을 입력하세요" />
                                    <Select label="상품 카테고리" options={['웨어러블', '전자기기', '의류', '식품']} />
                                    <Input label="* 상품 코드 (SKU)" placeholder="예: SKU-100234" />
                                    <Input label="* 주문 번호"
                                        placeholder="PO 번호를 입력하세요"
                                        value={productId}
                                        onChange={() => { console.log() }}
                                    />
                                </div>
                            </div>
                        )}

                        {/* 탭 2: 가격 및 재고 (5, 6, 7, 8번 항목) */}
                        {activeTab === 'pricing' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-left-2 duration-300">
                                <h3 className="text-xl font-bold">가격 및 재고 설정</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                                    <div className="flex gap-2">
                                        <div className="flex-[3]"><Input label="제품 가격" type="number" placeholder="0" /></div>
                                        <div className="flex-[2]"><Select label="통화 종류" options={['KRW (₩)', 'USD ($)', 'JPY (¥)']} /></div>
                                    </div>
                                    <Select label="제품 할인 정책" options={['할인 없음', '시즌 오프 (10%)', '신규 등록 (5%)', '대량 구매']} />
                                    <Counter label="* 상품 수량" unit="개" />
                                    <Counter label="* 상품 입출고 단위" unit="Box" />
                                </div>
                            </div>
                        )}

                        {/* 탭 3: 물류 및 파트너 (9, 10, 14, 15번 항목) */}
                        {activeTab === 'logistics' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-left-2 duration-300">
                                <h3 className="text-xl font-bold">물류 및 연결 정보</h3>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                                    <Select label="* 상품 등록자" options={['김철수 과장', '이영희 대리', '관리자']} />
                                    <Input label="* 등록 일자" type="date" />
                                    <Select label="택배사 정보" options={['CJ대한통운', '우체국택배', '한진택배', '로젠택배']} />
                                    <Select label="거래처 정보" options={['(주)에이비씨 유통', '(주)글로벌 파트너스', '직접 매입']} />
                                </div>
                            </div>
                        )}

                        {/* 탭 4: 상품 설명 (12번 항목) */}
                        {activeTab === 'description' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-left-2 duration-300">
                                <h3 className="text-xl font-bold">상품 상세 설명 (메모)</h3>
                                <textarea
                                    className="w-full h-80 p-4 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all resize-none"
                                    placeholder="상품에 대한 추가 메모나 상세 설명을 자유롭게 작성하세요."
                                />
                            </div>
                        )}

                        {/* 탭 5: 상품 이미지 (11번 항목 - 요청한 디자인 참고) */}
                        {activeTab === 'images' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-left-2 duration-300">
                                <div className="flex justify-between items-center border-b pb-4">
                                    <h3 className="text-xl font-bold">상품 이미지 업로드</h3>
                                    <button className="text-sm font-bold text-blue-600 hover:text-blue-700">초기화</button>
                                </div>

                                {/* 등록된 이미지 그리드 디자인 */}

                                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                    {/* key={i}를 추가하여 리액트가 각 항목을 식별할 수 있게 합니다. */}
                                    {[0, 1, 2].map((i) => (
                                        <ImagePreview key={i} id={i} imgUrl={tempImages[i]} />
                                    ))}
                                </div>

                                {/* 드롭존 영역 */}
                                <div className="border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-lg p-12 flex flex-col items-center justify-center bg-slate-50/50 dark:bg-slate-900/30 hover:bg-slate-50 transition-colors cursor-pointer group">
                                    <div className="w-12 h-12 bg-white dark:bg-slate-800 rounded-full flex items-center justify-center shadow-sm border border-slate-100 dark:border-slate-700 mb-4 group-hover:scale-110 transition-transform">
                                        <Upload size={20} className="text-blue-600" />
                                    </div>
                                    <p className="text-sm font-bold text-slate-600 dark:text-slate-400">클릭하여 이미지 추가</p>
                                    <p className="text-xs text-slate-400 mt-1">파일 당 최대 10MB (JPG, PNG)</p>
                                </div>
                            </div>
                        )}

                    </div>
                </main>
            </div>
        </div>
    );
}


// 공통 컴포넌트 영역
const Input = ({ label, onChange, ...props }: any) => (
    <div className="space-y-2">
        <label className="text-xs font-bold text-slate-500 uppercase tracking-tight">
            {label}
        </label>
        <input
            {...props}
            onChange={onChange} // 부모로부터 받은 onChange를 명시적으로 전달
            className="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500 transition-all"
        />
    </div>
);

const Select = ({ label, options }: any) => (
    <div className="space-y-2">
        <label className="text-xs font-bold text-slate-500 uppercase tracking-tight">{label}</label>
        <select className="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg text-sm outline-none focus:ring-2 focus:ring-blue-500/10 focus:border-blue-500 transition-all appearance-none cursor-pointer">
            {options.map((o: string) => <option key={o}>{o}</option>)}
        </select>
    </div>
);

const Counter = ({ label, unit }: any) => (
    <div className="space-y-2">
        <label className="text-xs font-bold text-slate-500 uppercase tracking-tight">{label}</label>
        <div className="flex items-center justify-between px-3 py-2 bg-slate-50 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800">
            <button className="w-8 h-8 flex items-center justify-center rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm text-slate-400 hover:text-blue-600">-</button>
            <span className="text-sm font-bold text-slate-700 dark:text-slate-200">0 <span className="text-[10px] text-slate-400 font-normal">{unit}</span></span>
            <button className="w-8 h-8 flex items-center justify-center rounded bg-blue-600 text-white shadow-sm hover:bg-blue-700">+</button>
        </div>
    </div>
);

interface ImagePreviewProps {
    id: number;
    imgUrl: string;
    onRemove?: (id: number) => void; // 삭제 로직을 위한 props 추가 (선택사항)
}

const ImagePreview = ({ id, imgUrl, onRemove }: ImagePreviewProps) => {
    // 중괄호를 사용했으므로 return이 반드시 필요합니다.
    return (
        <div className="group relative aspect-square bg-slate-100 dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 overflow-hidden">
            {imgUrl ? (
                <img
                    src={imgUrl}
                    alt={`Product ${id}`}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
            ) : (
                <div className="w-full h-full flex items-center justify-center text-slate-300">
                    <ImageIcon size={24} /> {/* 이미지 없을 때 플레이스홀더 */}
                </div>
            )}

            <button
                onClick={() => onRemove?.(id)}
                className="absolute top-2 right-2 p-1 bg-white/90 dark:bg-slate-800/90 rounded shadow-sm text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
            >
                <X size={14} />
            </button>
        </div>
    );
};