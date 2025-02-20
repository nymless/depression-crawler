'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

interface User {
    id: number;
    username: string;
}

export default function Home() {
    const [user, setUser] = useState<User | null>(null);
    const router = useRouter();

    useEffect(() => {
        fetch('/api/auth/me')
            .then((res) => res.json())
            .then((data: { authenticated: boolean; user?: User }) => {
                if (!data.authenticated) router.push('/login');
                else setUser(data.user ?? null);
            });
    }, [router]);

    const handleLogout = async () => {
        const res = await fetch('/api/auth/logout', {
            method: 'POST',
        });
        if (res.ok) {
            setUser(null);
            router.refresh();
        }
    };

    return (
        <div className="flex flex-col gap-5">
            <h1 className="text-center text-xl">Home</h1>
            <div className="text-center">Welcome {user?.username} </div>
            <Link href={'/crawler'} className="text-center hover:underline">
                Сrawler
            </Link>
            <button
                onClick={handleLogout}
                className={user ? 'hover:text-gray-500' : 'hidden'}
            >
                Logout
            </button>
        </div>
    );
}
