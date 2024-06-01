import { env } from '@/libs/env';

export enum DataType {
  HOURLY = 'hourly',
  DAILY = 'daily',
}

export enum Direction {
  UP = 'up',
  DOWN = 'down',
}

export type PriceData = {
  date: string;
  close: number;
  high: number;
  low: number;
  volume: number;
};

export type DirectionPrediction = {
  direction: Direction;
  date: string;
};

export type PricePrediction = {
  price: number;
  date: string;
};

export const getPriceForecast = async (data: DataType) => {
  const response = await fetch(
    `${env('NEXT_PUBLIC_API_URL')}/predict/price/${data}`
  );
  return (await response.json()) as PricePrediction;
};

export const getDirectionForecast = async (data: DataType) => {
  const response = await fetch(
    `${env('NEXT_PUBLIC_API_URL')}/predict/direction/${data}`
  );
  return (await response.json()) as DirectionPrediction;
};

export const getPriceHistory = async (data: DataType) => {
  const response = await fetch(`${env('NEXT_PUBLIC_API_URL')}/price/${data}`);
  return (await response.json()) as PriceData[];
};
