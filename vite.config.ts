// https://vitejs.dev/config/
import { globSync } from 'glob'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'


// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    build: {
        minify: false,
        sourcemap: "inline",
        rollupOptions: {
            input: globSync("front/main/**/*.ts"),
            output: {
                dir: "out/front/",
                entryFileNames: "[name].js",
                assetFileNames: "assets/[name].[ext]",
                chunkFileNames: "chunks/[name].js",
            }
        }
    }
})
