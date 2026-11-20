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
  for (const [status, body, message] of [
    [413, { detail: 'Too large' }, /Too large/],
    [415, { error: true, code: 'INVALID_IMAGE_FORMAT', message: 'Unsupported or corrupted image file.' },
      /Unsupported or corrupted image file/],
    [415, null, /Unsupported image format/],
    [422, { detail: [{ msg: 'Expected an image file' }] }, /Expected an image file/],
    [422, { detail: { reason: 'invalid' } }, /Unprocessable image/],
  ]) {
    let requests = 0;
    const { classifyImage } = client('android', {
      fetch: async () => {
        requests++;
        return Response.json(body, { status });
      },
    });
    await assert.rejects(classifyImage('file:///photo.jpg'), message);
    assert.equal(requests, 1);
  }
});

test('the last backend message survives exhausted 5xx retries', async () => {
  let requests = 0;
  const message = 'Service temporarily unavailable. Please try again.';
  const { classifyImage } = client('android', {
    setTimeout: fastTimers,
    clearTimeout() {},
    fetch: async () => {
      requests++;
      return Response.json({ error: true, code: 'SERVICE_UNAVAILABLE', message }, { status: 503 });
    },
  });
  await assert.rejects(classifyImage('file:///photo.jpg'), { message });
  assert.equal(requests, 3);
});

test('municipal rules retain the shared retry handling', async () => {
  let requests = 0;
  const { fetchLocationRules } = client('android', {
    setTimeout: fastTimers,
    clearTimeout() {},
    fetch: async (url, options) => {
      assert.equal(url, 'http://test-api:8000/api/rules/san-francisco');
      assert.equal(options.method, 'GET');
      if (++requests === 1) return new Response('Temporarily unavailable', { status: 503 });
      return Response.json({ city: 'san-francisco', rules: {} });
    },
  });
  assert.deepEqual(await fetchLocationRules('san-francisco'), { city: 'san-francisco', rules: {} });
  assert.equal(requests, 2);
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

function abortError() {
  const error = new Error('aborted');
  error.name = 'AbortError';
  return error;
}

test('wakeServer waits through a slow cold start and then remembers the server is awake', async () => {
  const calls = [];
  const replies = [
    () => { throw abortError(); },
    () => Response.json({ detail: 'starting' }, { status: 503 }),
    () => Response.json({ status: 'ok' }),
  ];
  const { wakeServer, isServerAwake } = client('ios', {
    setTimeout: fastTimers,
    clearTimeout() {},
    fetch: async (url) => {
      calls.push(url);
      return replies[calls.length - 1]();
    },
  });
  assert.equal(isServerAwake(), false);
  const [first, second] = await Promise.all([wakeServer(), wakeServer()]);
  assert.equal(first, true);
  assert.equal(second, true);
  assert.equal(calls.length, 3);
  assert.ok(calls.every((url) => url === 'http://test-api:8000/health'));
  assert.equal(isServerAwake(), true);
  assert.equal(await wakeServer(), true);
  assert.equal(calls.length, 3);
});

test('wakeServer gives up quickly when the server is unreachable', async () => {
  let calls = 0;
  const { wakeServer, isServerAwake } = client('android', {
    setTimeout: fastTimers,
    clearTimeout() {},
    fetch: async () => { calls++; throw new TypeError('Network request failed'); },
  });
  assert.equal(await wakeServer(), false);
  assert.equal(calls, 3);
  assert.equal(isServerAwake(), false);
});

// Fake timers on a virtual clock: each timer advances the clock by its delay.
function virtualClock() {
  const clock = { now: 0 };
  clock.Date = { now: () => clock.now };
  clock.setTimeout = (callback, delay) => {
    clock.now += delay;
    queueMicrotask(callback);
    return 0;
  };
  return clock;
}

function hangUntilAborted(_url, { signal }) {
  return new Promise((_resolve, reject) => {
    signal.addEventListener('abort', () => reject(abortError()));
  });
}

test('wakeServer never runs past its 90 s deadline when the server never starts', async () => {
  const clock = virtualClock();
  // The fake clock advances when a timer is scheduled, so this records when each ping times out.
  const pingEnds = [];
  const { wakeServer } = client('android', {
    Date: clock.Date,
    setTimeout: clock.setTimeout,
    clearTimeout() {},
    fetch: (url, options) => { pingEnds.push(clock.now); return hangUntilAborted(url, options); },
  });
  assert.equal(await wakeServer(), false);
  assert.ok(clock.now <= 90000, `wake ended at ${clock.now} ms`);
  assert.ok(pingEnds.length >= 5);
  assert.ok(pingEnds.every((end) => end <= 90000), pingEnds.join(','));
});

test('a 200 page that is not the health response counts as still starting', async () => {
  const clock = virtualClock();
  let calls = 0;
  const { wakeServer, isServerAwake } = client('android', {
    Date: clock.Date,
    setTimeout: clock.setTimeout,
    clearTimeout() {},
    fetch: async () => {
      calls++;
      return calls < 3
        ? new Response('<html>Service waking up…</html>', { headers: { 'Content-Type': 'text/html' } })
        : Response.json({ status: 'ok' });
    },
  });
  assert.equal(await wakeServer(), true);
  assert.equal(calls, 3);
  assert.equal(isServerAwake(), true);
});

test('a successful API response marks the server awake without a health check', async () => {
  const urls = [];
  const { fetchLocationRules, wakeServer, isServerAwake } = client('android', {
    fetch: async (url) => { urls.push(url); return Response.json({ rules: [] }); },
  });
  await fetchLocationRules('oakland');
  assert.equal(isServerAwake(), true);
  assert.equal(await wakeServer(), true);
  assert.deepEqual(urls, ['http://test-api:8000/api/rules/oakland']);
});
