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
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop: 블러 강도를 높여 더 모던하게 변경 */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-md transition-opacity"
                onClick={onClose}
            />

            {/* Dialog: 고정된 정사각형 비율 유지 */}
            <div className="relative bg-white dark:bg-slate-900 rounded-xl shadow-2xl max-w-md w-full overflow-hidden animate-in fade-in zoom-in duration-200">
                
                {/* Close Button: 헤더를 없애고 이미지 위에 띄워 깔끔하게 처리 */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 z-10 p-2 bg-black/20 hover:bg-black/40 backdrop-blur-sm text-white rounded-full transition-colors"
                >
                    <X className="w-5 h-5" />
                </button>

                {/* Image Container: 1:1 비율 고정 */}
                <div className="aspect-square w-full bg-slate-100 dark:bg-slate-800">
                    <img
                        src={imgUrl}
                        alt="Product Preview"
                        className="w-full h-full object-cover" // 정사각형을 가득 채우도록 설정
                    />
                </div>

                <div className="p-5 text-center">
                </div>
            </div>
        </div>
    );
}