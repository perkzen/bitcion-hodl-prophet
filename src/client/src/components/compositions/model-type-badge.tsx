import { ModelType } from '@/api';
import { Badge } from '@/components/ui/badge';

type ModelTypeBadgeProps = {
  type: ModelType;
};
const ModelTypeBadge = ({ type }: ModelTypeBadgeProps) => {
  const getLabel = (type: ModelType) => {
    switch (type) {
      case ModelType.REGRESSION:
        return 'Regression';
      case ModelType.CLASSIFICATION:
        return 'Classification';
      default:
        return 'Unknown';
    }
  };
  const getVariant = (type: ModelType) => {
    switch (type) {
      case ModelType.REGRESSION:
        return 'red';
      case ModelType.CLASSIFICATION:
        return 'blue';
      default:
        return 'default';
    }
  };

  return <Badge variant={getVariant(type)}>{getLabel(type)}</Badge>;
};

export default ModelTypeBadge;
