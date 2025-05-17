import type { CrawlerStatus as CrawlerStatusType } from '@/types/crawler';

interface CrawlerStatusProps {
    status: CrawlerStatusType | null;
}

export default function CrawlerStatus({ status }: CrawlerStatusProps) {
    const isWorking = status?.state !== 'idle';

    return (
        <div className="flex flex-col gap-2">
            <p>
                Status:{' '}
                <span className={isWorking ? 'text-green-600' : ''}>
                    {status?.state ?? 'Loading...'}
                </span>
            </p>
            {status?.current_group && (
                <p>Current group: {status.current_group}</p>
            )}
            {status && status.progress > 0 && (
                <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                        className="bg-blue-600 h-2.5 rounded-full"
                        style={{ width: `${status.progress}%` }}
                    ></div>
                </div>
            )}
            {status?.error && (
                <p className="text-red-500">{status.error}</p>
            )}
        </div>
    );
} 