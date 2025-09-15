
import { useCallback } from 'react';

// Define the enum-like object for correction types
export const CorrectionType = {
  JSON_EXPECTED: 'SPELLING'
} as const;
type CorrectionType = typeof CorrectionType[keyof typeof CorrectionType];

// Map CorrectionType to string descriptions
const CORRECTION_MAP: Record<CorrectionType, string> = {
  [CorrectionType.JSON_EXPECTED]: 'JSON Expected'
};

export function useTraining() {
  const issueCorrection = useCallback((correction: CorrectionType) => {



    return CORRECTION_MAP[correction] || 'Unknown Correction';
  }, []);

  return { issueCorrection };
}
