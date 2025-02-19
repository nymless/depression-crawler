import { CRAWLER_URL } from '@/lib/env';

export async function GET() {
    const res = await fetch(`${CRAWLER_URL}/status`);
    const data = await res.json();

    return new Response(JSON.stringify(data), { status: res.status });
}
