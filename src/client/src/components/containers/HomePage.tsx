'use client';
import { DataType } from '@/api';
import PriceCard from '@/components/compositions/price-card';
import PricePredictionCard from '@/components/compositions/price-prediction-card';
import DirectionPredictionCard from '@/components/compositions/direction-prediction-card';
import {
  useDirectionForecast,
  usePriceForecast,
  usePriceHistory,
} from '@/api/hooks';
import PriceChart from '@/components/compositions/price-chart';
import { useSearchParams } from 'next/navigation';

const HomePage = () => {
  const params = useSearchParams();
  const dataType = (params.get('data') as DataType) || DataType.DAILY;

  const { data: prices } = usePriceHistory(dataType);

  const currentPrice = prices[prices.length - 1]?.close;
  const lastDate = prices[prices.length - 1]?.date;

  const { data: pricePrediction } = usePriceForecast(dataType);
  const { data: directionPrediction } = useDirectionForecast(dataType);

  return (
    <main className="flex w-full flex-col gap-8 sm:gap-20 px-2 sm:px-24 py-8">
      <div className={'flex flex-row flex-wrap gap-4 justify-center w-full'}>
        {currentPrice && lastDate && (
          <PriceCard price={currentPrice} date={lastDate} />
        )}
        {pricePrediction && (
          <PricePredictionCard
            lastPrice={currentPrice}
            price={pricePrediction?.price}
            date={pricePrediction?.date}
          />
        )}

        {directionPrediction && (
          <DirectionPredictionCard
            direction={directionPrediction?.direction}
            date={directionPrediction?.date}
          />
        )}
      </div>
      <div className={'mx-auto w-full'}>
        <PriceChart dataType={dataType} data={prices} />
      </div>
    </main>
  );
};

export default HomePage;
