"use client"
import React from 'react';
import { useRouter } from 'next/navigation';
import { ChevronRight } from 'lucide-react';

// 1. 개별 행 Props 인터페이스
interface TransactionRowProps {
    name: string;
    type: string;
    amount: string;
    date: string;
    viewId: number;
}

// 2. 개별 행 컴포넌트
const TransactionRow = ({ name, type, amount, date, viewId }: TransactionRowProps) => {
    const router = useRouter();

    const getTypeStyle = (type: string) => {
        switch (type) {
            case '입고': return 'bg-blue-50 text-blue-600';
            case '출고': return 'bg-orange-50 text-orange-600';
            case '주문완료': return 'bg-green-50 text-green-600';
            default: return 'bg-gray-100 text-gray-600';
        }
    };

    return (
        // tr에 직접 onClick을 걸어 문법 오류를 방지합니다.
        <tr
            onClick={() => router.push(`/transactions?view=${viewId}`)}
            className="group hover:bg-gray-50/80 transition-colors cursor-pointer"
        >
            <td className="px-6 py-4 font-semibold text-gray-800 text-sm">{name}</td>
            <td className="px-6 py-4">
                <span className={`px-2 py-1 rounded text-[11px] font-bold ${getTypeStyle(type)}`}>
                    {type}
                </span>
            </td>
            <td className={`px-6 py-4 font-bold text-sm ${amount.startsWith('+') ? 'text-blue-500' : 'text-gray-700'}`}>
                {amount}
            </td>
            <td className="px-6 py-4 text-xs text-gray-400 font-medium">{date}</td>
            <td className="px-6 py-4 text-right">
                <div className="inline-flex items-center justify-center w-8 h-8 rounded-full group-hover:bg-white group-hover:shadow-sm transition-all">
                    <ChevronRight size={16} className="text-gray-300 group-hover:text-blue-500" />
                </div>
            </td>
        </tr>
    );
};

// 3. 메인 테이블 컴포넌트
const DashTransactionTable = () => {
    return (
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            {/* 헤더 영역 */}
            <div className="p-6 border-b border-gray-50 flex justify-between items-center">
                <h3 className="text-lg font-bold text-gray-800">최근 재고 트랜잭션</h3>
                <button className="text-sm text-green-600 font-bold hover:underline transition-all">
                    전체보기
                </button>
            </div>

            {/* 테이블 영역 */}
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                    <thead className="bg-gray-50/50 text-gray-400 uppercase tracking-wider">
                        <tr>
                            <th className="px-6 py-4 font-bold text-[11px]">상품명</th>
                            <th className="px-6 py-4 font-bold text-[11px]">변동 유형</th>
                            <th className="px-6 py-4 font-bold text-[11px]">수량</th>
                            <th className="px-6 py-4 font-bold text-[11px]">일시</th>
                            <th className="px-6 py-4 w-16"></th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-50">
                        <TransactionRow
                            name="나이키 에어맥스"
                            type="입고"
                            amount="+50"
                            date="2024-05-22 14:00"
                            viewId={1001}
                        />
                        <TransactionRow
                            name="삼성 갤럭시 S24"
                            type="출고"
                            amount="-2"
                            date="2024-05-22 13:45"
                            viewId={1002}
                        />
                        <TransactionRow
                            name="애플 맥북 프로"
                            type="주문완료"
                            amount="-1"
                            date="2024-05-22 12:30"
                            viewId={1003}
                        />
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DashTransactionTable;