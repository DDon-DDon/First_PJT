'use client';
import React, { useState } from 'react';
import { PackageSearch, Save, Upload, Plus, Search, X, Check } from 'lucide-react';
import AuditInquiryDialog, { AuditInquiryDialogProps } from './_components/AuditInquiryDialog';

interface InventoryItem {
    id: string;
    category: string;
    sku: string;
    name: string;
    unit: string;
    currentStock: number;
    adjustment: number;
    finalStock: number;
    remark: string;
}

const InventoryAuditPage = () => {
    // 1. 현재 테이블에 올라와 있는 조정 대상 리스트
    const [items, setItems] = useState<InventoryItem[]>([]);
    // 2. 다이얼로그(모달) 오픈 상태
    const [isModalOpen, setIsModalOpen] = useState(false);
    // 3. 모달 내 검색어
    const [searchTerm, setSearchTerm] = useState('');

    // [가상 DB 데이터] 실제로는 API를 통해 불러오게 됩니다.
    const mockDB: InventoryItem[] = [
        { id: '1', category: '필기구', sku: 'ABC-123-DEF', name: '프리미엄 연필', unit: '12자루(1다스)', currentStock: 100, adjustment: 0, finalStock: 100, remark: '' },
        { id: '2', category: '사무용품', sku: 'GHI-456-JKL', name: 'A4 복사용지', unit: '500매(1박스)', currentStock: 50, adjustment: 0, finalStock: 50, remark: '' },
        { id: '3', category: '전자기기', sku: 'MNO-789-PQR', name: '무선 마우스', unit: '1개', currentStock: 30, adjustment: 0, finalStock: 30, remark: '' },
    ];

    // 조정 대상 리스트에 상품 추가
    const addItemToAudit = (item: InventoryItem) => {
        if (items.find((i) => i.id === item.id)) {
            alert('이미 리스트에 포함된 상품입니다.');
            return;
        }
        setItems([...items, item]);
    };

    // 리스트에서 제외
    const removeItem = (id: string) => {
        setItems(items.filter((item) => item.id !== id));
    };

    const handleAdjustmentChange = (id: string, value: number) => {
        setItems(items.map(item =>
            item.id === id ? { ...item, adjustment: value, finalStock: item.currentStock + value } : item
        ));
    };

    const handleFinalStockChange = (id: string, value: number) => {
        setItems(items.map(item =>
            item.id === id ? { ...item, finalStock: value, adjustment: value - item.currentStock } : item
        ));
    };

    return (
        <main className="flex-1 p-8 bg-[#f0f2f5] min-h-screen">
            <header className="flex justify-between items-end mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-[#202022]">재고 조정 (Audit)</h1>
                    <p className="text-sm text-gray-500 mt-1">실사 후 차이가 발생하는 품목을 추가하여 보정합니다.</p>
                </div>
                <div className="flex gap-2">
                    {/* 상품 불러오기 버튼 강조 */}
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="flex items-center gap-1 px-4 py-2 bg-white border border-[#00c73c] text-[#00c73c] rounded text-sm font-bold hover:bg-[#f0fff4] transition-colors"
                    >
                        <Plus size={16} /> 조정 상품 불러오기
                    </button>
                    <button className="flex items-center gap-1 px-3 py-2 border border-gray-300 rounded text-sm bg-white hover:bg-gray-50 text-gray-600 font-medium">
                        <Upload size={16} /> 엑셀 업로드
                    </button>
                    <button className="flex items-center gap-1 px-4 py-2 bg-[#00c73c] text-white rounded text-sm font-bold hover:bg-[#00ab34] shadow-sm">
                        <Save size={16} /> 조정 내용 저장
                    </button>
                </div>
            </header>

            {/* 테이블 카드 영역 */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                {items.length > 0 ? (
                    <table className="w-full text-sm text-left">
                        <thead className="bg-[#f9fafb] border-b border-gray-200 text-gray-600 font-semibold">
                            <tr>
                                <th className="px-4 py-3">분류</th>
                                <th className="px-4 py-3">제품 코드 (SKU)</th>
                                <th className="px-4 py-3">품명</th>
                                <th className="px-4 py-3 text-center">단위</th>
                                <th className="px-4 py-3 text-right">현재고</th>
                                <th className="px-4 py-3 w-28 text-center text-[#00c73c]">조정 수량</th>
                                <th className="px-4 py-3 w-28 text-center text-blue-600">조정 후 재고</th>
                                <th className="px-4 py-3">비고</th>
                                <th className="px-4 py-3 w-10"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-100">
                            {items.map((item) => (
                                <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                                    <td className="px-4 py-4 text-gray-500">{item.category}</td>
                                    <td className="px-4 py-4 font-mono font-medium text-xs text-gray-400">{item.sku}</td>
                                    <td className="px-4 py-4 font-semibold text-gray-800">{item.name}</td>
                                    <td className="px-4 py-4 text-center text-gray-500">{item.unit}</td>
                                    <td className="px-4 py-4 text-right font-bold text-gray-700">{item.currentStock}</td>
                                    <td className="px-4 py-4">
                                        <input
                                            type="number"
                                            value={item.adjustment}
                                            onChange={(e) => handleAdjustmentChange(item.id, Number(e.target.value))}
                                            className="w-full border border-gray-300 rounded px-2 py-1 text-center focus:ring-1 focus:ring-[#00c73c] outline-none"
                                        />
                                    </td>
                                    <td className="px-4 py-4">
                                        <input
                                            type="number"
                                            value={item.finalStock}
                                            onChange={(e) => handleFinalStockChange(item.id, Number(e.target.value))}
                                            className="w-full border border-blue-200 bg-blue-50 rounded px-2 py-1 text-center font-bold text-blue-700 focus:ring-1 focus:ring-blue-500 outline-none"
                                        />
                                    </td>
                                    <td className="px-4 py-4">
                                        <input
                                            type="text"
                                            placeholder="사유 입력"
                                            className="w-full border-b border-transparent hover:border-gray-300 focus:border-[#00c73c] outline-none bg-transparent py-1 transition-all"
                                        />
                                    </td>
                                    <td className="px-4 py-4">
                                        <button onClick={() => removeItem(item.id)} className="text-gray-300 hover:text-red-500">
                                            <X size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <div className="flex flex-col items-center py-20 text-gray-400">
                        <PackageSearch size={48} className="mb-2 opacity-20" />
                        <p>조정할 상품을 상단 버튼을 통해 불러와주세요.</p>
                    </div>
                )}
            </div>

            {/* 상품 조회 다이얼로그 (모달) */}
            {isModalOpen && (
                <AuditInquiryDialog
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    onAddItem={addItemToAudit}
                    mockDB={mockDB}
                />
            )}
        </main>
    );
};

export default InventoryAuditPage;