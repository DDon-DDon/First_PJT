// components/StockGrid.tsx
import { ProductCard } from './ProductCard';

export function StockGrid() {
  // 실제 환경에선 props로 받거나 API 호출을 통해 데이터를 가져옵니다.
  const products = [
    { name: "Apple Watch Series 8", category: "Wearables", price: "$399.00", sku: "APL-W8-GPS", inventory: 3, status: "Low Stock" as const, imageUrl: "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&q=80" },
    { name: "Dell XPS 13", category: "Computers", price: "$999.00", sku: "DEL-XPS-13", inventory: 0, status: "Out of Stock" as const, imageUrl: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&q=80" },
    { name: "Sony WH-1000XM4", category: "Electronics", price: "$348.00", sku: "SNY-XM4-BLK", inventory: 45, status: "In Stock" as const, imageUrl: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&q=80" },
  ];

  return (
    <section className="px-8 pb-12 flex-1 overflow-y-auto custom-scrollbar">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products.map((product, index) => (
          <ProductCard key={index} {...product} />
        ))}
      </div>
    </section>
  );
}