import PageHeader from '../layout/PageHeader';
import { Plus } from 'lucide-react';

export default function MainHeader() {
  return (
      <PageHeader
        title="Inventory Overview"
        actions={
          <button className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-semibold bg-blue-600">
            <Plus size={18} />
            Create Order
          </button>
        }
      />
  );
}
