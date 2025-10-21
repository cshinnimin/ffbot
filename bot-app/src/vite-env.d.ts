/// <reference types="vite/client" />

interface ImportMetaEnv {
	// Exposed backend ports (injected via vite.config.ts define)
	readonly NES_API_PORT?: string;
	readonly LLM_API_PORT?: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
