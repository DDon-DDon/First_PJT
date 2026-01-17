// StockViewCard
import { ArrowUpRight, ArrowDownRight, Clock, MoreVertical } from 'lucide-react';

// 상품 데이터 타입 정의
export interface StockTileInfo {
  id: string;
  image: string;
  brand: string;
  name: string;
  tag: 'HOT' | 'LOW STOCK' | 'IN STOCK' | 'OUT OF STOCK';
  lastUpdated: string;
  transactionType: '입고' | '출고' | '등록';
  changeAmount: number;
}


const StockTile = ({ product }: { product: StockTileInfo }) => {
  // 태그별 스타일 지정
  const tagStyles = {
    'HOT': 'bg-red-500 text-white',
    'LOW STOCK': 'bg-amber-100 text-amber-600 border border-amber-200',
    'IN STOCK': 'bg-emerald-100 text-emerald-600 border border-emerald-200',
    'OUT OF STOCK': 'bg-slate-200 text-slate-500',
  };

  return (
    <div className="group flex flex-col bg-white dark:bg-slate-900 rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800 hover:shadow-xl transition-all duration-300">
      {/* 1. 상품 이미지 섹션 */}
      <div className="relative aspect-[4/3] overflow-hidden bg-slate-100">
        <img 
          src={product.image} 
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
        {/* 4. 상품 구분용 태그 정보 */}
        <div className="absolute top-3 left-3">
          <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold tracking-wider ${tagStyles[product.tag]}`}>
            {product.tag}
          </span>
        </div>
        {/* <button className="absolute top-3 right-3 p-1.5 bg-white/80 backdrop-blur-md rounded-full text-slate-600 hover:text-blue-600 transition-colors">
          <MoreVertical size={16} />
        </button> */}
      </div>

      {/* 정보 섹션 */}
      <div className="p-4 flex flex-col flex-1">
        {/* 2. 브랜드 / 공급사 */}
        <div className="flex items-center gap-1 mb-1">
          <span className="text-xs font-bold text-slate-400 uppercase tracking-tight">{product.brand}</span>
          {/* <span className="text-[10px] text-slate-300">|</span>
          <span className="text-[10px] text-slate-400">일반</span> */}
        </div>

        {/* 3. 상품 이름 */}
        <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-100 line-clamp-2 mb-3 h-10 leading-snug">
          {product.name}
        </h3>

        <div className="mt-auto space-y-2 pt-3 border-t border-slate-50 dark:border-slate-800">
          {/* 5. 최신 업데이트 날짜 */}
          <div className="flex items-center justify-between text-[11px] text-slate-500">
            <div className="flex items-center gap-1">
              <Clock size={12} className="text-slate-400" />
              <span>최신 업데이트</span>
            </div>
            <span className="font-medium">{product.lastUpdated}</span>
          </div>

          {/* 6. 상품 트랜잭션 이력 (증감 표시) */}
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-widest">Transaction</span>
            <div className={`flex items-center gap-1 px-2 py-1 rounded-lg font-bold text-xs ${
              product.transactionType === '입고' ? 'text-blue-600 bg-blue-50' : 
              product.transactionType === '출고' ? 'text-rose-600 bg-rose-50' : 'text-slate-600 bg-slate-100'
            }`}>
              {product.transactionType === '입고' && <ArrowUpRight size={14} />}
              {product.transactionType === '출고' && <ArrowDownRight size={14} />}
              <span>{product.transactionType} {product.changeAmount !== 0 && `${product.changeAmount > 0 ? '+' : ''}${product.changeAmount}`}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockTile;