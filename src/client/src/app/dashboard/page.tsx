import {
  dehydrate,
  HydrationBoundary,
  QueryClient,
} from '@tanstack/react-query';
import DashboardPage from '@/components/containers/DashboardPage';
import { getAuditLogs, getMetrics } from '@/api';
import { AUDIT_LOG_QUERY_KEY, METRIC_QUERY_KEY } from '@/api/hooks';

const Dashboard = async () => {
  const queryClient = new QueryClient();

  await Promise.all([
    queryClient.prefetchQuery({
      queryFn: getAuditLogs,
      queryKey: [AUDIT_LOG_QUERY_KEY],
    }),
    queryClient.prefetchQuery({
      queryFn: getMetrics,
      queryKey: [METRIC_QUERY_KEY],
    }),
  ]);

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <DashboardPage />
    </HydrationBoundary>
  );
};

export default Dashboard;
