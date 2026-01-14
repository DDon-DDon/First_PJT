'use client';

import React, { useState } from 'react';
import {
    PlusIcon,
    MinusIcon,
    Calendar,
    User,
    CheckCircle2,
    ArrowRight,
    Archive,
    ExternalLink,
    ChevronDown,
    X
} from 'lucide-react';

import ImagePreviewDialog from '../../components/ImagePreviewDialog';

interface StockTransactionsProps {
    productId?: string; // URL의 ?view=1234 값을 전달받음
}

const imgUrl = 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80';

// StockTransactions
export default function TransactionDetail({ productId }: StockTransactionsProps) {
    const [quantity, setQuantity] = useState(50);
    const [openPreview, setOpenPreview] = useState(false);
    const currentStock = 240;
    const handleIncrease = () => setQuantity(prev => prev + 1);
    const handleDecrease = () => setQuantity(prev => (prev > 0 ? prev - 1 : 0));

    return (
        <div className="space-y-8">

            {/* Page Heading */}
            <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 dark:text-white tracking-tight">
                        Stock transaction history
                    </h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">
                        Log incoming shipments or outgoing dispatch items accurately.
                    </p>
                </div>
            </div>

            {/* Main Transaction Card */}
            <div className="bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 overflow-hidden">

                {/* Segmented Control */}
                <div className="border-b border-slate-200 dark:border-slate-800 p-6 pb-0 bg-slate-50/50 dark:bg-slate-800/50">
                    <div className="flex justify-center md:justify-start">
                        <div className="inline-flex rounded-lg bg-slate-200 dark:bg-slate-700 p-1 mb-6">
                            <label className="relative flex items-center justify-center px-6 py-2.5 cursor-pointer select-none rounded-md transition-all group">
                                <input defaultChecked className="peer sr-only" name="transaction_type" type="radio" value="in" />
                                <div className="absolute inset-0 bg-white dark:bg-slate-600 shadow-sm rounded-md opacity-0 peer-checked:opacity-100 transition-opacity"></div>
                                <span className="relative flex items-center gap-2 z-10 text-sm font-semibold text-slate-600 dark:text-slate-300 peer-checked:text-primary dark:peer-checked:text-white">
                                    <Archive size={18} />
                                    Stock In (Receiving)
                                </span>
                            </label>
                            <label className="relative flex items-center justify-center px-6 py-2.5 cursor-pointer select-none rounded-md transition-all group">
                                <input className="peer sr-only" name="transaction_type" type="radio" value="out" />
                                <div className="absolute inset-0 bg-white dark:bg-slate-600 shadow-sm rounded-md opacity-0 peer-checked:opacity-100 transition-opacity"></div>
                                <span className="relative flex items-center gap-2 z-10 text-sm font-semibold text-slate-600 dark:text-slate-300 peer-checked:text-orange-600 dark:peer-checked:text-orange-400">
                                    <ExternalLink size={18} />
                                    Stock Out (Dispatching)
                                </span>
                            </label>
                        </div>
                    </div>
                </div>

                <form className="p-6 md:p-8 grid grid-cols-1 md:grid-cols-12 gap-8">
                    {/* Left Column */}
                    <div className="md:col-span-8 space-y-8">
                        <div className="space-y-2">
                            <div className="flex items-center justify-between gap-4">
                                <h2 className="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">
                                    Information
                                </h2>
                            </div>

                            {/* Preview Box */}
                            <div className="mt-4 p-4 bg-blue-50/50 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-900/30 rounded-xl flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div
                                        className="h-12 w-12 bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center cursor-pointer hover:shadow-md transition"
                                        onClick={() => setOpenPreview(true)}
                                    >
                                        <img
                                            src="https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80"
                                            alt="Product Preview"
                                            className="w-full h-full object-cover grayscale opacity-90 dark:opacity-80"
                                        />
                                    </div>
                                    <div>
                                        <p className="text-sm font-bold text-slate-900 dark:text-white">Wireless Mouse M30</p>
                                        <p className="text-xs text-slate-500 dark:text-slate-400 font-mono">WM-302-BLK</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <span className="block text-[10px] text-slate-500 dark:text-slate-400 font-bold uppercase tracking-wider">On Hand</span>
                                    <span className="block text-xl font-black text-slate-900 dark:text-white">{currentStock}</span>
                                </div>
                            </div>
                        </div>

                        {/* Quantity & Reason Area */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 ml-1">Quantity</label>
                                <div className="flex items-center h-[56px] w-full bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-xl overflow-hidden focus-within:ring-2 focus-within:ring-primary transition-all">
                                    <button
                                        type="button"
                                        onClick={handleDecrease}
                                        className="h-full px-4 flex items-center justify-center hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 transition-colors border-r border-slate-200 dark:border-slate-800"
                                    >
                                        <MinusIcon size={20} strokeWidth={2.5} />
                                    </button>
                                    <div className="flex-1 h-full flex items-center justify-center font-bold text-xl text-slate-900 dark:text-white">
                                        {quantity}
                                    </div>
                                    <button
                                        type="button"
                                        onClick={handleIncrease}
                                        className="h-full px-4 flex items-center justify-center hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 transition-colors border-l border-slate-200 dark:border-slate-800"
                                    >
                                        <PlusIcon size={20} strokeWidth={2.5} />
                                    </button>
                                </div>
                                <p className="text-xs text-slate-500 dark:text-slate-400 mt-2 flex items-center gap-1.5 ml-1 font-medium">
                                    <ArrowRight size={14} className="text-primary" />
                                    Projected: <span className="text-slate-900 dark:text-white font-bold">{currentStock + quantity}</span>
                                </p>
                            </div>

                            {/* [M3 수정] Reason / Reference */}
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 ml-1">Reason / Reference</label>
                                <div className="space-y-2">
                                    <div className="relative">
                                        <select className="appearance-none block w-full h-[56px] px-4 rounded-xl border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary shadow-sm sm:text-sm">
                                            <option>Purchase Order (PO)</option>
                                            <option>Return from Customer</option>
                                            <option>Inventory Adjustment</option>
                                            <option>Other</option>
                                        </select>
                                        <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" size={18} />
                                    </div>
                                    <input
                                        className="block w-full h-[56px] px-4 rounded-xl border-slate-300 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary shadow-sm sm:text-sm"
                                        placeholder="Reference Number (e.g. PO-123)"
                                        type="text"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Right Column: Meta Details */}
                    {/* [M3 수정] 오른쪽 패널의 필드들을 Material 3 규격 높이(56px)로 일원화 */}
                    <div className="md:col-span-4 bg-slate-50 dark:bg-slate-800/40 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 flex flex-col">
                        <div className="space-y-6 flex-1">
                            {/* Transaction Date */}
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 ml-1">Transaction Date</label>
                                <div className="relative">
                                    <Calendar size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                                    <input
                                        className="block w-full h-[56px] pl-11 pr-4 rounded-xl border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary shadow-sm"
                                        type="date"
                                        defaultValue={new Date().toISOString().split('T')[0]}
                                    />
                                </div>
                            </div>

                            {/* Responsible Person */}
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 ml-1">Responsible Person</label>
                                <div className="relative">
                                    <User size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                                    <select className="appearance-none block w-full h-[56px] pl-11 pr-10 rounded-xl border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary shadow-sm">
                                        <option>Alex Morgan</option>
                                        <option>Sarah Connor</option>
                                        <option>John Doe</option>
                                    </select>
                                    <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" size={18} />
                                </div>
                            </div>

                            {/* Notes */}
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 ml-1">Notes</label>
                                <textarea
                                    rows={4}
                                    className="block w-full p-4 rounded-xl border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary shadow-sm resize-none"
                                    placeholder="Provide additional context here..."
                                ></textarea>
                            </div>
                        </div>

                        <div className="pt-6 mt-6 border-t border-slate-200 dark:border-slate-700 flex gap-3">
                            <button className="flex-1 cursor-pointer bg-blue-600 hover:bg-blue-800 transition-colors  text-white font-semibold py-2.5 px-4 rounded-md shadow-sm flex items-center justify-center gap-2" type="submit">
                                <CheckCircle2 size={18} />
                                Confirm
                            </button>
                            <button className="px-4 py-2.5 cursor-pointer bg-white hover:bg-gray-50 transition-colors dark:bg-slate-800 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 font-semibold rounded-md hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors" type="button">
                                Cancel
                            </button>
                        </div>
                    </div>
                </form>
            </div>
            {openPreview && (
                <ImagePreviewDialog
                    imgUrl={imgUrl}
                    isOpen={openPreview}
                    onClose={() => setOpenPreview(false)}
                />
            )}
        </div>
    )
}