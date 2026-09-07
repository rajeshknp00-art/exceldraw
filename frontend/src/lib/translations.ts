// Client-side translations (subset of backend translations)
export const translations = {
  en: {
    symptom_input_placeholder: "Describe your symptoms...",
    analyze_button: "Analyze Symptoms",
    urgency_emergency: "EMERGENCY",
    urgency_urgent: "URGENT",
    urgency_routine: "ROUTINE",
    urgency_self_care: "SELF CARE",
  },
  es: {
    symptom_input_placeholder: "Describe sus síntomas...",
    analyze_button: "Analizar Síntomas",
    urgency_emergency: "EMERGENCIA",
    urgency_urgent: "URGENTE",
    urgency_routine: "RUTINARIO",
    urgency_self_care: "AUTOCUIDADO",
  },
  fr: {
    symptom_input_placeholder: "Décrivez vos symptômes...",
    analyze_button: "Analyser les symptômes",
    urgency_emergency: "URGENCE",
    urgency_urgent: "URGENT",
    urgency_routine: "ROUTINIER",
    urgency_self_care: "AUTO-SOINS",
  },
  de: {
    symptom_input_placeholder: "Beschreiben Sie Ihre Symptome...",
    analyze_button: "Symptome analysieren",
    urgency_emergency: "NOTFALL",
    urgency_urgent: "DRINGEND",
    urgency_routine: "ROUTINE",
    urgency_self_care: "SELBSTPFLEGE",
  },
  zh: {
    symptom_input_placeholder: "描述您的症状...",
    analyze_button: "分析症状",
    urgency_emergency: "紧急",
    urgency_urgent: "急诊",
    urgency_routine: "常规",
    urgency_self_care: "自我护理",
  },
  hi: {
    symptom_input_placeholder: "अपने लक्षणों का वर्णन करें...",
    analyze_button: "लक्षणों का विश्लेषण करें",
    urgency_emergency: "आपातकाल",
    urgency_urgent: "तत्काल",
    urgency_routine: "नियमित",
    urgency_self_care: "स्व-देखभाल",
  }
}

export function getTranslation(language: string, key: string): string {
  const lang = language in translations ? language : 'en'
  return (translations as any)[lang]?.[key] || (translations.en as any)[key] || key
}

export const supportedLanguages = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Español' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'zh', name: '中文' },
  { code: 'hi', name: 'हिन्दी' }
]
