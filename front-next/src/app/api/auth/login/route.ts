import { openDB, User } from '@/lib/db';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

export interface UserToken {
    id: number;
    username: string;
}

export async function POST(request: Request) {
    const { username, password } = await request.json();
    const db = await openDB();

    const result = await db.query('SELECT * FROM users WHERE username = $1', [
        username,
    ]);
    const user: User | undefined = result.rows[0];

    if (!(user && (await bcrypt.compare(password, user.password)))) {
        return new Response(JSON.stringify({ error: 'Invalid credentials' }), {
            status: 401,
        });
    }

    const userToken: UserToken = { id: user.id, username: user.username };
    const privateKey = process.env.JWT_SECRET;

    if (!privateKey) {
        console.error('JWT_SECRET is not defined in environment variables');
        return new Response(JSON.stringify({ error: 'Server login error' }), {
            status: 500,
        });
    }
    const token = jwt.sign(userToken, privateKey, { expiresIn: '1h' });

    // Use a non-Secure cookie in development to avoid issues over HTTP,
    // and a Secure cookie in production for safer transmission over HTTPS.
    const setCookieDev = `token=${token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=3600`;
    const setCookieProd = `token=${token}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=3600`;
    const setCookie =
        process.env.NODE_ENV === 'development' ? setCookieDev : setCookieProd;

    return new Response(JSON.stringify({ token }), {
        status: 200,
        headers: {
            'Set-Cookie': setCookie,
        },
    });
}
