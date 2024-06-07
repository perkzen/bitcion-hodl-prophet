'use client';

import {
  Area,
  AreaChart,
  Label,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import React, { useMemo } from 'react';
import { DataType, PriceData } from '@/api';
import { formatCurrency, formatDate } from '@/libs/utils';
import useIsMobile from '@/libs/use-is-mobile';

type ChartProps = {
  data: PriceData[];
  dataType: DataType;
};

const PriceChart = ({ data, dataType }: ChartProps) => {
  const isMobile = useIsMobile();

  const prices = useMemo(() => {
    if (data.length === 0 || !data) {
      return [];
    }

    return data?.map((d) => {
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
      <AreaChart
        data={prices}
        margin={{ right: 60, left: 60, top: 30, bottom: 30 }}
      >
        <XAxis type={'category'} dataKey="date" xAxisId={0} tick={{ dy: 5 }}>
          <Label value="Date" offset={0} position="bottom" />
        </XAxis>
        <YAxis
          type={'number'}
          domain={['dataMin - 500', 'dataMax + 500']}
          dataKey="close"
          yAxisId={0}
          tick={{ dx: -5 }}
        >
          <Label
            value={'Price ($)'}
            offset={-40}
            angle={-90}
            position="insideLeft"
          />
        </YAxis>
        <Tooltip
          content={(props) => {
            const y = props.payload?.[0]?.value;
            const x = props.payload?.[0]?.payload?.date;

            if (!y || !x) return null;

            return (
              <div
                className={
                  'bg-neutral-800 border border-[#F6931D] px-4 py-2 shadow rounded-md'
                }
              >
                <div>{formatCurrency(Number(y))}</div>
                <div>{formatDate(x)}</div>
              </div>
            );
          }}
        />
        <defs>
          <linearGradient id="color" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#F6931D" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#26262" stopOpacity={0} />
          </linearGradient>
        </defs>
        <Area
          type="monotone"
          dataKey="close"
          stroke="#F6931D"
          fillOpacity={1}
          fill="url(#color)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;
