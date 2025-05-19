import type { CrawlerStatusType } from '@/types/crawler';

interface CrawlerStatusProps {
    status: CrawlerStatusType | null;
    onReset?: () => void;
}

export default function CrawlerStatus({ status, onReset }: CrawlerStatusProps) {
    const isWorking = status?.state !== 'idle';

    return (
        <div className="flex flex-col gap-2">
            <div className="flex justify-between items-center">
                <p>
                    Status:{' '}
                    <span className={isWorking ? 'text-green-600' : ''}>
                        {status?.state ?? 'Loading...'}
                    </span>
                </p>
                {status?.error && (
                    <button
                        onClick={onReset}
                        className="px-2 py-1 text-sm text-gray-600 hover:text-gray-800"
                    >
                        Reset
                    </button>
                )}
            </div>
            {status?.current_group && (
                <p>Current group: {status.current_group}</p>
            )}
            {status && status.progress !== null && (
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                        className="bg-blue-600 h-2.5 rounded-full"
                        style={{ width: `${status.progress}%` }}
                    ></div>
                </div>
            )}
            {status?.error && <p className="text-red-500">{status.error}</p>}
        </div>
    );
}
