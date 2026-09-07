import { useState, useEffect } from 'react'
import { getTranslation, getSupportedLanguages } from '@/lib/translations'

type Language = 'en' | 'es' | 'fr' | 'de' | 'zh' | 'hi'

export function useTranslation(language?: string) {
  const [lang, setLang] = useState<Language>(language || 'en')
  
  const t = (key: string): string => {
    // This would be replaced with actual translation logic
    // For now, return the key as fallback
    return key
  }
  
  const languages = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
    { code: 'de', name: 'Deutsch' },
    { code: 'zh', name: '中文' },
    { code: 'hi', name: 'हिन्दी' }
  ]
  
  return { t, language: lang, setLanguage: setLang, languages }
}
