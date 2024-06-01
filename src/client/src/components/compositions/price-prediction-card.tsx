import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { cn, formatCurrency, formatDate } from '@/libs/utils';
import React from 'react';
import { Direction } from '@/libs/api';
import { TrendingDown, TrendingUp } from 'lucide-react';

type PricePredictionCardProps = {
  price: number;
  date: string;
  lastPrice: number;
};

const PricePredictionCard = ({
  date,
  price,
  lastPrice,
}: PricePredictionCardProps) => {
  const classes = {
    [Direction.UP]: 'text-green-500',
    [Direction.DOWN]: 'text-red-500',
  };

  const cardBorderClasses = {
    [Direction.UP]: 'border-green-500',
    [Direction.DOWN]: 'border-red-500',
  };

  const TrendingIcon = () => {
    if (price > lastPrice) {
      return <TrendingUp className={classes[Direction.UP]} />;
    }
    return <TrendingDown className={classes[Direction.DOWN]} />;
  };

  return (
    <Card
      className={cn(
        'w-[350px] bg-neutral-800 text-white',
        cardBorderClasses[price > lastPrice ? Direction.UP : Direction.DOWN]
      )}
    >
      <CardHeader>
        <CardTitle>Bitcoin Price Prediction</CardTitle>
        <CardDescription className={'text-neutral-300'}>
          Price prediction for {formatDate(date)}
        </CardDescription>
      </CardHeader>
      <CardContent className={'flex flex-row gap-4'}>
        <span>{formatCurrency(price)}</span>
        <TrendingIcon />
      </CardContent>
    </Card>
  );
};

export default PricePredictionCard;
