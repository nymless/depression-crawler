'use client';
import { useEffect, useState } from 'react';

export default function CrawlerPage() {
    const [status, setStatus] = useState<'Running' | 'Stopped' | null>(null);
    const [loading, setLoading] = useState(false);

    const fetchStatus = async () => {
        try {
            const res = await fetch('/api/crawler/status');
            const data = await res.json();
            setStatus(data.running ? 'Running' : 'Stopped');
        } catch (error) {
            console.error('Error fetching status:', error);
        }
    };

    const handleStart = async () => {
        setLoading(true);
        try {
            await fetch('/api/crawler/start', { method: 'POST' });
            fetchStatus();
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
            fetchStatus();
        } catch (error) {
            console.error('Error stopping crawler:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, []);

    return (
        <div className="flex flex-col gap-5">
            <h1 className="text-center text-xl">Crawler Control</h1>
            <p className="text-center">
                Status:{' '}
                <span className={status === 'Running' ? 'text-green-600' : ''}>
                    {status ?? 'Loading...'}
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
        </div>
    );
}
