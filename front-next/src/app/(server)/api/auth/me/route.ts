import { JWT_SECRET } from '@/lib/env';
import jwt from 'jsonwebtoken';
import { User } from '../login/route';

export interface AuthMeResponse {
    authenticated: boolean;
    user?: User;
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
        const user = jwt.verify(token, JWT_SECRET) as User;
        response.authenticated = true;
        response.user = user;
        return new Response(JSON.stringify(response), { status: 200 });
    } catch {
        return new Response(JSON.stringify(response), {
            status: 401,
        });
    }
}
