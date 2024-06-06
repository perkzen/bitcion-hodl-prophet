'use client';

import { PropsWithChildren, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppProgressBar } from 'next-nprogress-bar';

const Providers = ({ children }: PropsWithChildren) => {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
          },
        },
      })
  );
  return (
    <>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
      <AppProgressBar
        height="4px"
        color="#F6931D"
        options={{ showSpinner: false }}
        shallowRouting
      />
    </>
  );
};

export default Providers;
