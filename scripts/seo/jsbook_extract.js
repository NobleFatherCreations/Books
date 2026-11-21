// Read MOVEMENTS / CH / BODIES out of a one-page book (data only, run in an empty sandbox) and print JSON.
const fs = require('fs'), vm = require('vm');
const h = fs.readFileSync(process.argv[2], 'utf8');
const s = h.indexOf('var MOVEMENTS');
const re = /BODIES\[\d+\]\s*=/g; let last = -1, m;
while ((m = re.exec(h))) last = m.index;
const t1 = h.indexOf('`', last), t2 = h.indexOf('`', t1 + 1);
const code = h.slice(s, t2 + 1) + ';';
const box = {};
vm.runInNewContext(code + '\nthis.__d={MOVEMENTS,CH,BODIES};', box, { timeout: 5000 });
process.stdout.write(JSON.stringify(box.__d));
