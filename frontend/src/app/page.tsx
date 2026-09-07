'use client'

import { useState } from 'react'
import { HeartPulse, Brain, Shield, Languages, Mic, Download, AlertTriangle, Loader2 } from 'lucide-react'
import { SymptomInput } from '@/components/triage/SymptomInput'
import { TriageResult } from '@/components/triage/TriageResult'
import { useTriage } from '@/hooks/useTriage'
import { getTranslation, supportedLanguages } from '@/lib/translations'

export default function HomePage() {
  const { isAnalyzing, result, error, isGeneratingReport, analyzeSymptoms, generateReport, reset } = useTriage()
  const [language, setLanguage] = useState('en')
  
  const handleAnalyze = async (symptoms: string, lang: string) => {
    await analyzeSymptoms(symptoms, lang)
  }
  
  const handleGenerateReport = async (format: string) => {
    if (result?.triage_id) {
      await generateReport(result.triage_id, format, language)
    }
  }
  
  const handleNewAnalysis = () => {
    reset()
  }

  const getUrgencyColor = (level: string) => {
    switch (level) {
      case 'emergency': return 'bg-red-600 text-white'
      case 'urgent': return 'bg-orange-600 text-white'
      case 'routine': return 'bg-amber-600 text-white'
      case 'self_care': return 'bg-green-600 text-white'
      default: return 'bg-gray-500 text-white'
    }
  }

  const urgencyLabels = {
    emergency: 'EMERGENCY',
    urgent: 'URGENT',
    routine: 'ROUTINE',
    self_care: 'SELF CARE'
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-950">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <svg className="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">Healthcare AI Triage</h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">AI-powered symptom analysis</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-sm"
              >
                {[
                  { code: 'en', name: 'English' },
                  { code: 'es', name: 'Español' },
                  { code: 'fr', name: 'Français' },
                  { code: 'de', name: 'Deutsch' },
                  { code: 'zh', name: '中文' },
                  { code: 'hi', name: 'हिन्दी' }
                ].map(lang => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
              <div className="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-5.986 5.986M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>HIPAA Ready</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <section className="mb-12">
          <div className="text-center mb-8">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              AI-Powered Health Triage
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Describe your symptoms in natural language or use voice input. Our AI analyzes your symptoms using medical guidelines and provides evidence-based triage recommendations.
            </p>
          </div>

          {/* Feature Badges */}
          <div className="flex flex-wrap justify-center gap-3 mb-8">
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.548c0-.59-.348-1.13-.858-1.386z" />
              </svg>
              <span>RAG Medical Guidelines</span>
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-sm font-medium">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-5.986 5.986M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <span>Guardrails Protected</span>
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded-full text-sm font-medium">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 114 0 2 2 0 01-4 0zM1.105 6.553A9.044 9.044 0 0112 5.4a9.044 9.044 0 008.588 5.598" />
              </svg>
              <span>6 Languages</span>
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-full text-sm font-medium">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              <span>Voice Input</span>
            </span>
          </div>
        </section>

        {/* Symptom Input */}
        <section className="mb-12">
          <div className="max-w-3xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
                Describe Your Symptoms
              </h3>
              
              <SymptomInput
                onAnalyze={handleAnalyze}
                isAnalyzing={isAnalyzing}
                language={language}
                onLanguageChange={setLanguage}
              />
              
              {error && (
                <div className="p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300">
                  <p className="font-medium">Error</p>
                  <p className="text-sm mt-1">{error}</p>
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Results */}
        {result && (
          <section className="mb-12">
            <TriageResult
              result={result}
              onGenerateReport={handleGenerateReport}
              onNewAnalysis={handleNewAnalysis}
              language={language}
            />
          </section>
        )}

        {/* Features Grid */}
        <section className="mb-12">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">GenAI Techniques Integrated</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              { icon: '🎤', title: 'Voice AI', desc: 'STT + TTS for accessible symptom input in 6 languages', color: 'bg-red-100' },
              { icon: '🧠', title: 'RAG Pipeline', desc: 'Medical guidelines vector DB with hybrid search & citations', color: 'bg-blue-100' },
              { icon: '🛡️', title: 'Guardrails', desc: 'No diagnosis, PII redaction, liability disclaimers', color: 'bg-green-100' },
              { icon: '🌐', title: 'Multi-language', desc: '6 languages: EN, ES, FR, DE, ZH, HI with RTL support', color: 'bg-amber-100' },
              { icon: '🔗', title: 'Knowledge Graph', desc: 'Medical entity relationships (symptoms, conditions, medications)', color: 'bg-purple-100' },
              { icon: '📄', title: 'Content Generation', desc: 'Triage report generation (PDF/HTML/Text) with citations', color: 'bg-red-100' },
            ].map((feature, idx) => (
              <div key={idx} className={`rounded-2xl p-6 border border-gray-200 dark:border-gray-700 ${feature.color} dark:opacity-80`}>
                <span className="text-3xl mb-3">{feature.icon}</span>
                <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{feature.title}</h4>
                <p className="text-gray-600 dark:text-gray-400 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Tech Stack */}
        <section className="mb-12">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">Tech Stack</h3>
          <div className="grid md:grid-cols-4 gap-4 max-w-5xl mx-auto">
            {[
              { category: 'Frontend', tech: ['Next.js 14', 'React 18', 'Tailwind CSS', 'shadcn/ui', 'TypeScript'] },
              { category: 'Backend', tech: ['FastAPI', 'Python 3.11', 'PostgreSQL', 'Redis', 'JWT Auth'] },
              { category: 'AI/ML', tech: ['OpenAI Whisper', 'Edge TTS', 'Milvus', 'pgvector', 'NetworkX'] },
              { category: 'DevOps', tech: ['Docker', 'Docker Compose', 'GitHub Actions', 'Prometheus', 'Grafana'] },
            ].map((stack, idx) => (
              <div key={idx} className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700">
                <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.548c0-.59-.348-1.13-.858-1.386z" />
                  </svg>
                  {stack.category}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {stack.tech.map((t, i) => (
                    <span key={i} className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Disclaimer Footer */}
        <footer className="border-t border-gray-200 dark:border-gray-700 pt-8 pb-4">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center max-w-3xl mx-auto">
            <strong>Disclaimer:</strong> This is an AI-powered triage assistant for informational purposes only. 
            It does NOT provide medical diagnosis, treatment recommendations, or replace professional medical advice. 
            Always consult a qualified healthcare provider for medical concerns. 
            In case of emergency, call emergency services immediately.
          </p>
          <div className="flex justify-center gap-6 mt-4 text-sm text-gray-500 dark:text-gray-400">
            <span>Built with Next.js 14 + FastAPI</span>
            <span>6 GenAI Techniques</span>
            <span>6 Languages Supported</span>
            <span>Docker Ready</span>
          </div>
        </footer>
      </main>
    </div>
  )
}

const urgencyLabels = {
  emergency: 'EMERGENCY',
  urgent: 'URGENT',
  routine: 'ROUTINE',
  self_care: 'SELF CARE'
}
