// Utility for communicating with the NES emulator RAM

export async function getRamContents() {
  const ram_contents_resource = await fetch('/symlinks/ramdisk/ram_contents.json');
  const ram_contents = await ram_contents_resource.json();
  return ram_contents;
}

export async function getRamValuesMap(addresses: string[]) {
  const ram_contents = await getRamContents();
  const values: Record<string, string> = {};

  addresses.forEach(address => {
    values[address] = ram_contents[address];
  });

  return values;
}