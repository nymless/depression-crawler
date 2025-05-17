'use client';
import { User } from '@/app/(server)/api/auth/login/route';
import type { AuthMeResponse } from '@/app/(server)/api/auth/me/route';
import { createContext, useContext, useEffect, useState } from 'react';

interface AuthContextType {
    user: User | null;
    setUser: (user: User | null) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        fetch('/api/auth/me')
            .then((res) => res.json())
            .then((data: AuthMeResponse) => {
                if (data.authenticated) setUser(data.user ?? null);
            });
    }, []);

    return (
        <AuthContext.Provider value={{ user, setUser }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
