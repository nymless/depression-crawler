import { useState } from 'react';
import type { CollectDataRequest } from '@/types/crawler';

interface CrawlerFormProps {
    onSubmit: (request: CollectDataRequest) => Promise<void>;
    loading: boolean;
    isWorking: boolean;
    error: string | null;
}

export default function CrawlerForm({ onSubmit, loading, isWorking, error }: CrawlerFormProps) {
    const [groups, setGroups] = useState<string>('');
    const [targetDate, setTargetDate] = useState<string>('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        const groupsList = groups
            .split(',')
            .map((g: string) => g.trim())
            .filter(Boolean);
            
        if (!groupsList.length) {
            return;
        }

        const request: CollectDataRequest = {
            groups: groupsList,
            target_date: targetDate,
        };

        await onSubmit(request);
        setGroups('');
        setTargetDate('');
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <h2 className="font-bold text-xl">Collect Data</h2>
            <div>
                <label htmlFor="groups" className="block mb-2">
                    Groups (comma-separated):
                </label>
                <input
                    type="text"
                    id="groups"
                    value={groups}
                    onChange={(e) => setGroups(e.target.value)}
                    placeholder="group1, group2, group3"
                    className="w-full p-2 border rounded"
                    disabled={loading || isWorking}
                />
            </div>
            <div>
                <label htmlFor="date" className="block mb-2">
                    Target Date:
                </label>
                <input
                    type="date"
                    id="date"
                    value={targetDate}
                    onChange={(e) => setTargetDate(e.target.value)}
                    className="w-full p-2 border rounded"
                    disabled={loading || isWorking}
                />
            </div>
            {error && <p className="text-red-500">{error}</p>}
            <button
                type="submit"
                disabled={loading || isWorking}
                className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 disabled:opacity-50"
            >
                Collect Data
            </button>
        </form>
    );
} 