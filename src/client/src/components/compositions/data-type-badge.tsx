import { DataType } from '@/api';
import { Badge } from '@/components/ui/badge';

type DataTypeBadgeProps = {
  type: DataType;
};

const DataTypeBadge = ({ type }: DataTypeBadgeProps) => {
  const getLabel = (type: DataType) => {
    switch (type) {
      case DataType.DAILY:
        return 'Daily';
      case DataType.HOURLY:
        return 'Hourly';
      default:
        return 'Unknown';
    }
  };

  const getVariant = (type: DataType) => {
    switch (type) {
      case DataType.DAILY:
        return 'yellow';
      case DataType.HOURLY:
        return 'green';
      default:
        return 'default';
    }
  };

  return <Badge variant={getVariant(type)}>{getLabel(type)}</Badge>;
};

export default DataTypeBadge;
