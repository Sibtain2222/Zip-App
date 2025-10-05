import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',   // allow access from outside your PC
    port: 5173,        // frontend runs here
    allowedHosts: [
      'clerklike-seismological-tereasa.ngrok-free.dev'
    ],
    proxy: {
      '/api': 'http://localhost:8000'  // backend on Django
    }
  }
})
