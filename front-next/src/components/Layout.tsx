import Header from './Header';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex flex-col min-h-screen bg-[#F4F4F4]">
            <Header />
            <main className="flex-1 w-full flex justify-center py-6">
                {children}
            </main>
        </div>
    );
}
