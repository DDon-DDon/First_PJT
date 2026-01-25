import { X, Calendar, Hash, User, Activity, Package } from 'lucide-react';

export interface TransDetailData {
    dateTime: string;
    type: string;
    refNo: string;
    quantity: string;
    status: string;
    operator: string;
}

export interface TransDetailDialogProps {
    data: TransDetailData | null;
    isOpen: boolean;
    onClose: () => void;
}

export default function TransDetailDialog({ data, isOpen, onClose }: TransDetailDialogProps) {
    if (!isOpen || !data) return null;

    // 상태값에 따른 배지 컬러 분기
    const getStatusColor = (status: string) => {
        return status === 'Completed' 
            ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400'
            : 'bg-amber-100 text-amber-700 dark:bg-amber-500/10 dark:text-amber-400';
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <div className="absolute inset-0 bg-black/60 backdrop-blur-md" onClick={onClose} />

            {/* Dialog Card */}
            <div className="relative bg-white dark:bg-slate-900 rounded-[.5rem] shadow-xl max-w-md w-full overflow-hidden animate-in fade-in zoom-in duration-200">
                
                {/* Header */}
                <div className="flex items-center justify-between px-6 py-5 border-b border-slate-100 dark:border-slate-800">
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">Transaction Detail</h3>
                    <button onClick={onClose} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors">
                        <X className="w-5 h-5 text-slate-500" />
                    </button>
                </div>

                {/* Content Area */}
                <div className="p-6 space-y-6">
                    {/* Main Highlighting Section (Type & Status) */}
                    <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800/50 rounded-2xl">
                        <div>
                            <p className="text-xs text-slate-500 mb-1">Type</p>
                            <span className="font-bold text-slate-900 dark:text-white uppercase tracking-wider">{data.type}</span>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-xs font-bold ${getStatusColor(data.status)}`}>
                            {data.status}
                        </span>
                    </div>

                    {/* Information Grid */}
                    <div className="grid grid-cols-1 gap-5">
                        <DetailItem icon={<Calendar />} label="Date & Time" value={data.dateTime} />
                        <DetailItem icon={<Hash />} label="Reference No." value={data.refNo} />
                        <DetailItem icon={<Package />} label="Quantity" value={data.quantity} valueClass={data.quantity.startsWith('+') ? 'text-blue-600 font-bold' : 'text-red-600 font-bold'} />
                        <DetailItem icon={<User />} label="Operator" value={data.operator} />
                    </div>
                </div>

                {/* Footer Button */}
                <div className="p-6 pt-0">
                </div>
            </div>
        </div>
    );
}

// 정보 한 줄을 렌더링하는 내부 컴포넌트
function DetailItem({ icon, label, value, valueClass = "" }: { icon: React.ReactNode, label: string, value: string, valueClass?: string }) {
    return (
        <div className="flex items-start gap-4">
            <div className="p-2.5 bg-slate-100 dark:bg-slate-800 rounded-xl text-slate-600 dark:text-slate-400">
                {icon && <span className="[&>svg]:w-5 [&>svg]:h-5">{icon}</span>}
            </div>
            <div className="flex flex-col">
                <span className="text-xs text-slate-500 font-medium">{label}</span>
                <span className={`text-[15px] text-slate-900 dark:text-slate-200 mt-0.5 ${valueClass}`}>{value}</span>
            </div>
        </div>
    );
}