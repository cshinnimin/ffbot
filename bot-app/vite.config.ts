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
    },
    server: {
      hmr: false,
      proxy: {
        '/llm': {
          target: 'http://localhost:5001',
          changeOrigin: true,
          secure: false
        }
      }
    }
  };
});