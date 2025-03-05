'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from './AuthProvider';

export default function Header() {
    const { user, setUser } = useAuth();
    const router = useRouter();

    const handleLogout = async () => {
        const res = await fetch('/api/auth/logout', { method: 'POST' });
        if (res.ok) {
            setUser(null);
            router.refresh();
        }
    };

    return (
        <header className="h-16 w-full flex items-center px-8 shadow-md bg-[#3F3F4B] text-white">
            <p className="font-bold text-2xl">Depression Crawler</p>

            <nav className="flex-1 flex justify-center gap-16 text-lg">
                {user && (
                    <>
                        <Link href="/" className="hover:underline">
                            Home
                        </Link>
                        <Link href="/crawler" className="hover:underline">
                            Crawler
                        </Link>
                        <Link href="/dashboard" className="hover:underline">
                            Dashboard
                        </Link>
                        <Link href="/about" className="hover:underline">
                            About
                        </Link>
                    </>
                )}
            </nav>

            {user ? (
                <div className="flex items-center gap-4">
                    <span className="text-lg">{user.username}</span>
                    <button
                        onClick={handleLogout}
                        className="text-lg hover:underline"
                    >
                        Logout
                    </button>
                </div>
            ) : (
                <Link href="/login" className="text-lg hover:underline">
                    Login
                </Link>
            )}
        </header>
    );
}
