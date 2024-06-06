import { DataType } from '@/api';
import HomePage from '@/components/containers/HomePage';
import { Suspense } from 'react';

type HomeProps = {
  searchParams: { data: DataType };
};

export default async function Home({ searchParams }: HomeProps) {
  const dataType = searchParams.data || DataType.DAILY;

  return (
    <Suspense
      fallback={
        <div className={'text-white text-lg py-20 text-center'}>Loading...</div>
      }
    >
      <HomePage dataType={dataType} />
    </Suspense>
  );
}
