'use client';
import { useAuth } from '@/components/AuthProvider';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { AuthMeResponse } from '../(server)/api/auth/me/route';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();
    const { setUser } = useAuth();

    const handleLogin = async (event: FormEvent) => {
        event.preventDefault();
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        if (res.ok) {
            const authRes = await fetch('/api/auth/me');
            const data: AuthMeResponse = await authRes.json();
            if (data.authenticated) {
                setUser(data.user ?? null);
                router.push('/');
            }
        } else alert('Invalid credentials');
    };

    return (
        <div className="flex flex-col gap-6 text-center">
            <h1 className="font-bold text-2xl">Login</h1>
            <form onSubmit={handleLogin} className="flex gap-2">
                <input
                    type="text"
                    placeholder="Username"
                    autoComplete="username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    required
                    className="p-1"
                />
                <input
                    type="password"
                    placeholder="Password"
                    autoComplete="current-password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                    className="p-1"
                />
                <button type="submit" className="hover:underline">
                    Login
                </button>
            </form>
        </div>
    );
}
