import { AuthProvider } from '@/components/AuthProvider';
import Layout from '@/components/Layout';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
    subsets: ['latin'],
});

export const metadata: Metadata = {
    title: 'Depression Crawler',
    description: "Master's thesis project",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <AuthProvider>
            <html lang="en">
                <body className={`${inter.className}`}>
                    <Layout>{children}</Layout>
                </body>
            </html>
        </AuthProvider>
    );
}
