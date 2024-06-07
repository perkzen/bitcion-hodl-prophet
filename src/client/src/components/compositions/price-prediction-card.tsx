import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { cn, formatCurrency, formatDate } from '@/libs/utils';
import React from 'react';
import { Direction } from '@/api';
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
  return (
    <Card
      className={cn('w-[350px] border-[#F6931D] bg-neutral-800 text-white')}
    >
      <CardHeader>
        <CardTitle>Bitcoin Price Prediction</CardTitle>
        <CardDescription className={'text-neutral-300'}>
          Price prediction for {formatDate(date)}
        </CardDescription>
      </CardHeader>
      <CardContent className={'flex flex-row gap-4'}>
        <span className={price > lastPrice ? 'text-green-500' : 'text-red-500'}>
          {formatCurrency(price)}
        </span>
      </CardContent>
    </Card>
  );
};

export default PricePredictionCard;
