import { CRAWLER_URL } from '@/lib/env';

export async function POST() {
    const res = await fetch(`${CRAWLER_URL}/reset`, {
        method: 'POST',
    });
    const data = await res.json();

    return new Response(JSON.stringify(data), { status: res.status });
}
