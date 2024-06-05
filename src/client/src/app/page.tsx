import {
  DataType,
  Direction,
  getDirectionForecast,
  getPriceForecast,
  getPriceHistory,
} from '@/libs/api';

import dynamic from 'next/dynamic';
import PriceCard from '@/components/compositions/price-card';
import PricePredictionCard from '@/components/compositions/price-prediction-card';
import DirectionPredictionCard from '@/components/compositions/direction-prediction-card';

const Chart = dynamic(() => import('@/components/compositions/price-chart'), {
  ssr: false,
});
export const revalidate = 0;

type HomeProps = {
  searchParams: { data: DataType };
};

export default async function Home({ searchParams }: HomeProps) {
  const dataType = searchParams.data || DataType.DAILY;

  const prices = await getPriceHistory(dataType);
  const currentPrice = prices[prices.length - 1].close;
  const lastDate = prices[prices.length - 1].date;

  const pricePrediction = await getPriceForecast(dataType);
  const directionPrediction = await getDirectionForecast(dataType);

  return (
    <main className="flex w-full flex-col gap-8 sm:gap-20 px-2 sm:px-24 py-8">
      <div className={'flex flex-row flex-wrap gap-4 justify-center w-full'}>
        <PriceCard price={currentPrice} date={lastDate} />
        <PricePredictionCard
          lastPrice={currentPrice}
          price={pricePrediction.price}
          date={pricePrediction.date}
        />
        <DirectionPredictionCard
          direction={directionPrediction.direction}
          date={directionPrediction.date}
        />
      </div>
      <div className={'mx-auto w-full'}>
        <Chart data={prices} dataType={dataType} />
      </div>
    </main>
  );
}
