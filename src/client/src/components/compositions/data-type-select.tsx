'use client';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useRouter, useSearchParams } from 'next/navigation';
import { useCallback, useEffect, useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import {
  DIRECTION_FORECAST_QUERY_KEY,
  PRICE_FORECAST_QUERY_KEY,
  PRICE_HISTORY_QUERY_KEY,
} from '@/api/hooks';

const DataTypeSelect = () => {
  const router = useRouter();
  const params = useSearchParams();

  const [selected, setSelected] = useState<string>(
    params.get('data') || 'daily'
  );

  const queryClient = useQueryClient();

  const handleSelect = useCallback(
    async (value: string) => {
      setSelected(value);
      router.push(`?data=${value}`, {});
      await queryClient.invalidateQueries({
        queryKey: [value],
      });
    },
    [queryClient, router]
  );

  useEffect(() => {
    if (!params.has('data')) {
      handleSelect(selected);
    }
  }, [handleSelect, params, selected]);

  return (
    <Select defaultValue={selected} onValueChange={handleSelect}>
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select a interval" />
      </SelectTrigger>
      <SelectContent className={'bg-neutral-800'}>
        <SelectGroup>
          <SelectLabel>Data interval</SelectLabel>
          <SelectItem value="hourly">Hourly</SelectItem>
          <SelectItem value="daily">Daily</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
};

export default DataTypeSelect;
