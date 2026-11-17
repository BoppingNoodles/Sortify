const fs = require('node:fs');
const path = require('node:path');
const babel = require('@babel/core');

function check(file) {
  if (fs.statSync(file).isDirectory()) {
    for (const entry of fs.readdirSync(file)) check(path.join(file, entry));
  } else if (/\.(js|cjs)$/.test(file)) {
    babel.parseSync(fs.readFileSync(file, 'utf8'), {
      filename: file,
      babelrc: false,
      configFile: false,
      parserOpts: { sourceType: 'unambiguous', plugins: ['jsx'] },
    });
  }
}

for (const file of ['src', 'tests', 'scripts', 'App.js', 'index.js']) check(file);
console.log('Frontend JavaScript and JSX syntax checks passed.');
