import { useQuery } from '@tanstack/react-query';
import {
  DataType,
  getDirectionForecast,
  getPriceForecast,
  getPriceHistory,
} from '@/api/index';

export const PRICE_FORECAST_QUERY_KEY = 'price-forecast';

export const usePriceForecast = (data: DataType) =>
  useQuery({
    queryKey: [PRICE_FORECAST_QUERY_KEY, data],
    queryFn: () => getPriceForecast(data),
  });

export const DIRECTION_FORECAST_QUERY_KEY = 'direction-forecast';
export const useDirectionForecast = (data: DataType) =>
  useQuery({
    queryKey: [DIRECTION_FORECAST_QUERY_KEY, data],
    queryFn: () => getDirectionForecast(data),
  });

export const PRICE_HISTORY_QUERY_KEY = 'price-history';
export const usePriceHistory = (data: DataType) =>
  useQuery({
    initialData: [],
    queryKey: [PRICE_HISTORY_QUERY_KEY, data],
    queryFn: () => getPriceHistory(data),
  });
