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

const DataTypeSelect = () => {
  const router = useRouter();
  const params = useSearchParams();

  const [selected, setSelected] = useState<string>(
    params.get('data') || 'daily'
  );
  const handleSelect = useCallback(
    (value: string) => {
      setSelected(value);
      router.push(`?data=${value}`, {});
    },
    [router]
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
      <SelectContent className={'bg-neutral-800 text-white'}>
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
