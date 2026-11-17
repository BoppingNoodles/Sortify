const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const babel = require('@babel/core');

// Exercise the actual Expo modules without loading native bindings in Node.
exports.loadSource = (relativePath, mocks = {}, globals = {}) => {
  const filename = path.resolve(__dirname, '..', relativePath);
  const { code } = babel.transformSync(fs.readFileSync(filename, 'utf8'), {
    filename,
    babelrc: false,
    configFile: false,
    plugins: [
      require.resolve('@babel/plugin-transform-modules-commonjs'),
      require.resolve('@babel/plugin-transform-react-jsx'),
    ],
  });
  const module = { exports: {} };
  vm.runInNewContext(code, {
    module,
    exports: module.exports,
    require: (name) => Object.hasOwn(mocks, name) ? mocks[name] : require(name),
    process: { env: { EXPO_PUBLIC_API_URL: 'http://test-api:8000/' } },
    console,
    fetch,
    FormData,
    AbortController,
    setTimeout,
    clearTimeout,
    ...globals,
  }, { filename });
  return module.exports;
};
