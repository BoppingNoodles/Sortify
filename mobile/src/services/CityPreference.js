import React, { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MUNICIPALITIES } from './municipalities';

const CITY_KEY = '@sortify_city';
const DEFAULT_CITY = 'berkeley';
const CityPreference = createContext(null);

export function CityPreferenceProvider({ children }) {
  const [city, setCity] = useState(null);
  const writes = useRef(Promise.resolve());

  useEffect(() => {
    let active = true;
    AsyncStorage.getItem(CITY_KEY).then((stored) => {
      if (active && Object.hasOwn(MUNICIPALITIES, stored)) {
        setCity((current) => current ?? stored);
      }
    }).catch((error) => console.warn('Could not load sorting location.', error));
    return () => { active = false; };
  }, []);

  const selectCity = useCallback((nextCity) => {
    if (!Object.hasOwn(MUNICIPALITIES, nextCity)) return;
    setCity(nextCity);
    writes.current = writes.current.then(() => AsyncStorage.setItem(CITY_KEY, nextCity))
      .catch((error) => console.warn('Could not save sorting location.', error));
  }, []);

  return (
    <CityPreference.Provider value={[city ?? DEFAULT_CITY, selectCity]}>
      {children}
    </CityPreference.Provider>
  );
}

export function useCityPreference() {
  return useContext(CityPreference);
}
