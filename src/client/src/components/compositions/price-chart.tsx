'use client';

import { Legend, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts';
import React, { useMemo } from 'react';
import { PriceData } from '@/libs/api';

type ChartProps = {
  data: PriceData[];
};

const PriceChart = ({ data }: ChartProps) => {
  const prices = useMemo(() => {
    return data.map((d) => {
      return {
        ...d,
        date: Intl.DateTimeFormat('en-DE', {
          hour: 'numeric',
          minute: 'numeric',
        }).format(new Date(d.date)),
      };
    });
  }, [data]);

  return (
    <LineChart
      width={1200}
      height={550}
      data={prices}
      margin={{ top: 5, right: 60, left: 60, bottom: 5 }}
    >
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
  );
};

export default PriceChart;
