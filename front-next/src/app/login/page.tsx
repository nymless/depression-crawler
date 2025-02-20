'use client';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';

export default function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();

    const handleLogin = async (event: FormEvent) => {
        event.preventDefault();
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });

        if (res.ok) {
            router.push('/');
            router.refresh();
        } else alert('Invalid credentials');
    };

    return (
        <div className="flex flex-col gap-5">
            <h1 className="text-center text-xl">Login</h1>
            <form onSubmit={handleLogin} className="flex gap-2">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    required
                    className="bg-white text-black p-1"
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    required
                    className="bg-white text-black p-1"
                />
                <button type="submit" className="hover:text-gray-500">
                    Login
                </button>
            </form>
        </div>
    );
}
