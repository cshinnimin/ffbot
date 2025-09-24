// Utility for communicating with the NES emulator RAM
import { RamContentsError, FlaskRamWriteError } from "../types/Error";
import type { RamCatLookup, RamCatNumberEntry, RamCatLookupEntry } from "../types/RamCatalog";

// Singleton promise for Ram Catalog Lookups
let ramCatalogLookupsPromise: Promise<Record<string, RamCatLookup>> | null = null;

// Singleton promise for Ram Catalog Entries
let ramCatalogEntriesPromise: Promise<Record<string, RamCatNumberEntry | RamCatLookupEntry>> | null = null;

/**
 * Private function to load and return the Ram Catalog Lookups as an object keyed by item.key.
 * Only loads once per page refresh.
 */
function getRamCatalogLookups(): Promise<Record<string, RamCatLookup>> {
  if (!ramCatalogLookupsPromise) {
    ramCatalogLookupsPromise = fetch('/symlinks/ramdisk/ram_catalog.json')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load ram_catalog.json');
        return res.json();
      })
      .then((ramCatalog) => {
        if (!ramCatalog.lookups || !Array.isArray(ramCatalog.lookups)) {
          throw new Error('ram_catalog.json missing lookups array');
        }

        const lookups: Record<string, RamCatLookup> = {};
        for (const item of ramCatalog.lookups) {
          lookups[item.key] = {
            default: item.default,
            map: item.map
          };
        }

        return lookups;
      });
  }
  return ramCatalogLookupsPromise;
}

/**
 * Private function to load and return the Ram Catalog Entries as an object keyed by item.address.
 * Only loads once per page refresh. Resolves lookups using the cached lookups object.
 */
function getRamCatalogEntries(): Promise<Record<string, RamCatNumberEntry | RamCatLookupEntry>> {
  if (!ramCatalogEntriesPromise) {
    ramCatalogEntriesPromise = fetch('/symlinks/ramdisk/ram_catalog.json')
      .then(res => {
        if (!res.ok) throw new Error('Failed to load ram_catalog.json');
        return res.json();
      })
      .then(async (ramCatalog) => {
        if (!ramCatalog.catalog || !Array.isArray(ramCatalog.catalog)) {
          throw new Error('ram_catalog.json missing catalog array');
        }

        const entries: Record<string, RamCatNumberEntry | RamCatLookupEntry> = {};

        // we need the lookups first so we can associate them 
        // to the relevant RamCatLookupEntry objects
        const lookups = await getRamCatalogLookups();

        for (const catalogEntry of ramCatalog.catalog) {
          if (catalogEntry.type === 'number') {
            // if catalogEntry.type is `number`, create a RamCatNumberEntry
            entries[catalogEntry.address] = {
              description: catalogEntry.description,
              weight: catalogEntry.weight
            };
          } else if (catalogEntry.type === 'lookup') {
            // if catalogEntry.type is `lookup`, create a RamCatLookupEntry
            const lookup = lookups[catalogEntry.lookup];
            if (!lookup) {
              throw new Error(`Lookup key '${catalogEntry.lookup}' not found in lookups`);
            }

            entries[catalogEntry.address] = {
              description: catalogEntry.description,
              lookup
            };
          }
        }

        return entries;
      });
  }
  return ramCatalogEntriesPromise;
}

// Private function to return ram contents. We cannot cache this as RAM is dynamic and
// we need it freshly read on every request.
async function getRamContents() {
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
  const RAM_CATALOG_ENTRIES = await getRamCatalogEntries();
  const values: Record<string, string> = {};

  try {
    addresses.forEach(address => {
      const rcLookupEntry = RAM_CATALOG_ENTRIES[address];
      if (!rcLookupEntry) {
        throw new RamContentsError('LLM requesting a RAM address not present in RAM Catalog.');
      }

      if ('lookup' in rcLookupEntry) {
        // is a RamCatLookupEntry
        const lookupVal = rcLookupEntry.lookup.map[ram_contents[address]];

        if (lookupVal !== undefined) {
          values[address] = lookupVal;
        } else {
          values[address] = rcLookupEntry.lookup.default;
        }
      } else if ('weight' in rcLookupEntry) {
        // is a RamCatNumberEntry
        const rawVal = parseInt(ram_contents[address], 16);
        const weight = parseInt(rcLookupEntry.weight as unknown as string, 10);
        values[address] = (rawVal * weight).toString();
      } else {
        throw new RamContentsError('RAM Catalog entry has unexpected format.');
      }
    });
  } catch (error) {
    throw new RamContentsError('Game memory not in expected format. Perhaps a RAM address I have been trained on is not available for lookup.');
  }

  return values;
}

export async function sendLuaScript(luaScript: string) {
  // Read port from VITE_FLASK_PORT in .env, default to 5000
  const port = import.meta.env.VITE_FLASK_PORT || '5000';

  const url = `http://localhost:${port}/write_ram`;
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