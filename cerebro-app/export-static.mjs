// Exporta Cerebro Zamna como sitio estático para https://zamna.softvibes.art/cerebro/
// Uso: node export-static.mjs [--out ../sitio/cerebro]
import {promises as fs} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {buildGraph, htmlToText} from './build.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const arg = (n) => { const i = args.indexOf(n); return i < 0 ? undefined : args[i + 1]; };
const OUT = path.resolve(HERE, arg('--out') || '../sitio/cerebro');

const clean = (s) => s
  .replaceAll('/Users/rogergv/Documents/SoftvibesLab/SoftvibesSites/grupo-zamna-realty/', '')
  .replaceAll('/Users/rogergv/Documents/SoftvibesLab/', '')
  .replaceAll('/Users/rogergv/', '~/');
const noteName = (id) => id.replace(/[^A-Za-z0-9_-]/g, '-');
const version = createHash('sha256').update(await fs.readFile(path.join(HERE, 'dist/app.js'))).update(await fs.readFile(path.join(HERE, 'style.css'))).digest('hex').slice(0, 10);

await fs.rm(OUT, {recursive: true, force: true});
await fs.mkdir(path.join(OUT, 'dist'), {recursive: true});
await fs.mkdir(path.join(OUT, 'notes'), {recursive: true});

let html = await fs.readFile(path.join(HERE, 'index.html'), 'utf8');
html = html.replace('<head>', '<head>\n  <meta name="robots" content="noindex, nofollow" />')
  .replace('<script type="module" src="/dist/app.js"></script>', `<script>window.BRAIN_STATIC = true;</script>\n  <script type="module" src="dist/app.js?v=${version}"></script>`)
  .replace('href="/style.css"', `href="style.css?v=${version}"`);
if (!html.includes('BRAIN_STATIC')) throw new Error('No se pudo activar el modo estático en index.html');
await fs.writeFile(path.join(OUT, 'index.html'), html);
for (const f of ['style.css', 'dist/app.js', 'THIRD-PARTY-NOTICES.txt']) await fs.copyFile(path.join(HERE, f), path.join(OUT, f));

const {graph, records} = await buildGraph();
await fs.writeFile(path.join(OUT, 'graph.json'), clean(JSON.stringify(graph)));
const bodyByPath = new Map();
for (const r of records.values()) bodyByPath.set(r.node.relativePath, r.body || '');
let notes = 0;
for (const n of graph.nodes) {
  if (n.kind === 'index') continue;
  const markdown = bodyByPath.get(n.relativePath) || '';
  await fs.writeFile(path.join(OUT, 'notes', noteName(n.id) + '.json'), clean(JSON.stringify({id: n.id, markdown, path: n.path})));
  notes++;
}

const leaks = [];
for (const f of ['graph.json', 'index.html']) if (/\/Users\/rogergv/.test(await fs.readFile(path.join(OUT, f), 'utf8'))) leaks.push(f);
for (const f of await fs.readdir(path.join(OUT, 'notes'))) if (/\/Users\/rogergv/.test(await fs.readFile(path.join(OUT, 'notes', f), 'utf8'))) leaks.push('notes/' + f);
console.log(`Sitio estático: ${graph.nodes.length} nodos, ${notes} notas -> ${OUT}`);
if (leaks.length) { console.error('Rutas locales sin limpiar en:', leaks.slice(0, 10)); process.exitCode = 1; }
