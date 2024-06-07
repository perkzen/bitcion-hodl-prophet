import { AuditLogTable } from '@/components/compositions/audit-log-table';

const DashboardPage = () => {
  return (
    <div className={'flex'}>
      <AuditLogTable />
    </div>
  );
};

export default DashboardPage;
