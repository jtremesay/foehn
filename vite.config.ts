import { defineConfig } from 'vite'
import { djangoVitePlugin } from 'django-vite-plugin'
import { globSync } from 'glob'

export default defineConfig({
    plugins: [
        djangoVitePlugin({
            input: [
                'foehn/static/foehn/js/main.ts',
                'foehn/static/foehn/css/main.scss',
                //...globSync('front/main/*.ts'),
            ]
        })
    ],
});
