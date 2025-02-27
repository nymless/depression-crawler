export type CrawlerStatus = {
    running: boolean;
    requests_count: number;
    saved_posts_count: number;
};

export type CrawlerSummary = Omit<CrawlerStatus, 'running'>;
