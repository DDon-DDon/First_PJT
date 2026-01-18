// AuditInquiryDialog.tsx
"use client"

import React, { useState } from 'react';
import { Search, X, Plus } from 'lucide-react';

// Props 타입 정의
export interface AuditInquiryDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onAddItem: (item: any) => void;
  mockDB: any[]; // 실제 환경에서는 API 데이터 타입으로 대체
}

const AuditInquiryDialog = ({ isOpen, onClose, onAddItem, mockDB }: AuditInquiryDialogProps) => {
  const [searchTerm, setSearchTerm] = useState('');

  // 모달이 닫혀있으면 아무것도 렌더링하지 않음
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl overflow-hidden">
        <div className="p-4 border-b border-gray-100 flex justify-between items-center bg-[#f9fafb]">
          <h2 className="font-bold text-lg text-gray-800">조정 상품 선택</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X size={24} />
          </button>
        </div>

        <div className="p-4 mb-4">
          <div className="relative mb-4">
            <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
            <input
              type="text"
              placeholder="품명 또는 SKU 코드로 검색"
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md outline-none focus:ring-1 focus:ring-[#00c73c]"
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="max-h-80 overflow-y-auto border border-gray-100 rounded-md">
            <table className="w-full text-sm text-left">
              <thead className="bg-gray-50 text-gray-500 sticky top-0">
                <tr>
                  <th className="px-4 py-2">상품정보</th>
                  <th className="px-4 py-2">현재고</th>
                  <th className="px-4 py-2 w-20 text-center">선택</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {mockDB
                  .filter(dbItem => 
                    dbItem.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                    dbItem.sku.toLowerCase().includes(searchTerm.toLowerCase())
                  )
                  .map((dbItem) => (
                    <tr key={dbItem.id} className="hover:bg-green-50/50 transition-colors">
                      <td className="px-4 py-3">
                        <div className="font-bold text-gray-700">{dbItem.name}</div>
                        <div className="text-xs text-gray-400 font-mono">{dbItem.sku} | {dbItem.category}</div>
                      </td>
                      <td className="px-4 py-3 text-gray-600 font-medium">{dbItem.currentStock}</td>
                      <td className="px-4 py-3 text-center">
                        <button
                          onClick={() => onAddItem(dbItem)}
                          className="p-1 rounded-full border border-gray-200 text-gray-400 hover:bg-[#00c73c] hover:text-white hover:border-[#00c73c] transition-all"
                        >
                          <Plus size={16} />
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* <div className="p-4 bg-gray-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-[#202022] text-white rounded font-bold text-sm"
          >
            닫기
          </button>
        </div> */}
      </div>
    </div>
  );
};

export default AuditInquiryDialog;