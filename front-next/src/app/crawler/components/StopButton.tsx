import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useState } from 'react';

interface StopButtonProps {
    onClick: () => Promise<void>;
    disabled: boolean;
}

export default function StopButton({ onClick, disabled }: StopButtonProps) {
    const [isOpen, setIsOpen] = useState(false);

    const handleStop = async () => {
        setIsOpen(false);
        await onClick();
    };

    return (
        <>
            <button
                onClick={() => setIsOpen(true)}
                disabled={disabled}
                className="px-2 py-1 text-sm text-gray-600 hover:text-gray-800 disabled:opacity-50"
            >
                Stop
            </button>

            <Transition appear show={isOpen} as={Fragment}>
                <Dialog
                    as="div"
                    className="relative z-10"
                    onClose={() => setIsOpen(false)}
                >
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                    <Dialog.Title
                                        as="h3"
                                        className="text-lg font-medium leading-6 text-gray-900"
                                    >
                                        Stop Crawler
                                    </Dialog.Title>
                                    <div className="mt-2">
                                        <p className="text-sm text-gray-500">
                                            Are you sure you want to stop the
                                            crawler? This action cannot be
                                            undone.
                                        </p>
                                    </div>

                                    <div className="mt-4 flex justify-end gap-2">
                                        <button
                                            type="button"
                                            className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                                            onClick={() => setIsOpen(false)}
                                        >
                                            Cancel
                                        </button>
                                        <button
                                            type="button"
                                            className="px-3 py-1 text-sm text-red-600 hover:text-red-800"
                                            onClick={handleStop}
                                        >
                                            Stop
                                        </button>
                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </>
    );
}
