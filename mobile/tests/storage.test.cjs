const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { test } = require('node:test');
const { loadSource } = require('./load-source.cjs');

const SCANS_KEY = '@sortify_saved_scans';
const DEVICE_KEY = '@sortify_device_uuid';
const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const scanData = {
  item_name: 'Bottle',
  category: 'plastic',
  confidence: 0.92,
  disposal_tip: 'Empty and rinse.',
  location: 'berkeley',
};

const mediaMocks = {
  'expo-file-system': { File: class File { delete() {} } },
  'expo-image-manipulator': {
    ImageManipulator: { manipulate() { throw new Error('unexpected thumbnail'); } },
    SaveFormat: { JPEG: 'jpeg' },
  },
};

function setup(t, data = new Map(), media = mediaMocks) {
  const storage = {
    getItem: t.mock.fn(async (key) => data.get(key) ?? null),
    setItem: t.mock.fn(async (key, value) => { data.set(key, value); }),
    removeItem: t.mock.fn(async (key) => { data.delete(key); }),
  };
  const generateUuid = t.mock.fn(randomUUID);
  const service = loadSource('src/services/storage.js', {
    '@react-native-async-storage/async-storage': storage,
    'expo-crypto': { randomUUID: generateUuid },
    ...media,
    '../styles/theme': loadSource('src/styles/theme.js'),
  }, { console: { warn() {} } });
  return { ...service, storage, data, generateUuid };
}

test('saves only scan metadata with a generated UUID and ISO timestamp', async (t) => {
  const app = setup(t);
  const record = await app.saveScanRecord({
    ...scanData,
    id: 'caller-id',
    timestamp: 'caller-time',
    photoUri: 'file:///camera/photo.jpg',
    alternatives: [],
  });

  assert.match(record.id, UUID_V4);
  assert.equal(record.timestamp, new Date(record.timestamp).toISOString());
  const expected = [{ id: record.id, timestamp: record.timestamp, ...scanData }];
  assert.deepEqual(JSON.parse(app.data.get(SCANS_KEY)), expected);
  assert.deepEqual(JSON.parse(JSON.stringify(await app.loadSavedScans())), expected);
  assert.equal(await app.saveScanRecord({ ...scanData, category: 'invalid' }), null);
  assert.equal(app.storage.setItem.mock.callCount(), 1);
});

test('stores a resized jpeg thumbnail and strips malformed thumbnail data', async (t) => {
  const deleted = [];
  const thumbnail = 'abc+/def=';
  const app = setup(t, new Map(), {
    'expo-file-system': {
      File: class File {
        constructor(uri) { this.uri = uri; }
        delete() { deleted.push(this.uri); }
      },
    },
    'expo-image-manipulator': {
      ImageManipulator: {
        manipulate(uri) {
          assert.equal(uri, 'file:///photo.jpg');
          return {
            resize(size) {
              assert.equal(size.width, 96);
              assert.equal(size.height, undefined);
              return this;
            },
            async renderAsync() {
              return {
                uri: 'file://rendered.jpg',
                release() {},
                async saveAsync(options) {
                  assert.equal(options.format, 'jpeg');
                  assert.equal(options.compress, 0.6);
                  assert.equal(options.base64, true);
                  return { uri: 'file://saved.jpg', base64: thumbnail };
                },
              };
            },
            release() {},
          };
        },
      },
      SaveFormat: { JPEG: 'jpeg' },
    },
  });

  const record = await app.saveScanRecord(scanData, {
    uri: 'file:///photo.jpg',
    width: 800,
    height: 600,
  });
  assert.equal(record.thumbnail, thumbnail);
  assert.deepEqual(deleted, ['file://saved.jpg', 'file://rendered.jpg']);

  const stored = JSON.parse(app.data.get(SCANS_KEY));
  stored[0].thumbnail = 'bad thumbnail!';
  app.data.set(SCANS_KEY, JSON.stringify(stored));
  const [loaded] = await app.loadSavedScans();
  assert.equal(loaded.thumbnail, undefined);
  assert.equal(loaded.item_name, scanData.item_name);
});

test('keeps exactly the newest 100 of 105 saves in insertion order', async (t) => {
  const { saveScanRecord, loadSavedScans, data } = setup(t);
  const ids = [];
  for (let number = 1; number <= 105; number++) {
    const record = await saveScanRecord({ ...scanData, item_name: String(number) });
    ids.push(record.id);
  }

  const saved = await loadSavedScans();
  assert.equal(new Set(ids).size, 105);
  assert.deepEqual(Array.from(saved, (scan) => Number(scan.item_name)),
    Array.from({ length: 100 }, (_, index) => 105 - index));
  assert.equal(JSON.parse(data.get(SCANS_KEY)).length, 100);
});

