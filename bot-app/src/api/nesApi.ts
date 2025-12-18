// Utility for communicating with the NES emulator RAM
import { RamContentsError, FlaskRamWriteError } from "../types/Error";

export async function getRamValuesMap(addresses: string[]) {
  const port = import.meta.env.NES_API_PORT || '5000';
  const url = `http://localhost:${port}/nes/read`;

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ addresses }),
  });

  if (!response.ok) {
    // Attempt to extract backend error message if provided
    let errMsg = 'Game memory not in expected format. Perhaps a RAM address I have been trained on is not available for lookup.';

    try {
      const data = await response.json();
      if (data && data.error) errMsg = data.error;
    } catch (e) {
      // ignore JSON parse errors and use default message
    }

    throw new RamContentsError(errMsg);
  }

  const data = await response.json();
  
  return data.addresses as Record<string, string>;
}

export async function sendLuaScript(luaScript: string) {
  // Read port from .env, if not found, default to 5000
  const port = import.meta.env.NES_API_PORT || '5000';

  // updated route name in backend: write-lua
  const url = `http://localhost:${port}/nes/write-lua`;
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ lua_script: luaScript }),
  });

  if (!response.ok) {
    throw new FlaskRamWriteError('Failed to write Lua script.');
  }

  return response.ok;
}

export async function getMonstersByLocation(location: string) {
  const port = import.meta.env.NES_API_PORT || '5000';
  const url = `http://localhost:${port}/nes/bestiary/get-monsters-by-location`;

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location }),
  });

  if (!response.ok) {
    let errMsg = 'Failed to retrieve bestiary monsters for location.';
    try {
      const data = await response.json();
      if (data && data.error) errMsg = data.error;
    } catch (e) {}
    throw new Error(errMsg);
  }

  const data = await response.json();
  return data.monsters as string[];
}

export async function getLocationsByMonster(monsters: string[]) {
  const port = import.meta.env.NES_API_PORT || '5000';
  const url = `http://localhost:${port}/nes/bestiary/get-locations-by-monster`;

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ monsters }),
  });

  if (!response.ok) {
    let errMsg = 'Failed to retrieve bestiary locations for monsters.';
    try {
      const data = await response.json();
      if (data && data.error) errMsg = data.error;
    } catch (e) {}
    throw new Error(errMsg);
  }

  const data = await response.json();
  return data.locations as Record<string, string[]>;
}