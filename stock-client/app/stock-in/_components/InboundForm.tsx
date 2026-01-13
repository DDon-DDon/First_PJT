"use client";

import { useState } from 'react';
import { PlusIcon, MinusIcon, PackageSearch, ArrowRight } from 'lucide-react';

interface InboundFormProps {
  productId?: string; // URL의 ?view=1234 값을 전달받음
}

export default function InboundForm({ productId }: InboundFormProps) {
  const [quantity, setQuantity] = useState(1);

  const handleDecrease = () => {
    if (quantity > 1) setQuantity(prev => prev - 1);
  };

  const handleIncrease = () => {
    setQuantity(prev => prev + 1);
  };

  // 1. view(productId)가 없는 경우: 루트 상태의 안내 UI (Empty State)
  if (!productId) {
    return (
      <div className="mb-12 flex flex-col items-center justify-center p-16 border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-3xl bg-white/30 dark:bg-slate-900/30 backdrop-blur-sm animate-in fade-in zoom-in-95 duration-500">
        <div className="w-20 h-20 bg-blue-50 dark:bg-blue-900/20 rounded-2xl flex items-center justify-center mb-6 text-blue-600 dark:text-blue-400">
          <PackageSearch size={40} />
        </div>
        <h3 className="text-2xl font-bold text-slate-900 dark:text-white mb-3">입고 대상이 선택되지 않았습니다</h3>
        <p className="text-slate-500 dark:text-slate-400 text-center max-w-md mb-8 leading-relaxed">
          새로운 재고를 등록하거나 수량을 보정하려면 아래 히스토리 목록에서 제품을 선택해 주세요.
        </p>
        <div className="flex items-center gap-2 text-blue-600 font-semibold text-sm animate-bounce-x">
          히스토리에서 제품 선택하기 <ArrowRight size={16} />
        </div>
      </div>
    );
  }

  // 2. view(productId)가 있는 경우: 기존 입력 폼 UI
  return (
    <div className="grid grid-cols-12 gap-8 mb-12 items-stretch animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Left: Product Preview Section */}
      <div className="col-span-12 lg:col-span-5 flex flex-col gap-6">
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm relative h-96">
          <img
            src={"https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800&q=80"}
            alt="Product Preview"
            className="w-full h-full object-cover grayscale opacity-90 dark:opacity-80"
          />
          {/* 제품 ID 태그 표시 (테스트용) */}
          <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-md text-white text-xs px-3 py-1.5 rounded-full font-mono">
            ID: {productId}
          </div>
        </div>
        <div className="flex flex-col flex-1 justify-between px-1">
          <div className="space-y-3">
            <h3 className="text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
              Product Name
            </h3>
            <p className="text-slate-500 dark:text-slate-400 text-base leading-relaxed border-l-2 border-slate-200 dark:border-slate-700 pl-4">
              Detailed product description goes here. This section can now accommodate 
              longer sentences to provide more context about the item.
            </p>
          </div>
          <button className="mt-6 w-full py-4 border-2 border-blue-600 text-blue-600 font-bold rounded-xl hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors">
            See Detail
          </button>
        </div>
      </div>

      {/* Right: Input Form Section */}
      <div className="col-span-12 lg:col-span-7">
        <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm h-full flex flex-col">
          <div className="flex items-center justify-between mb-8">
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">Inbound Item</h3>
            <div className="flex gap-2">
              <span className="bg-sky-100 dark:bg-sky-900/30 text-sky-600 dark:text-sky-400 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Stable</span>
              <span className="bg-rose-100 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Popular</span>
            </div>
          </div>

          <form className="space-y-6 flex-1 flex flex-col">
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-2">
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">Quantity Add</label>
                <div className="flex items-center h-12 w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-blue-500 transition-all">
                  <button 
                    type="button"
                    onClick={handleDecrease}
                    className="h-full aspect-square flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 transition-colors border-r border-slate-200 dark:border-slate-700"
                  >
                    <MinusIcon size={18} strokeWidth={2.5} />
                  </button>
                  <div className="flex-1 h-full flex items-center justify-center bg-white dark:bg-slate-900">
                    <span className="font-bold text-lg text-slate-900 dark:text-white">{quantity}</span>
                  </div>
                  <button 
                    type="button"
                    onClick={handleIncrease}
                    className="h-full aspect-square flex items-center justify-center hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-400 transition-colors border-l border-slate-200 dark:border-slate-700"
                  >
                    <PlusIcon size={18} strokeWidth={2.5} />
                  </button>
                </div>
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">Product Type</label>
                <select className="w-full h-12 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-blue-500 outline-none">
                  <option>None</option>
                  <option>Hardware</option>
                  <option>Software</option>
                  <option>Consumable</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">
                Reference / PO Number / Order Number <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                className="w-full h-12 bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700 rounded-lg px-4 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-blue-500 outline-none"
                placeholder="Enter reference number"
              />
            </div>

            <div className="space-y-2 flex-1 flex flex-col">
              <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300">Description</label>
              <textarea
                className="w-full flex-1 min-h-[160px] bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-4 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
                placeholder="Enter detailed description here..."
              ></textarea>
            </div>

            <div className="pt-4 mt-auto">
              <button type="submit" className="w-full h-14 bg-blue-600 text-white text-lg font-bold rounded-xl hover:bg-blue-700 transition-shadow shadow-lg shadow-blue-500/20">
                Confirm Inbound
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}