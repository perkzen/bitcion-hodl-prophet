import {
  DataType,
  getDirectionForecast,
  getPriceForecast,
  getPriceHistory,
} from '@/api';
import HomePage from '@/components/containers/HomePage';
import { Suspense } from 'react';
import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query';
import {
  DIRECTION_FORECAST_QUERY_KEY,
  PRICE_FORECAST_QUERY_KEY,
  PRICE_HISTORY_QUERY_KEY,
} from '@/api/hooks';

type HomeProps = {
  searchParams: { data: DataType };
};

export default async function Home({ searchParams }: HomeProps) {
  const dataType = searchParams.data || DataType.DAILY;
  const queryClient = new QueryClient();

  await Promise.all([
    queryClient.prefetchQuery({
      queryFn: () => getPriceHistory(dataType),
      queryKey: [PRICE_HISTORY_QUERY_KEY, dataType],
    }),
    queryClient.prefetchQuery({
      queryFn: () => getPriceForecast(dataType),
      queryKey: [PRICE_FORECAST_QUERY_KEY, dataType],
    }),
    queryClient.prefetchQuery({
      queryFn: () => getDirectionForecast(dataType),
      queryKey: [DIRECTION_FORECAST_QUERY_KEY, dataType],
    }),
  ]);

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Suspense
        fallback={
          <div className={'text-white text-lg py-20 text-center'}>
            Loading...
          </div>
        }
      >
        <HomePage dataType={dataType} />
      </Suspense>
    </HydrationBoundary>
  );
}
