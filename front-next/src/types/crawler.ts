export type CrawlerState =
    | "idle" // waiting
    | "collecting_groups" // collecting groups info
    | "preprocessing_groups" // preprocessing groups info
    | "collecting_data" // collecting posts and comments
    | "preprocessing" // preprocessing data
    | "inference" // inference
    | "saving_results"; // saving results

export type CrawlerStatusType = {
    state: CrawlerState;
    current_group: string | null;
    progress: number | null;
    error: string | null;
    should_stop: boolean;
};

export type CollectDataRequest = {
    groups: string[];
    target_date: string;
};

export type CollectDataResponse = {
    status: string;
    groups: string[];
    target_date: string;
    error?: string;
    current_status?: CrawlerStatusType;
};

export type StopResponse = {
    status: string;
};
