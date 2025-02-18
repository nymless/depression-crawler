export async function POST() {
    const crawler_url = process.env.CRAWLER_URL;

    if (!crawler_url) {
        console.error("CRAWLER_URL is not defined in environment variables");
        return new Response(JSON.stringify({ error: "Server login error" }), {
            status: 500,
        });
    }

    const res = await fetch(`${crawler_url}/start`, { method: "POST" });
    const data = await res.json();

    return new Response(JSON.stringify(data), { status: res.status });
}
