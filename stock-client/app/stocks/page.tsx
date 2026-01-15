// app/stocks/page.tsx
import { StockHeader } from './_components/StockHeader';
import { StockFilters } from './_components/StockFilters';
import { StockGrid } from './_components/StockGrid';

export default function StocksPage() {
  return (
    <div className="flex-1 overflow-y-auto">
      {/* Transaction 페이지와 동일한 max-w 컨테이너 적용 */}
      <div className="max-w-[1600px] mx-auto">
        <StockHeader />
        <StockFilters />
        <StockGrid />
      </div>
    </div>
  );
}