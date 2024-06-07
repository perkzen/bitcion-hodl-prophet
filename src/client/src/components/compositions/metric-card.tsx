import { ClsMetric, DataType, Metric, ModelType, RegMetric } from '@/api';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import React from 'react';
import { formatDate } from '@/libs/utils';

type MetricCardProps = {
  metric: Metric;
};

const MetricCard = ({ metric }: MetricCardProps) => {
  const getTitle = () => {
    let title = '';

    if (metric.data_type === DataType.DAILY) {
      title += 'Daily';
    }

    if (metric.data_type === DataType.HOURLY) {
      title += 'Hourly';
    }

    if (metric.model_type === ModelType.REGRESSION) {
      title += ' Price Prediction Model';
    }

    if (metric.model_type === ModelType.CLASSIFICATION) {
      title += ' Trend Prediction Model';
    }

    return title;
  };

  const getMetrics = () => {
    if (metric.model_type === ModelType.REGRESSION) {
      const metrics = metric.metrics as RegMetric;

      return (
        <div>
          <div>MAE: {metrics.mae}</div>
          <div>MSE: {metrics.mse}</div>
          <div>EVS: {metrics.evs}</div>
        </div>
      );
    }

    if (metric.model_type === ModelType.CLASSIFICATION) {
      const metrics = metric.metrics as ClsMetric;

      return (
        <div>
          <div>Accuracy: {metrics.accuracy}</div>
          <div>Precision: {metrics.precision}</div>
          <div>Recall: {metrics.recall}</div>
        </div>
      );
    }
  };

  return (
    <Card className="bg-neutral-800 text-white">
      <CardHeader>
        <CardTitle>
          {getTitle()}{' '}
          <span className={'font-light text-sm'}>v{metric.model_version}</span>
        </CardTitle>
        <CardDescription className={'text-neutral-300'}>
          {formatDate(metric.created_at)}
        </CardDescription>
      </CardHeader>
      <CardContent>{getMetrics()}</CardContent>
    </Card>
  );
};

export default MetricCard;
