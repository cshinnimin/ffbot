import { defineConfig, loadEnv } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  // Load env file from parent directory
  const env = loadEnv(mode, process.cwd() + "/..", '');
  
  return {
    envDir: "..",
    envPrefix: "VITE_",
    plugins: [tailwindcss(), react()],
    define: {
      // Explicitly define environment variables, this is required for the React app to access the
      // environment variables defined in the root project folder .env file where we are 
      // consolidating all environment variables for the project
      'import.meta.env.VITE_DEBUG_MODE': JSON.stringify(env.VITE_DEBUG_MODE),
      'import.meta.env.VITE_TRAINING_MAX_ATTEMPTS': JSON.stringify(env.VITE_TRAINING_MAX_ATTEMPTS),
      // Expose backend ports to the browser without requiring the VITE_ prefix in .env
      // (to avoid redundancy since these values are also needed by backend parts of the project)
      // Ports are safe to expose (not secrets) and will be injected at build/dev time
      'import.meta.env.NES_API_PORT': JSON.stringify(env.NES_API_PORT || '5000'),
      'import.meta.env.LLM_API_PORT': JSON.stringify(env.LLM_API_PORT || '5001'),
    },
    server: {
      port: parseInt(env.VITE_PORT || '5173'),
      hmr: false,
      proxy: {
        '/llm': {
          // Use LLM_API_PORT from the root .env (loaded above). Fall back to 5001 if not set.
          target: `http://localhost:${env.LLM_API_PORT || '5001'}`,
          changeOrigin: true,
          secure: false
        }
      }
    }
  };
});