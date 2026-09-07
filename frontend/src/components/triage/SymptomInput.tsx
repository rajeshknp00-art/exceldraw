'use client'

import { useState, useRef, useEffect } from 'react'
import { Mic, Send, Loader2, AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SymptomInputProps {
  onAnalyze: (symptoms: string, language: string) => Promise<void>
  isAnalyzing: boolean
  language: string
  onLanguageChange: (lang: string) => void
}

export function SymptomInput({ onAnalyze, isAnalyzing, language, onLanguageChange }: SymptomInputProps) {
  const [symptoms, setSymptoms] = useState('')
  const [error, setError] = useState<string | null>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  
  const handleVoiceInput = async () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Voice input not supported in this browser')
      return
    }
    
    const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)()
    recognition.lang = language
    recognition.interimResults = true
    recognition.continuous = false
    
    recognition.onstart = () => {
      setError(null)
    }
    
    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join('')
      setSymptoms(transcript)
    }
    
    recognition.onerror = (event) => {
      setError('Voice input failed: ' + event.error)
    }
    
    recognition.start()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!symptoms.trim()) return
    await onAnalyze(symptoms, language)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="symptoms" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Describe your symptoms in detail
        </label>
        <div className="relative">
          <textarea
            ref={textareaRef}
            id="symptoms"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            rows={5}
            className={cn(
              "w-full px-4 py-4 border border-gray-300 dark:border-gray-600 rounded-lg",
              "bg-white dark:bg-gray-900 text-gray-900 dark:text-white",
              "placeholder-gray-400 dark:placeholder-gray-500",
              "focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent",
              "resize-none"
            )}
            placeholder="Describe your symptoms in detail... (e.g., 'I have chest pain that started an hour ago. It feels like pressure in the center of my chest and radiates to my left arm.')"
          />
          <div className="absolute bottom-2 right-2 flex gap-2">
            <button
              type="button"
              onClick={handleVoiceInput}
              disabled={isAnalyzing}
              className="p-2 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded-lg hover:bg-primary-200 dark:hover:bg-primary-900/50 transition-colors disabled:opacity-50"
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
          <select value={language} onChange={(e) => onLanguageChange(e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500">
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
        type="submit"
        disabled={isAnalyzing || !symptoms.trim()}
        className="w-full py-4 bg-primary-600 hover:bg-primary-700 disabled:bg-primary-300 text-white font-semibold rounded-lg text-lg transition-colors flex items-center justify-center gap-2"
      >
        {isAnalyzing ? (
          <>
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Analyzing...
          </>
        ) : (
          <>
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.548c0-.59-.348-1.13-.858-1.386z" />
            </svg>
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
    </form>
  )
}
