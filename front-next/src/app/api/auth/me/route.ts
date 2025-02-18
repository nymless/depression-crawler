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

    const privateKey = process.env.JWT_SECRET;
    
    if (!privateKey) {
        console.error('JWT_SECRET is not defined in environment variables');
        return new Response(JSON.stringify({ error: 'Server login error' }), {
            status: 500,
        });
    }

    try {
        const decoded = jwt.verify(token, privateKey);
        response.authenticated = true;
        response.user = decoded;
        return new Response(JSON.stringify(response), { status: 200 });
    } catch {
        return new Response(JSON.stringify(response), {
            status: 401,
        });
    }
}
