'use client'

import { useState } from 'react'
import { Mic, Send, AlertTriangle, Loader2, Download, Languages, Shield, Brain, HeartPulse } from 'lucide-react'
import { useTranslation } from '@/hooks/useTranslation'

export default function HomePage() {
  const [symptoms, setSymptoms] = useState('')
  const [language, setLanguage] = useState('en')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const { t, languages } = useTranslation()

  const handleAnalyze = async () => {
    if (!symptoms.trim()) return
    
    setIsAnalyzing(true)
    setError(null)
    
    try {
      const response = await fetch('/api/v1/triage/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms, language })
      })
      
      const data = await response.json()
      
      if (data.success) {
        setResult(data.data)
      } else {
        setError(data.error || 'Analysis failed')
      }
    } catch (err) {
      setError('Failed to analyze symptoms. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleVoiceInput = async () => {
    // Mock voice input - would use Web Speech API
    setSymptoms('I have chest pain that started an hour ago. It feels like pressure in the center of my chest.')
  }

  const handleGenerateReport = async () => {
    if (!result) return
    
    try {
      const response = await fetch('/api/v1/reports/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          triage_id: result.triage_id, 
          format: 'pdf',
          language: language
        })
      })
      
      const data = await response.json()
      if (data.success && data.download_url) {
        window.open(data.download_url, '_blank')
      }
    } catch (err) {
      console.error('Report generation failed:', err)
    }
  }

  const getUrgencyColor = (level: string) => {
    switch (level) {
      case 'emergency': return 'bg-medical-red text-white'
      case 'urgent': return 'bg-medical-orange text-white'
      case 'routine': return 'bg-medical-amber text-white'
      case 'self_care': return 'bg-medical-green text-white'
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
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white dark:from-gray-900 dark:to-gray-950">
      {/* Header */}
      <header className="border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <HeartPulse className="h-8 w-8 text-primary-600" />
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
                <Shield className="h-4 w-4" />
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
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
              <Brain className="h-4 w-4" />
              <span>RAG Medical Guidelines</span>
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-medical-green/10 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-sm font-medium">
              <Shield className="h-4 w-4" />
              <span>Guardrails Protected</span>
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-medical-amber/10 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded-full text-sm font-medium">
              <Languages className="h-4 w-4" />
              <span>6 Languages</span>
            </span>
            <span className="inline-flex items-center gap-2 px-4 py-2 bg-medical-red/10 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-full text-sm font-medium">
              <HeartPulse className="h-4 w-4" />
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
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="symptoms" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Describe your symptoms in detail
                  </label>
                  <div className="relative">
                    <textarea
                      id="symptoms"
                      value={symptoms}
                      onChange={(e) => setSymptoms(e.target.value)}
                      rows={5}
                      className="w-full px-4 py-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                      placeholder="Describe your symptoms in detail... (e.g., 'I have chest pain that started an hour ago. It feels like pressure in the center of my chest and radiates to my left arm.')"
                    />
                    <div className="absolute bottom-2 right-2 flex gap-2">
                      <button
                        onClick={handleVoiceInput}
                        disabled={isAnalyzing}
                        className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors"
                        aria-label="Voice input"
                      >
                        <Mic className="h-5 w-5" />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Age</label>
                    <input type="number" min="0" max="120" className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500" placeholder="Optional" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Gender</label>
                    <select className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option value="">Select</option>
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Language</label>
                    <select value={language} onChange={(e) => setLanguage(e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500">
                      <option value="en">English</option>
                      <option value="es">Español</option>
                      <option value="fr">Français</option>
                      <option value="de">Deutsch</option>
                      <option value="zh">中文</option>
                      <option value="hi">हिन्दी</option>
                    </select>
                  </div>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing || !symptoms.trim()}
                  className="w-full py-4 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 text-white font-semibold rounded-lg text-lg transition-colors flex items-center justify-center gap-2"
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Brain className="h-5 w-5" />
                      Analyze Symptoms
                    </>
                  )}
                </button>

                {error && (
                  <div className="p-4 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300">
                    <p className="font-medium">Error</p>
                    <p className="text-sm mt-1">{error}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </section>

        {/* Results */}
        {result && (
          <section className="mb-12">
            <div className="max-w-3xl mx-auto space-y-6">
              {/* Urgency Banner */}
              <div className={`rounded-xl p-6 text-center ${getUrgencyColor(result.urgency_level)} animate-pulse`}>
                <div className="flex items-center justify-center gap-2 mb-2">
                  <AlertTriangle className="h-8 w-8" />
                  <span className="text-3xl font-bold">{urgencyLabels[result.urgency_level as keyof typeof urgencyLabels] || result.urgency_level.toUpperCase()}</span>
                  <AlertTriangle className="h-8 w-8" />
                </div>
                <p className="text-lg font-medium">Confidence: {Math.round(result.confidence * 100)}%</p>
              </div>

              {/* Possible Conditions */}
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700">
                <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <Brain className="h-5 w-5 text-primary-600" />
                  Possible Conditions
                </h4>
                <div className="space-y-3">
                  {result.possible_conditions.map((condition: any, idx: number) => (
                    <div key={idx} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <h5 className="font-semibold text-gray-900 dark:text-white">{condition.name}</h5>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{condition.description}</p>
                        </div>
                        <div className="text-right">
                          <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                            {Math.round(condition.probability * 100)}%
                          </span>
                          <p className="text-xs text-gray-500 dark:text-gray-400">probability</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommended Action */}
              <div className="bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
                <h4 className="text-lg font-bold text-blue-900 dark:text-blue-100 mb-2 flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  Recommended Action
                </h4>
                <p className="text-blue-800 dark:text-blue-200">{result.recommended_action}</p>
              </div>

              {/* Red Flags */}
              {result.red_flags.length > 0 && (
                <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl p-6">
                  <h4 className="text-lg font-bold text-red-900 dark:text-red-100 mb-3 flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5" />
                    Red Flags - Seek Immediate Care
                  </h4>
                  <ul className="space-y-2">
                    {result.red_flags.map((flag: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2 text-red-800 dark:text-red-200">
                        <AlertTriangle className="h-5 w-5 flex-shrink-0" />
                        <span>{flag}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Body Parts */}
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-6">
                <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                  <HeartPulse className="h-5 w-5 text-red-600" />
                  Body Parts Involved
                </h4>
                <div className="flex flex-wrap gap-2">
                  {result.body_parts_involved.map((part: string, idx: number) => (
                    <span key={idx} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
                      {part}
                    </span>
                  ))}
                </div>
              </div>

              {/* Follow-up Questions */}
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700">
                <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                  <Brain className="h-5 w-5 text-primary-600" />
                  Follow-up Questions for Your Doctor
                </h4>
                <div className="space-y-3">
                  {result.follow_up_questions.map((question: string, idx: number) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-xs font-bold flex items-center justify-center">
                        {idx + 1}
                      </span>
                      <p className="text-gray-700 dark:text-gray-300 text-sm">{question}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Disclaimer */}
              <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-6 border border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-600 dark:text-gray-400">{result.disclaimer}</p>
              </div>

              {/* Actions */}
              <div className="flex flex-wrap gap-4 justify-center">
                <button
                  onClick={handleGenerateReport}
                  className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
                >
                  <Download className="h-5 w-5" />
                  Generate Report (PDF)
                </button>
                <button className="px-6 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-semibold rounded-lg transition-colors">
                  New Analysis
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Features Grid */}
        <section className="mb-12">
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">GenAI Techniques Integrated</h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {[
              { icon: Mic, title: 'Voice AI', desc: 'STT + TTS for accessible symptom input in 6 languages', color: 'bg-medical-red/10' },
              { icon: Brain, title: 'RAG Pipeline', desc: 'Medical guidelines vector DB with hybrid search & citations', color: 'bg-primary-100' },
              { icon: Shield, title: 'Guardrails', desc: 'No diagnosis, PII redaction, liability disclaimers', color: 'bg-medical-green/10' },
              { icon: Languages, title: 'Multi-language', desc: '6 languages: EN, ES, FR, DE, ZH, HI with RTL support', color: 'bg-medical-amber/10' },
              { icon: Brain, title: 'Knowledge Graph', desc: 'Medical entity relationships (symptoms, conditions, medications)', color: 'bg-purple-100' },
              { icon: HeartPulse, title: 'Content Generation', desc: 'Triage report generation (PDF/HTML/Text) with citations', color: 'bg-medical-red/10' },
            ].map((feature, idx) => (
              <div key={idx} className={`rounded-2xl p-6 border border-gray-200 dark:border-gray-700 ${feature.color} dark:opacity-80`}>
                <feature.icon className="h-8 w-8 text-primary-600 dark:text-primary-400 mb-3" />
                <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{feature.title}</feature.icon>
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
                  <Brain className="h-5 w-5 text-primary-600" />
                  {stack.category}
                </h4>
                <div className="flex flex-wrap gap-2">
                  {stack.tech.map((t, i) => (
                    <span key={i} className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-full text-sm font-medium">
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
