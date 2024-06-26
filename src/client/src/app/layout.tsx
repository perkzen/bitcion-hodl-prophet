import { ReactNode } from 'react';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { cn } from '@/libs/utils';
import Navbar from '@/components/compositions/navbar';
import Providers from '@/components/providers/providers';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Bitcoin Hodl Prophet',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={cn(inter.className, 'bg-neutral-800')}>
        <Providers>
          <Navbar />
          <main className="flex w-full flex-col gap-8 sm:gap-20 px-2 sm:px-24 py-8">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
