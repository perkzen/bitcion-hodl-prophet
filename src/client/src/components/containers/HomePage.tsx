'use client';
import { DataType } from '@/api';
import PriceCard from '@/components/compositions/price-card';
import PricePredictionCard from '@/components/compositions/price-prediction-card';
import DirectionPredictionCard from '@/components/compositions/direction-prediction-card';
import PriceChart from '@/components/compositions/price-chart';
import {
  useDirectionForecast,
  usePriceForecast,
  usePriceHistory,
} from '@/api/hooks';

type HomeProps = {
  dataType: DataType;
};

const HomePage = ({ dataType }: HomeProps) => {
  const { data: prices } = usePriceHistory(dataType);
  const currentPrice = prices[prices.length - 1].close;
  const lastDate = prices[prices.length - 1].date;

  const { data: pricePrediction } = usePriceForecast(dataType);
  const { data: directionPrediction } = useDirectionForecast(dataType);

  return (
    <>
      <div className={'flex flex-row flex-wrap gap-4 justify-center w-full'}>
        <PriceCard price={currentPrice} date={lastDate} />
        <PricePredictionCard
          lastPrice={currentPrice}
          price={pricePrediction?.price!}
          date={pricePrediction?.date!}
        />
        <DirectionPredictionCard
          direction={directionPrediction?.direction!}
          date={directionPrediction?.date!}
        />
      </div>
      <div className={'mx-auto w-full'}>
        <PriceChart dataType={dataType} data={prices} />
      </div>
    </>
  );
};

export default HomePage;
