import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

import fr from './locales/fr/common.json'
import nl from './locales/nl/common.json'
import en from './locales/en/common.json'
import pl from './locales/pl/common.json'

const supportedLanguages = ['fr', 'nl', 'en', 'pl'] as const
type SupportedLanguage = (typeof supportedLanguages)[number]

const storedLanguage = localStorage.getItem('tooly_language')
const initialLanguage: SupportedLanguage = supportedLanguages.includes(storedLanguage as SupportedLanguage)
  ? (storedLanguage as SupportedLanguage)
  : 'fr'

void i18n.use(initReactI18next).init({
  resources: {
    fr: { translation: fr },
    nl: { translation: nl },
    en: { translation: en },
    pl: { translation: pl },
  },
  lng: initialLanguage,
  fallbackLng: 'fr',
  interpolation: { escapeValue: false },
})

export { supportedLanguages }
export default i18n
