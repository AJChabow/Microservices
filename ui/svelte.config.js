import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import adapter from '@sveltejs/adapter-static';
/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	 kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: "index.html",
        strict: false,
    }),
    // Optional: Add any other necessary configurations here
  }
};

export default config;
