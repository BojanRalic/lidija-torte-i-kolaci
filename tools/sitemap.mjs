// Builds sitemap.xml from the public .html pages; lastmod comes from each file's mtime.
// Run before every deploy: node tools/sitemap.mjs
import { readdirSync, statSync, writeFileSync } from 'node:fs';
const SITE = 'https://lidijatorteikolaci.rs/'; // change together with canonical tags once the domain is bought
const root = new URL('..', import.meta.url).pathname;
const pages = readdirSync(root).filter((f) => f.endsWith('.html') && f !== '404.html' && !f.startsWith('temp-'));
const urls = pages.map((f) => {
  const loc = SITE + (f === 'index.html' ? '' : f.replace(/\.html$/, ''));
  const lastmod = statSync(root + f).mtime.toISOString().slice(0, 10);
  return `  <url><loc>${loc}</loc><lastmod>${lastmod}</lastmod></url>`;
});
writeFileSync(root + 'sitemap.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join('\n')}\n</urlset>\n`);
console.log(`sitemap.xml: ${urls.length} url(s)`);
