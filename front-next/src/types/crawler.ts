export type CrawlerState =
    | 'idle' // waiting
    | 'collecting_posts' // collecting posts
    | 'collecting_comments' // collecting comments
    | 'preprocessing' // preprocessing data
    | 'inference' // inference
    | 'saving_results'; // saving results

export type CrawlerStatus = {
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
    current_status?: CrawlerStatus;
};

export type StopResponse = {
    status: string;
};
