'use client';
import type {
    CollectDataRequest,
    CollectDataResponse,
    CrawlerStatus as CrawlerStatusType,
} from '@/types/crawler';
import { useCallback, useEffect, useState } from 'react';
import usePolling from './hooks/usePolling';
import CrawlerStatus from './components/CrawlerStatus';
import CrawlerForm from './components/CrawlerForm';
import StopButton from './components/StopButton';

const POLLING_INTERVAL = 2000;

export default function CrawlerPage() {
    const [status, setStatus] = useState<CrawlerStatusType | null>(null);
    const [loading, setLoading] = useState(false);
    const [isPolling, setIsPolling] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchStatus = useCallback(async () => {
        try {
            const res = await fetch('/api/crawler/status');
            const newStatus: CrawlerStatusType = await res.json();
            setStatus(newStatus);

            // Stop polling if crawler is idle
            if (newStatus.state === 'idle') {
                setIsPolling(false);
            }
        } catch (error) {
            console.error('Error fetching status:', error);
        }
    }, []);

    usePolling(fetchStatus, isPolling, POLLING_INTERVAL);

    const handleStop = async () => {
        setLoading(true);
        try {
            await fetch('/api/crawler/stop', { method: 'POST' });
            await fetchStatus();
        } catch (error) {
            console.error('Error stopping crawler:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCollect = async (request: CollectDataRequest) => {
        setLoading(true);
        setError(null);

        try {
            const res = await fetch('/api/crawler/collect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(request),
            });

            const data: CollectDataResponse = await res.json();
            if (data.error) {
                setError(data.error);
            } else {
                setIsPolling(true);
            }
        } catch (error) {
            console.error('Error collecting data:', error);
            setError('Failed to start data collection');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, [fetchStatus]);

    const isWorking = status?.state !== 'idle';

    return (
        <div className="flex flex-col gap-6 text-center">
            <h1 className="font-bold text-2xl">Crawler Control</h1>

            <CrawlerStatus status={status} />

            {isWorking && (
                <StopButton onClick={handleStop} disabled={loading} />
            )}

            <CrawlerForm
                onSubmit={handleCollect}
                loading={loading}
                isWorking={isWorking}
                error={error}
            />
        </div>
    );
}
