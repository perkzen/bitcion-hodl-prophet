import { env } from '@/libs/env';
import axios from 'axios';

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

const api = axios.create({
  baseURL: env('NEXT_PUBLIC_API_URL'),
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getPriceForecast = async (data: DataType) => {
  const response = await api.get<PricePrediction>(`/predict/price/${data}`);
  return response.data as PricePrediction;
};

export const getDirectionForecast = async (data: DataType) => {
  const response = await api.get<DirectionPrediction>(
    `/predict/direction/${data}`
  );
  return response.data as DirectionPrediction;
};

export const getPriceHistory = async (data: DataType) => {
  const response = await api.get<PriceData[]>(`/price/${data}`);
  return response.data as PriceData[];
};
