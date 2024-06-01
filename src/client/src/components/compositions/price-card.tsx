import React from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { formatCurrency, formatDate } from '@/libs/utils';

type PriceCardProps = {
  price: number;
  date: string;
};

const PriceCard = ({ price, date }: PriceCardProps) => {
  return (
    <Card className="w-[350px] bg-neutral-800 border-[#F6931D] text-white">
      <CardHeader>
        <CardTitle>Bitcoin Price</CardTitle>
        <CardDescription className={'text-neutral-300'}>
          Price as of {formatDate(date)}
        </CardDescription>
      </CardHeader>
      <CardContent>{formatCurrency(price)}</CardContent>
    </Card>
  );
};

export default PriceCard;
