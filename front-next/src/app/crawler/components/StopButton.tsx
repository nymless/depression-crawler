interface StopButtonProps {
    onClick: () => Promise<void>;
    disabled: boolean;
}

export default function StopButton({ onClick, disabled }: StopButtonProps) {
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className="bg-red-500 text-white p-2 rounded hover:bg-red-600 disabled:opacity-50"
        >
            Stop Crawler
        </button>
    );
} 