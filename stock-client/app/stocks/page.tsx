// app/stocks/page.tsx
import React from 'react';
import Link from 'next/link';
import { Search, Upload, Plus } from 'lucide-react';
import StockTile, { StockTileInfo } from "./_components/StockTile"

export default function StockSearchPage() {
  // 샘플 데이터
  let idx = 1;
  const products: StockTileInfo[] = [
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800', brand: 'APPLE', name: '애플 워치 시리즈 8 GPS 41mm 스타라이트 알루미늄 케이스', tag: 'LOW STOCK', lastUpdated: '2024-05-20 14:30', transactionType: '출고', changeAmount: -2 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800', brand: 'SONY', name: '소니 WH-1000XM5 노이즈 캔슬링 블루투스 헤드셋', tag: 'IN STOCK', lastUpdated: '2024-05-19 18:00', transactionType: '등록', changeAmount: 0 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800', brand: 'FOSSIL', name: '파실 남성용 젠 6 터치스크린 스마트워치 건메탈', tag: 'OUT OF STOCK', lastUpdated: '2024-05-18 11:20', transactionType: '출고', changeAmount: -1 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800', brand: 'APPLE', name: '애플 워치 시리즈 8 GPS 41mm 스타라이트 알루미늄 케이스', tag: 'LOW STOCK', lastUpdated: '2024-05-20 14:30', transactionType: '출고', changeAmount: -2 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800', brand: 'SONY', name: '소니 WH-1000XM5 노이즈 캔슬링 블루투스 헤드셋', tag: 'IN STOCK', lastUpdated: '2024-05-19 18:00', transactionType: '등록', changeAmount: 0 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800', brand: 'FOSSIL', name: '파실 남성용 젠 6 터치스크린 스마트워치 건메탈', tag: 'OUT OF STOCK', lastUpdated: '2024-05-18 11:20', transactionType: '출고', changeAmount: -1 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800', brand: 'APPLE', name: '애플 워치 시리즈 8 GPS 41mm 스타라이트 알루미늄 케이스', tag: 'LOW STOCK', lastUpdated: '2024-05-20 14:30', transactionType: '출고', changeAmount: -2 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800', brand: 'SONY', name: '소니 WH-1000XM5 노이즈 캔슬링 블루투스 헤드셋', tag: 'IN STOCK', lastUpdated: '2024-05-19 18:00', transactionType: '등록', changeAmount: 0 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800', brand: 'FOSSIL', name: '파실 남성용 젠 6 터치스크린 스마트워치 건메탈', tag: 'OUT OF STOCK', lastUpdated: '2024-05-18 11:20', transactionType: '출고', changeAmount: -1 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800', brand: 'APPLE', name: '애플 워치 시리즈 8 GPS 41mm 스타라이트 알루미늄 케이스', tag: 'LOW STOCK', lastUpdated: '2024-05-20 14:30', transactionType: '출고', changeAmount: -2 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800', brand: 'SONY', name: '소니 WH-1000XM5 노이즈 캔슬링 블루투스 헤드셋', tag: 'IN STOCK', lastUpdated: '2024-05-19 18:00', transactionType: '등록', changeAmount: 0 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800', brand: 'FOSSIL', name: '파실 남성용 젠 6 터치스크린 스마트워치 건메탈', tag: 'OUT OF STOCK', lastUpdated: '2024-05-18 11:20', transactionType: '출고', changeAmount: -1 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=800', brand: 'APPLE', name: '애플 워치 시리즈 8 GPS 41mm 스타라이트 알루미늄 케이스', tag: 'LOW STOCK', lastUpdated: '2024-05-20 14:30', transactionType: '출고', changeAmount: -2 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800', brand: 'SONY', name: '소니 WH-1000XM5 노이즈 캔슬링 블루투스 헤드셋', tag: 'IN STOCK', lastUpdated: '2024-05-19 18:00', transactionType: '등록', changeAmount: 0 },
    { id: (idx++).toString(), image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800', brand: 'FOSSIL', name: '파실 남성용 젠 6 터치스크린 스마트워치 건메탈', tag: 'OUT OF STOCK', lastUpdated: '2024-05-18 11:20', transactionType: '출고', changeAmount: -1 },

  ];
  const tags: String[] = ['전체', 'HOT', '웨어러블', '가전/디지털', '액세서리'];

  return (
    // min-h-screen을 사용하여 컨텐츠가 적어도 화면 전체 높이를 차지하게 하고, 
    // bg 컬러가 끊기지 않도록 합니다.
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 pb-20 overflow-y-auto">
      <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 sticky top-0 z-20 shadow-sm">
        <div className="max-w-7xl mx-auto px-2 py-2 md:py-4">
          <div className="flex flex-col items-center gap-6">
            <div className="relative w-full max-w-full">
              <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none text-blue-600">
                <Search size={20} strokeWidth={2.5} />
              </div>
              <input
                type="text"
                placeholder="조회할 상품명 또는 브랜드명을 입력하세요"
                className="w-full pl-14 pr-28 py-4 bg-white dark:bg-slate-800 border-2 border-blue-600 rounded-full text-base focus:outline-none shadow-lg shadow-blue-500/10 focus:ring-4 focus:ring-blue-500/5 transition-all"
              />
              <button className="absolute right-2 top-2 bottom-2 px-6 bg-blue-600 text-white rounded-full text-sm font-bold hover:bg-blue-700 transition-colors shadow-md">
                검색
              </button>
            </div>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-6 mt-6">
        <div className="flex gap-2 overflow-x-auto pb-1 w-full justify-start md:justify-center scrollbar-hide mb-6">
          {tags.map((cat, i) => (
            <button
              key={i}
              className={`px-5 py-2 rounded-full text-xs font-bold whitespace-nowrap border transition-all ${i === 0
                ? 'bg-slate-900 text-white border-slate-900 dark:bg-blue-600 dark:border-blue-600'
                : 'bg-white text-slate-500 border-slate-200 hover:border-blue-600 hover:text-blue-600 dark:bg-slate-800 dark:border-slate-700'
                }`}
            >
              {cat}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {products.map((product, index) => (
            <Link
              key={`${product.id}-${index}`}
              href={`/stocks/${product.id}`}
              className="block" // Link가 전체 영역을 차지하도록 설정
            >
              <StockTile product={product} />
            </Link>
          ))}
        </div>

        <div className="h-20" />
      </main>

      <div className="fixed bottom-8 right-8 flex flex-col gap-3 z-30">
        <button className="w-12 h-12 bg-white dark:bg-slate-800 shadow-2xl border border-slate-200 dark:border-slate-700 rounded-full flex items-center justify-center text-slate-600 hover:text-blue-600 hover:scale-110 transition-all">
          <Upload size={20} />
        </button>

        <Link
          key={`go-create`}
          href={`/stocks/new`}
        >
          <button className="w-12 h-12 bg-blue-600 shadow-xl shadow-blue-500/40 rounded-full flex items-center justify-center text-white hover:scale-110 active:scale-95 transition-all">
            <Plus size={24} />
          </button>
        </Link>
      </div>
    </div>
  );
}
