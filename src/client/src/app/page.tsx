import { DataType } from '@/libs/api';
import HomePage from '@/components/containers/HomePage';
import { Suspense } from 'react';

export const dynamic = 'force-dynamic';
export const revalidate = 0;

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
