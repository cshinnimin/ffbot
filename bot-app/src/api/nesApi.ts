// Utility for communicating with the NES emulator RAM

import { RamContentsError } from "../types/Error";

export async function getRamContents() {
  try {
    const ram_contents_resource = await fetch('/symlinks/ramdisk/ram_contents.json');
    const ram_contents = await ram_contents_resource.json();
    return ram_contents;
  } catch (error) {
    throw new RamContentsError('Access to game memory failed. Make sure LUA daemon is running.');
  }      
}

export async function getRamValuesMap(addresses: string[]) {
  const ram_contents = await getRamContents();
  const values: Record<string, string> = {};

  try {
    addresses.forEach(address => {
      values[address] = ram_contents[address];
    });
  } catch (error) {
    throw new RamContentsError('Game memory not in expected format.');
  }

  return values;
}