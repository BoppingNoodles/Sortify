const assert = require('node:assert/strict');
const { test } = require('node:test');
const { loadSource } = require('./load-source.cjs');

function client(os, globals) {
  return loadSource('src/services/api.js', {
    'react-native': { Platform: { OS: os, select: (values) => values[os] || values.default } },
  }, globals);
}

function fastTimers(callback, delay) {
  if (delay < 12000) queueMicrotask(callback);
  return 0;
}

test('web uploads image bytes with a bounded MIME-matched filename and location', async () => {
  const uri = `data:image/png;base64,${'A'.repeat(5000)}`;
  const payload = { item_name: 'Bottle', category: 'plastic', confidence: 0.9 };
  let requests = 0;
  const { classifyImage, API_BASE_URL } = client('web', {
    fetch: async (url, options) => {
      requests++;
      if (url === uri) return new Response(new Blob(['image bytes'], { type: 'image/png' }));
      assert.equal(url, 'http://test-api:8000/api/classify?location=san-francisco');
      const file = options.body.get('file');
      assert.equal(file.name, 'photo.png');
      assert.equal(file.type, 'image/png');
      assert.equal(await file.text(), 'image bytes');
      assert.equal(options.headers['Content-Type'], undefined);
      return Response.json(payload);
    },
  });
  assert.equal(API_BASE_URL, 'http://test-api:8000');
  assert.deepEqual(await classifyImage(uri, 'san-francisco'), payload);
  assert.equal(requests, 2);
});

test('web photo conversion errors stop before a malformed API upload', async () => {
  for (const result of [null, new Response('', { status: 404 }), new Response(new Blob([]))]) {
    let requests = 0;
    const { classifyImage } = client('web', {
      fetch: async () => {
        requests++;
        if (!result) throw new Error('Unreadable photo');
        return result;
      },
    });
    await assert.rejects(classifyImage('blob:photo'), /Could not read captured photo/);
    assert.equal(requests, 1);
  }
});

test('native upload retries transient errors using fresh multipart bodies', async () => {
  const bodies = [];
  class NativeFormData {
    append(name, value) { this[name] = value; }
  }
  const { classifyImage } = client('android', {
    FormData: NativeFormData,
    setTimeout: fastTimers,
    clearTimeout() {},
    fetch: async (url, options) => {
      bodies.push(options.body);
      if (bodies.length === 1) throw new TypeError('Network disconnected');
      if (bodies.length === 2) return Response.json({ detail: 'Busy' }, { status: 503 });
      return Response.json({ item_name: 'Bottle' });
    },
  });
  await classifyImage('file:///photo.jpg');
  assert.equal(bodies.length, 3);
  assert.equal(new Set(bodies).size, 3);
  assert.equal(bodies[0].file.uri, 'file:///photo.jpg');
  assert.equal(bodies[0].file.type, 'image/jpeg');
});

test('4xx errors are readable and never retried', async () => {
  for (const [status, detail, message] of [
    [413, 'Too large', /Too large/],
    [415, undefined, /Unsupported image format/],
    [422, [{ msg: 'Expected an image file' }], /Expected an image file/],
    [422, { reason: 'invalid' }, /Unprocessable image/],
  ]) {
    let requests = 0;
    const { classifyImage } = client('android', {
      fetch: async () => {
        requests++;
        return Response.json({ detail }, { status });
      },
    });
    await assert.rejects(classifyImage('file:///photo.jpg'), message);
    assert.equal(requests, 1);
  }
});

test('aborted requests exhaust retries with a friendly timeout error', async () => {
  let requests = 0;
  const { classifyImage } = client('android', {
    setTimeout: (callback) => { queueMicrotask(callback); return 0; },
    clearTimeout() {},
    fetch: async (url, options) => {
      requests++;
      return new Promise((resolve, reject) => {
        options.signal.addEventListener('abort', () => reject(new DOMException('Aborted', 'AbortError')));
      });
    },
  });
  await assert.rejects(classifyImage('file:///photo.jpg'), /timed out/);
  assert.equal(requests, 3);
});
