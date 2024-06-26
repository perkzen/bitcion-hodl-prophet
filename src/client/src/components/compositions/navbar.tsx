'use client';
import Image from 'next/image';
import Bitcoin from '@/assets/Bitcoin.png';
import DataTypeSelect from '@/components/compositions/data-type-select';
import { Suspense } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Navbar = () => {
  const pathname = usePathname();

  return (
    <nav className="flex items-center justify-between gap-2 py-4 px-8 text-white bg-neutral-800 shadow-lg">
      <Link
        className={'flex items-center gap-2'}
        href={{
          pathname: '/',
        }}
      >
        <Image src={Bitcoin} alt={'Bitcoin'} width={48} height={48} />
        <h1 className="text-2xl font-bold hidden sm:block">
          Bitcoin Hodl Prophet
        </h1>
      </Link>

      <div className={'flex flex-row gap-4 items-center'}>
        {pathname === '/' && (
          <Suspense fallback={'Loading...'}>
            <DataTypeSelect />
          </Suspense>
        )}
        <Link
          className={'cursor-pointer'}
          href={{
            pathname: '/dashboard',
          }}
        >
          Dashboard
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
