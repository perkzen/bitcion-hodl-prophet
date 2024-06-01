import { Direction } from '@/libs/api';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { cn, formatDate } from '@/libs/utils';
import React from 'react';
import { TrendingDown, TrendingUp } from 'lucide-react';

type DirectionPredictionCardProps = {
  direction: Direction;
  date: string;
};

const DirectionPredictionCard = ({
  direction,
  date,
}: DirectionPredictionCardProps) => {
  const classes = {
    [Direction.UP]: 'text-green-500',
    [Direction.DOWN]: 'text-red-500',
  };

  const cardBorderClasses = {
    [Direction.UP]: 'border-green-500',
    [Direction.DOWN]: 'border-red-500',
  };

  const TrendingIcon = () => {
    if (direction === Direction.UP) {
      return <TrendingUp className={classes[Direction.UP]} />;
    }
    return <TrendingDown className={classes[Direction.DOWN]} />;
  };

  return (
    <Card
      className={cn(
        'w-[350px] bg-neutral-800 text-white',
        cardBorderClasses[direction]
      )}
    >
      <CardHeader>
        <CardTitle>Bitcoin Price Prediction</CardTitle>
        <CardDescription className={'text-neutral-300'}>
          Direction prediction for {formatDate(date)}
        </CardDescription>
      </CardHeader>
      <CardContent className={'flex flex-row gap-4'}>
        <span className={'capitalize'}>{direction}</span>
        <TrendingIcon />
      </CardContent>
    </Card>
  );
};

export default DirectionPredictionCard;
