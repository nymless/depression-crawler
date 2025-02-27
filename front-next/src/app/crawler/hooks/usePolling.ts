import { useEffect } from 'react';

export default function usePolling(
    callback: () => void,
    isActive: boolean,
    delay: number
) {
    useEffect(() => {
        if (!isActive) return;
        const intervalId = setInterval(callback, delay);
        return () => clearInterval(intervalId);
    }, [callback, isActive, delay]);
}
