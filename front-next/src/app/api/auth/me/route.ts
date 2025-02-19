import { JWT_SECRET } from '@/lib/env';
import jwt, { JwtPayload } from 'jsonwebtoken';

interface AuthMeResponse {
    authenticated: boolean;
    user?: string | JwtPayload;
}

export async function GET(request: Request) {
    const token = request.headers.get('cookie')?.split('=')[1];
    const response: AuthMeResponse = { authenticated: false };

    if (!token) {
        return new Response(JSON.stringify(response), {
            status: 401,
        });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        response.authenticated = true;
        response.user = decoded;
        return new Response(JSON.stringify(response), { status: 200 });
    } catch {
        return new Response(JSON.stringify(response), {
            status: 401,
        });
    }
}
