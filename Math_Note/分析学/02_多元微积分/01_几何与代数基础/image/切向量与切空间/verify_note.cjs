// Usage: node verify_note.cjs <path-to-installed-katex-package>
const fs = require('node:fs');
const path = require('node:path');
const katex = require(path.resolve(process.argv[2]));
const note = path.resolve(__dirname, '../../.切向量与切空间.md.hidden');
const text = fs.readFileSync(note, 'utf8');
let count = 0;
const formula = /\$\$([\s\S]*?)\$\$|(?<![\\$])\$([^$\n]+)\$/g;
for (const match of text.matchAll(formula)) {
  const line = text.slice(0, match.index).split('\n').length;
  try {
    katex.renderToString(match[1] ?? match[2], {
      throwOnError: true, strict: 'error', trust: false,
      displayMode: match[1] !== undefined,
    });
  } catch (err) {
    throw new Error(`Line ${line}: ${err.message}`);
  }
  count++;
}
for (const match of text.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)) {
  const target = path.resolve(path.dirname(note), match[1]);
  if (!fs.existsSync(target)) throw new Error(`Missing target: ${target}`);
}
// A TeX row break may legally carry a spacing argument, e.g. \\[4pt].
const escapedDisplay = /\\\\\[(?!-?(?:\d+(?:\.\d*)?|\.\d+)(?:pt|em|ex|mm|cm|in)\])/;
if (text.includes('\\\\(') || escapedDisplay.test(text)) {
  throw new Error('Legacy escaped math delimiters remain.');
}
console.log(`KaTeX ${katex.version}: ${count} formulas passed strict parsing; all Markdown links exist.`);
