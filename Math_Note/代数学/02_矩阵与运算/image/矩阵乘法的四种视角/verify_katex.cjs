// Usage: node verify_katex.cjs <directory containing the katex npm package>
// Install the pinned validator outside the notes tree:
// npm install --prefix <tools-directory> katex@0.16.22 --no-audit --no-fund
const fs = require('node:fs');
const path = require('node:path');
const katex = require(path.resolve(process.argv[2] || 'node_modules/katex'));
const groups = JSON.parse(fs.readFileSync(path.join(__dirname, 'figure_formulas.json'), 'utf8'));
let count = 0;
for (const [figure, formulas] of Object.entries(groups)) {
  for (const tex of formulas) {
    try {
      katex.renderToString(tex, {throwOnError: true, strict: 'error', displayMode: true, trust: false});
      count++;
    } catch (error) {
      throw new Error(`${figure}: ${tex}\n${error.message}`);
    }
  }
}
console.log(`KaTeX ${katex.version}: ${count} formulas passed strict parsing across ${Object.keys(groups).length} figures.`);
