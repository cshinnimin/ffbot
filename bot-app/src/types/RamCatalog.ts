export type RamCatLookup = {
  default: string;
  map: Record<string, string>;
};

export type RamCatNumberEntry = {
  description: string;
  weight: number;
};

export type RamCatLookupEntry = {
  description: string;
  lookup: RamCatLookup;
};
