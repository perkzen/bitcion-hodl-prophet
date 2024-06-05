import { DataType, getPriceForecast, getPriceHistory } from '@/api';
import HomePage from '@/components/containers/HomePage';
import { Suspense } from 'react';
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query';
import { PRICE_FORECAST_QUERY_KEY, PRICE_HISTORY_QUERY_KEY } from '@/api/hooks';

type HomeProps = {
  searchParams: { data: DataType };
};

export default async function Home({ searchParams }: HomeProps) {
  const dataType = searchParams.data || DataType.DAILY;

  const queryClient = new QueryClient();

  await queryClient.prefetchQuery({
    queryKey: [PRICE_HISTORY_QUERY_KEY, dataType],
    queryFn: () => getPriceHistory(dataType),
  });

  await queryClient.prefetchQuery({
    queryKey: [PRICE_FORECAST_QUERY_KEY, dataType],
    queryFn: () => getPriceForecast(dataType),
  });

  await queryClient.prefetchQuery({
    queryKey: [PRICE_FORECAST_QUERY_KEY, dataType],
    queryFn: () => getPriceForecast(dataType),
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Suspense
        fallback={
          <div className={'text-white text-lg py-20 text-center'}>
            Loading...
          </div>
        }
      >
        <HomePage />
      </Suspense>
    </HydrationBoundary>
  );
}
