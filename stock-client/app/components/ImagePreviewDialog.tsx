// ImagePreview.tsx
interface ImagePreviewProps {
    imgUrl?: string;
    isOpen: boolean;
    onClose: () => void;
}
import { X } from 'lucide-react';

export default function ImagePreviewDialog({
    imgUrl,
    isOpen,
    onClose,
}: ImagePreviewProps) {
    if (!isOpen || !imgUrl) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/40 backdrop-blur-sm"
                onClick={onClose}
            />

            {/* Dialog */}
            <div className="relative bg-white dark:bg-slate-900 rounded-2xl shadow-xl max-w-lg w-full mx-4 animate-scale-in">
                {/* Header */}
                <div className="flex items-center justify-between px-5 py-4 border-b border-slate-200 dark:border-slate-700">
                    <h3 className="text-lg font-semibold text-slate-900 dark:text-white">
                        Image Preview
                    </h3>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Image */}
                <div className="p-4">
                    <img
                        src={imgUrl}
                        alt="Product Preview"
                        className="w-full rounded-xl object-contain"
                    />
                </div>
            </div>
        </div>
    );
}
