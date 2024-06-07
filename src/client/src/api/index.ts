import axios from 'axios';

export enum DataType {
  HOURLY = 'hourly',
  DAILY = 'daily',
}

export enum Direction {
  UP = 'up',
  DOWN = 'down',
}

export enum ModelType {
  REGRESSION = 'reg',
  CLASSIFICATION = 'cls',
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

export type AuditLog = {
  model_type: ModelType;
  data_type: DataType;
  model_version: string;
  prediction: {
    date: string;
    price?: number;
    direction?: Direction;
  };
  created_at: string;
};

export type ClsMetric = {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
};

export type RegMetric = {
  mae: number;
  mse: number;
  evs: number;
};

export type Metric = {
  model_type: ModelType;
  data_type: DataType;
  model_version: string;
  metrics: ClsMetric | RegMetric;
};

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
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

export const getAuditLogs = async () => {
  const response = await api.get('/audit-log');
  return response.data as AuditLog[];
};

export const getMetrics = async () => {
  const response = await api.get('/metrics');
  return response.data as Metric[];
};
