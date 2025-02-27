import { CrawlerSummary } from '@/types/crawler';

interface Props {
    summary: CrawlerSummary | null;
}

const СrawlerSummary = (props: Props) => {
    if (props.summary) {
        return <div>{JSON.stringify(props.summary)}</div>;
    }
};

export default СrawlerSummary;
