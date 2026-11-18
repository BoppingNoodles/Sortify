import AsyncStorage from '@react-native-async-storage/async-storage';
import { randomUUID } from 'expo-crypto';
import { File } from 'expo-file-system';
import { ImageManipulator, SaveFormat } from 'expo-image-manipulator';
import { COLORS } from '../styles/theme';

const SCANS_STORAGE_KEY = '@sortify_saved_scans';
const DEVICE_UUID_KEY = '@sortify_device_uuid';
const WELCOME_KEY = '@sortify_guest_welcome';
export const HISTORY_LIMIT = 100;
const THUMBNAIL_SIZE = 96;
const MAX_THUMBNAIL_LENGTH = 12 * 1024;
const UUID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const BASE64_PATTERN = /^[A-Za-z0-9+/]+={0,2}$/;

export async function hasSeenWelcome() {
  return (await AsyncStorage.getItem(WELCOME_KEY).catch(() => null)) === 'seen';
}

export function markWelcomeSeen() {
  return AsyncStorage.setItem(WELCOME_KEY, 'seen');
}

let historyQueue = Promise.resolve();
let deviceInitialization;

function isUuid(value) {
  return typeof value === 'string' && UUID_PATTERN.test(value);
}

function isThumbnail(value) {
  return typeof value === 'string' &&
    value.length <= MAX_THUMBNAIL_LENGTH &&
    BASE64_PATTERN.test(value);
}

function discardThumbnailUri(uri) {
  try {
    if (uri?.startsWith('file://')) new File(uri).delete();
    if (uri?.startsWith('blob:')) URL.revokeObjectURL(uri);
  } catch (error) {
    console.warn('Could not discard temporary thumbnail.', error);
  }
}

async function createThumbnail(photo) {
  if (!photo?.uri) return undefined;
  let context;
  let image;
  let thumbnail;

  try {
    context = ImageManipulator.manipulate(photo.uri);
    const size = photo.height > photo.width
      ? { height: THUMBNAIL_SIZE }
      : { width: THUMBNAIL_SIZE };
    image = await context.resize(size).renderAsync();
    thumbnail = await image.saveAsync({
      format: SaveFormat.JPEG,
      compress: 0.6,
      base64: true,
    });
    if (isThumbnail(thumbnail.base64)) return thumbnail.base64;
  } catch (error) {
    console.warn('Could not create scan thumbnail.', error);
  } finally {
    discardThumbnailUri(thumbnail?.uri);
    discardThumbnailUri(image?.uri);
    image?.release();
    context?.release();
  }
}

function isScanMetadata(scan) {
  return scan != null &&
    typeof scan.item_name === 'string' &&
    typeof scan.category === 'string' &&
    Object.hasOwn(COLORS.bins, scan.category) &&
    Number.isFinite(scan.confidence) &&
    scan.confidence >= 0 &&
    scan.confidence <= 1 &&
    typeof scan.disposal_tip === 'string';
}

async function readHistory() {
  const raw = await AsyncStorage.getItem(SCANS_STORAGE_KEY);
  if (raw === null) return [];

  let records;
  try {
    records = JSON.parse(raw);
  } catch (error) {
    if (error instanceof SyntaxError) return [];
    throw error;
  }

  if (!Array.isArray(records)) return [];

  return records.filter((record) =>
    isScanMetadata(record) &&
    isUuid(record.id) &&
    typeof record.timestamp === 'string' &&
    new Date(record.timestamp).toJSON() === record.timestamp
  ).slice(0, HISTORY_LIMIT)
    .map(({ thumbnail, ...record }) =>
      isThumbnail(thumbnail) ? { ...record, thumbnail } : record
    );
}

function enqueueHistoryOperation(operation) {
  const pending = historyQueue.then(operation);
  historyQueue = pending.catch(() => {});
  return pending;
}

export function saveScanRecord(scanData, photo) {
  return enqueueHistoryOperation(async () => {
    if (!isScanMetadata(scanData)) return null;

    const existing = await readHistory();
    const { item_name, category, confidence, disposal_tip, location } = scanData;
    const record = {
      id: randomUUID(),
      timestamp: new Date().toISOString(),
      item_name,
      category,
      confidence,
      disposal_tip,
    };
    if (typeof location === 'string') record.location = location;
    const thumbnail = await createThumbnail(photo);
    if (thumbnail) record.thumbnail = thumbnail;

    const updated = [record, ...existing].slice(0, HISTORY_LIMIT);
    await AsyncStorage.setItem(SCANS_STORAGE_KEY, JSON.stringify(updated));
    return record;
  }).catch((error) => {
    console.warn('Could not save scan history.', error);
    return null;
  });
}

export function loadSavedScans() {
  return enqueueHistoryOperation(readHistory).catch((error) => {
    console.warn('Could not load scan history.', error);
    return [];
  });
}

export function clearHistory() {
  return enqueueHistoryOperation(async () => {
    await AsyncStorage.removeItem(SCANS_STORAGE_KEY);
    return true;
  }).catch((error) => {
    console.warn('Could not clear scan history.', error);
    return false;
  });
}

async function initializeDeviceUuid() {
  const storedUuid = await AsyncStorage.getItem(DEVICE_UUID_KEY);
  if (isUuid(storedUuid)) return storedUuid;

  const deviceUuid = randomUUID();
  await AsyncStorage.setItem(DEVICE_UUID_KEY, deviceUuid);
  return deviceUuid;
}

export function getOrCreateDeviceUuid() {
  deviceInitialization ??= initializeDeviceUuid()
    .catch((error) => {
      console.warn('Could not initialize device UUID.', error);
      return null;
    })
    .finally(() => {
      deviceInitialization = undefined;
    });
  return deviceInitialization;
}