test('recovers missing, corrupt, and partially valid cache data', async (t) => {
  const app = setup(t);
  assert.equal((await app.loadSavedScans()).length, 0);
  for (const invalid of ['{', 'null', '{}', '"string"']) {
    app.data.set(SCANS_KEY, invalid);
    assert.equal((await app.loadSavedScans()).length, 0);
  }

  app.data.set(SCANS_KEY, '{');
  const previous = await app.saveScanRecord(scanData);
  app.data.set(SCANS_KEY, JSON.stringify([
    null,
    { ...previous, category: 'invalid' },
    { ...previous, timestamp: 'yesterday' },
    previous,
  ]));
  assert.deepEqual(Array.from(await app.loadSavedScans(), (scan) => scan.id), [previous.id]);

  const newest = await app.saveScanRecord(scanData);
  assert.deepEqual(JSON.parse(app.data.get(SCANS_KEY)).map((scan) => scan.id), [
    newest.id,
    previous.id,
  ]);
});

test('read, write and clear failures leave later operations usable', async (t) => {
  const app = setup(t);
  const original = await app.saveScanRecord(scanData);
  const dataBeforeFailure = app.data.get(SCANS_KEY);
  const reject = async () => { throw new Error('Storage unavailable'); };

  app.storage.getItem.mock.mockImplementationOnce(reject);
  assert.equal(await app.saveScanRecord(scanData), null);
  assert.equal(app.storage.setItem.mock.callCount(), 1);
  assert.equal(app.data.get(SCANS_KEY), dataBeforeFailure);

  app.storage.getItem.mock.mockImplementationOnce(reject);
  assert.equal((await app.loadSavedScans()).length, 0);

  app.storage.setItem.mock.mockImplementationOnce(reject);
  assert.equal(await app.saveScanRecord(scanData), null);

  app.storage.removeItem.mock.mockImplementationOnce(reject);
  assert.equal(await app.clearHistory(), false);
  assert.deepEqual(Array.from(await app.loadSavedScans(), (scan) => scan.id), [original.id]);

  const recovered = await app.saveScanRecord(scanData);
  assert.deepEqual(Array.from(await app.loadSavedScans(), (scan) => scan.id), [
    recovered.id, original.id,
  ]);
  assert.equal(await app.clearHistory(), true);
  assert.equal((await app.loadSavedScans()).length, 0);
});

test('serializes overlapping reads, saves, and clears while preserving the device UUID', async (t) => {
  const deviceId = randomUUID();
  const app = setup(t, new Map([[DEVICE_KEY, deviceId]]));
  const first = app.saveScanRecord({ ...scanData, item_name: 'First' });
  const second = app.saveScanRecord({ ...scanData, item_name: 'Second' });
  const beforeClear = app.loadSavedScans();
  const clear = app.clearHistory();
  const afterClear = app.loadSavedScans();
  const third = app.saveScanRecord({ ...scanData, item_name: 'Third' });

  const [firstScan, secondScan, snapshot, cleared, empty, thirdScan] = await Promise.all([
    first, second, beforeClear, clear, afterClear, third,
  ]);
  assert.deepEqual(Array.from(snapshot, (scan) => scan.id), [secondScan.id, firstScan.id]);
  assert.equal(cleared, true);
  assert.equal(empty.length, 0);
  assert.deepEqual(Array.from(await app.loadSavedScans(), (scan) => scan.id), [thirdScan.id]);
  assert.equal(app.data.get(DEVICE_KEY), deviceId);
});

test('guest UUID initialization is shared, survives reload, and differs on fresh storage', async (t) => {
  const app = setup(t);
  const first = app.getOrCreateDeviceUuid();
  assert.strictEqual(app.getOrCreateDeviceUuid(), first);
  const deviceId = await first;
  assert.match(deviceId, UUID_V4);
  assert.equal(app.storage.setItem.mock.callCount(), 1);
  assert.equal(app.data.get(DEVICE_KEY), deviceId);

  const reopened = setup(t, app.data);
  assert.equal(await reopened.getOrCreateDeviceUuid(), deviceId);
  assert.equal(reopened.generateUuid.mock.callCount(), 0);
  assert.notEqual(await setup(t).getOrCreateDeviceUuid(), deviceId);
});

test('replaces a malformed device UUID and retries after storage or generation failures', async (t) => {
  const app = setup(t, new Map([[DEVICE_KEY, 'fallback_device_uuid']]));
  const fail = () => { throw new Error('Device UUID unavailable'); };

  app.storage.getItem.mock.mockImplementationOnce(async () => fail());
  assert.equal(await app.getOrCreateDeviceUuid(), null);

  app.generateUuid.mock.mockImplementationOnce(fail);
  assert.equal(await app.getOrCreateDeviceUuid(), null);

  app.storage.setItem.mock.mockImplementationOnce(async () => fail());
  assert.equal(await app.getOrCreateDeviceUuid(), null);
  assert.equal(app.data.get(DEVICE_KEY), 'fallback_device_uuid');

  const recovered = await app.getOrCreateDeviceUuid();
  assert.match(recovered, UUID_V4);
  assert.equal(app.data.get(DEVICE_KEY), recovered);
});
