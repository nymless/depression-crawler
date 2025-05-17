import { openDB, UserDB } from '@/lib/db';
import { JWT_SECRET } from '@/lib/env';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

export interface User {
    id: number;
    username: string;
}

export async function POST(request: Request) {
    const { username, password } = await request.json();
    const db = await openDB();

    const result = await db.query('SELECT * FROM users WHERE username = $1', [
        username,
    ]);
    const userBD: UserDB | undefined = result.rows[0];

    if (!(userBD && (await bcrypt.compare(password, userBD.password)))) {
        return new Response(JSON.stringify({ error: 'Invalid credentials' }), {
            status: 401,
        });
    }

    const user: User = { id: userBD.id, username: userBD.username };
    const token = jwt.sign(user, JWT_SECRET, { expiresIn: '1h' });

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
