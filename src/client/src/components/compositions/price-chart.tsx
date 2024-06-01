'use client';

import {
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import React, { useMemo } from 'react';
import { DataType, PriceData } from '@/libs/api';
import { formatDate } from '@/libs/utils';

type ChartProps = {
  data: PriceData[];
  dataType: DataType;
};

const PriceChart = ({ data, dataType }: ChartProps) => {
  const prices = useMemo(() => {
    return data.map((d) => {
      return {
        ...d,
        date:
          dataType === DataType.DAILY
            ? formatDate(d.date).split(',')[0]
            : formatDate(d.date),
      };
    });
  }, [data, dataType]);

  return (
    <ResponsiveContainer width={'100%'} height={500}>
      <LineChart data={prices} margin={{ right: 30, left: 30 }}>
        <XAxis label={'Date'} type={'category'} dataKey="date" xAxisId={0} />
        <YAxis
          label={'Price'}
          type={'number'}
          domain={['dataMin - 500', 'dataMax + 500']}
          dataKey="close"
          yAxisId={0}
        />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="close" stroke="#F6931D" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;
