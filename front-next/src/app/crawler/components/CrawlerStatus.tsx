import type { CrawlerStatusType } from '@/types/crawler';
import StopButton from './StopButton';

interface CrawlerStatusProps {
    status: CrawlerStatusType | null;
    onReset: () => void;
    onStop: () => Promise<void>;
    isWorking: boolean;
    loading: boolean;
}

export default function CrawlerStatus({
    status,
    onReset,
    onStop,
    isWorking,
    loading,
}: CrawlerStatusProps) {
    return (
        <div className="flex flex-col gap-2">
            <h2 className="font-bold text-xl">Crawler status</h2>
            <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2">
                    <p>
                        Status:{' '}
                        <span className={isWorking ? 'text-green-600' : ''}>
                            {status?.state ?? 'Loading...'}
                        </span>
                    </p>
                    {isWorking && (
                        <StopButton onClick={onStop} disabled={loading} />
                    )}
                </div>
                {status?.current_group && (
                    <p>Current group: {status.current_group}</p>
                )}
                {status?.progress !== null && (
                    <p className="text-gray-600">
                        Progress: {status?.progress}%
                    </p>
                )}
                {status?.error && (
                    <div className="flex flex-col gap-2">
                        <p className="text-red-500">{status.error}</p>
                        <button
                            onClick={onReset}
                            className="px-2 py-1 text-sm text-gray-600 hover:text-gray-800 self-start"
                        >
                            Reset
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}
