// components/ProductCard.tsx
import { Package, ShoppingCart, Edit3, ExternalLink, AlertCircle } from 'lucide-react';

interface ProductProps {
  name: string;
  category: string;
  price: string;
  sku: string;
  inventory: number;
  status: 'In Stock' | 'Low Stock' | 'Out of Stock';
  imageUrl: string;
}

export function ProductCard({ name, category, price, sku, inventory, status, imageUrl }: ProductProps) {
  // 상태별 스타일 정의
  const statusConfig = {
    'In Stock': { 
      badge: 'bg-emerald-100 text-emerald-700', 
      text: 'text-emerald-600',
      icon: <Edit3 size={14} /> 
    },
    'Low Stock': { 
      badge: 'bg-amber-100 text-amber-700', 
      text: 'text-amber-600',
      icon: <ShoppingCart size={14} /> 
    },
    'Out of Stock': { 
      badge: 'bg-rose-100 text-rose-700', 
      text: 'text-rose-600',
      icon: <ExternalLink size={14} /> 
    },
  };

  const config = statusConfig[status];

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl overflow-hidden border border-slate-200 dark:border-slate-800 group hover:shadow-xl transition-all duration-300">
      {/* 이미지 섹션 */}
      <div className="relative h-48 overflow-hidden bg-slate-100 dark:bg-slate-800">
        <img 
          src={imageUrl} 
          alt={name} 
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
        />
        <span className={`absolute top-3 left-3 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider ${config.badge}`}>
          {status}
        </span>
      </div>

      {/* 정보 섹션 */}
      <div className="p-5">
        <div className="flex justify-between items-start mb-1">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{category}</span>
          <span className="text-sm font-bold text-slate-800 dark:text-white">{price}</span>
        </div>
        <h3 className="font-bold text-slate-800 dark:text-white mb-1">{name}</h3>
        <p className="text-xs text-slate-400 mb-4">SKU: {sku}</p>
        
        <div className="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-800">
          <div>
            <p className="text-[10px] font-semibold text-slate-400 uppercase">Inventory</p>
            <p className={`text-sm font-bold ${config.text}`}>{inventory} Units</p>
          </div>
          <button className="flex items-center gap-1.5 text-blue-600 dark:text-blue-400 text-xs font-bold hover:underline">
            {status === 'In Stock' ? 'Edit' : status === 'Low Stock' ? 'Restock' : 'Details'}
            {config.icon}
          </button>
        </div>
      </div>
    </div>
  );
}