'use client'

import { AlertTriangle, Shield, Brain, HeartPulse, Download, AlertCircle, X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface TriageResultProps {
  result: any
  onGenerateReport: (triageId: string, format: string, language: string) => Promise<void>
  onNewAnalysis: () => void
  language: string
}

const urgencyLabels = {
  emergency: 'EMERGENCY',
  urgent: 'URGENT',
  routine: 'ROUTINE',
  self_care: 'SELF CARE'
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

export function TriageResult({ result, onGenerateReport, onNewAnalysis, language }: TriageResultProps) {
  if (!result) return null

  const urgencyLabels = {
    emergency: 'EMERGENCY',
    urgent: 'URGENT',
    routine: 'ROUTINE',
    self_care: 'SELF CARE'
  }

  const getUrgencyColor = (level: string) => {
    switch (level) {
      case 'emergency': return 'bg-red-600 text-white animate-pulse'
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

  const handleGenerateReport = async (format: string) => {
    try {
      const response = await fetch('/api/v1/reports/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          triage_id: result.triage_id, 
          format,
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

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Urgency Banner */}
      <div className={cn('rounded-xl p-6 text-center', getUrgencyColor(result.urgency_level), 'animate-pulse')}>
        <div className="flex items-center justify-center gap-2 mb-2">
          <svg className="h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.177-.459-.76-.459-.936 0L3.32 19c-.398.565-.008 1.04.612.888l11.18 6.383a1 1 0 001.166 0l11.18-6.383c.62-.395.62-1.197 0-1.698L15.54 4.1a1 1 0 00-1.732 0L3.32 19c-.398.565-.008 1.04.612.888l11.18 6.383a1 1 0 001.166 0z" strokeWidth={2} stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <span className="text-3xl font-bold">{urgencyLabels[result.urgency_level as keyof typeof urgencyLabels] || result.urgency_level.toUpperCase()}</span>
        </div>
        <p className="text-lg font-medium">Confidence: {Math.round(result.confidence * 100)}%</p>
      </div>

      {/* Possible Conditions */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700">
        <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.548c0-.59-.348-1.13-.858-1.386z" />
          </svg>
          Possible Conditions
        </h4>
        <div className="space-y-3">
          {result.possible_conditions?.map((condition: any, idx: number) => (
            <div key={idx} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h5 className="font-semibold text-gray-900 dark:text-white">{condition.name}</h5>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{condition.description}</p>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">
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
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-5.986 5.986M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Recommended Action
        </h4>
        <p className="text-blue-800 dark:text-blue-200">{result.recommended_action}</p>
      </div>

      {/* Red Flags */}
      {result.red_flags && result.red_flags.length > 0 && (
        <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl p-6">
          <h4 className="text-lg font-bold text-red-900 dark:text-red-100 mb-3 flex items-center gap-2">
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.177-.459-.76-.459-.936 0L3.32 19c-.398.565-.008 1.04.612.888l11.18 6.383a1 1 0 001.166 0z" />
            </svg>
            Red Flags - Seek Immediate Care
          </h4>
          <ul className="space-y-2">
            {result.red_flags.map((flag: string, idx: number) => (
              <li key={idx} className="flex items-start gap-2 text-red-800 dark:text-red-200">
                <svg className="h-5 w-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.177-.459-.76-.459-.936 0L3.32 19c-.398.565-.008 1.04.612.888l11.18 6.383a1 1 0 001.166 0z" />
                </svg>
                <span>{flag}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Body Parts */}
      <div className="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-6">
        <h4 className="text-lg font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <svg className="h-5 w-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.5v15m7.5-7.5h-15" />
          </svg>
          Body Parts Involved
        </h4>
        <div className="flex flex-wrap gap-2">
          {result.body_parts_involved?.map((part: string, idx: number) => (
            <span key={idx} className="px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full text-sm font-medium">
              {part}
            </span>
          ))}
        </div>
      </div>

      {/* Follow-up Questions */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-gray-700">
        <h4 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.5-4 3-2.059.599-3.164 1.708-3.164 3.131 0 1.394.78 2.555 1.937 3.058" />
          </svg>
          Follow-up Questions for Your Doctor
        </h4>
        <div className="space-y-3">
          {result.follow_up_questions?.map((question: string, idx: number) => (
            <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
              <span className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-bold flex items-center justify-center">
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
          onClick={() => handleGenerateReport('pdf')}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors flex items-center gap-2"
        >
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Generate Report (PDF)
        </button>
        <button onClick={onNewAnalysis} className="px-6 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white font-semibold rounded-lg transition-colors">
          New Analysis
        </button>
      </div>
    </div>
  )
}

const urgencyLabels = {
  emergency: 'EMERGENCY',
  urgent: 'URGENT',
  routine: 'ROUTINE',
  self_care: 'SELF CARE'
}
