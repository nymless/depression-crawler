'use client';
import type { CrawlerStatus, CrawlerSummary } from '@/types/crawler';
import { useCallback, useEffect, useState } from 'react';
import СrawlerSummary from './components/СrawlerSummary';
import usePolling from './hooks/usePolling';

const POLLING_INTERVAL = 2000;

export default function CrawlerPage() {
    const [running, setRunning] = useState<'Running' | 'Stopped' | null>(null);
    const [summary, setSummary] = useState<CrawlerSummary | null>(null);
    const [loading, setLoading] = useState(false);
    const [isPolling, setIsPolling] = useState(false);

    const fetchStatus = useCallback(async () => {
        try {
            const res = await fetch('/api/crawler/status', {
                cache: 'no-store',
            });
            const status: CrawlerStatus = await res.json();
            setRunning(status.running ? 'Running' : 'Stopped');
            setSummary({
                requests_count: status.requests_count,
                saved_posts_count: status.saved_posts_count,
            });
        } catch (error) {
            console.error('Error fetching status:', error);
        }
    }, []);

    usePolling(fetchStatus, isPolling, POLLING_INTERVAL);

    const handleStart = async () => {
        setLoading(true);
        try {
            await fetch('/api/crawler/start', { method: 'POST' });
            await fetchStatus();
            setIsPolling(true);
        } catch (error) {
            console.error('Error starting crawler:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleStop = async () => {
        setLoading(true);
        try {
            await fetch('/api/crawler/stop', { method: 'POST' });
            setIsPolling(false);
            await fetchStatus();
        } catch (error) {
            console.error('Error stopping crawler:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, [fetchStatus]);

    return (
        <div className="flex flex-col gap-6 text-center">
            <h1 className="font-bold text-2xl">Crawler Control</h1>
            <p className="">
                Status:{' '}
                <span className={running === 'Running' ? 'text-green-600' : ''}>
                    {running ?? 'Loading...'}
                </span>
            </p>
            <button
                onClick={handleStart}
                disabled={loading}
                className="hover:text-gray-500"
            >
                Start
            </button>
            <button
                onClick={handleStop}
                disabled={loading}
                className="hover:text-gray-500"
            >
                Stop
            </button>
            <СrawlerSummary summary={summary} />
        </div>
    );
}
