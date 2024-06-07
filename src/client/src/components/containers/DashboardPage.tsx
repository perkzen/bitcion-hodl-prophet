'use client';
import { AuditLogTable } from '@/components/compositions/audit-log-table';
import { useMetrics } from '@/api/hooks';
import MetricCard from '@/components/compositions/metric-card';

const DashboardPage = () => {
  const { data } = useMetrics();

  return (
    <div className={'flex flex-col gap-8'}>
      <div className={'grid grid-cols-4 gap-4'}>
        {data.map((metric, i) => {
          return <MetricCard metric={metric} key={i} />;
        })}
      </div>
      <AuditLogTable />
    </div>
  );
};

export default DashboardPage;
