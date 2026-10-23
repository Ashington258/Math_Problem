// Usage: node tools/check_formulas.cjs <path-to-installed-katex-package>
const fs = require('node:fs');
const path = require('node:path');
const katex = require(path.resolve(process.argv[2]));
const root = path.resolve(__dirname, '..');
const historical = new Set(['切向量与切空间', '切向量与切线']);
const errors = [];
let files = 0, formulas = 0;
function visit(dir) {
  for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
    if (entry.name.startsWith('.') || historical.has(entry.name)) continue;
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) { visit(file); continue; }
    if (!entry.name.endsWith('.md')) continue;
    const text = fs.readFileSync(file, 'utf8');
    files++;
    const expression = /\$\$([\s\S]*?)\$\$|(?<![\\$])\$([^$\n]+)\$/g;
    for (const match of text.matchAll(expression)) {
      formulas++;
      try {
        katex.renderToString(match[1] ?? match[2], {
          throwOnError: true, strict: 'error', trust: false,
          displayMode: match[1] !== undefined,
        });
      } catch (error) {
        errors.push({file: path.relative(root, file),
          line: text.slice(0, match.index).split('\n').length, message: error.message});
      }
    }
  }
}
visit(root);
console.log(JSON.stringify({katex: katex.version, files, formulas, errors}, null, 2));
process.exitCode = errors.length ? 1 : 0;
