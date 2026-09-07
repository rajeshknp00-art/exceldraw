import { useState, useCallback } from 'react'
import { triageAPI, reportsAPI } from '@/lib/api'

interface SymptomInput {
  symptoms: string
  language: string
  age?: number
  gender?: string
}

interface TriageResult {
  triage_id: string
  urgency_level: string
  confidence: number
  possible_conditions: Array<{
    name: string
    probability: number
    description: string
  }>
  recommended_action: string
  disclaimer: string
  body_parts_involved: string[]
  red_flags: string[]
  follow_up_questions: string[]
  created_at: string
}

export function useTriage() {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [isGeneratingReport, setIsGeneratingReport] = useState(false)

  const analyzeSymptoms = useCallback(async (symptoms: string, language: string) => {
    if (!symptoms.trim()) return
    
    setIsAnalyzing(true)
    setError(null)
    
    try {
      const response = await triageAPI.analyze({ symptoms, language })
      if (response.data.success) {
        setResult(response.data.data)
      } else {
        setError(response.data.error || 'Analysis failed')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze symptoms. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }, [])

  const generateReport = useCallback(async (triageId: string, format: string = 'pdf', language: string = 'en') => {
    setIsGeneratingReport(true)
    try {
      const response = await reportsAPI.generate({ triage_id: triageId, format, language })
      if (response.data.success && response.data.download_url) {
        window.open(response.data.download_url, '_blank')
      }
    } catch (err) {
      console.error('Report generation failed:', err)
    } finally {
      setIsGeneratingReport(false)
    }
  }, [])

  const reset = useCallback(() => {
    setResult(null)
    setError(null)
  }, [])

  return {
    isAnalyzing,
    result,
    error,
    isGeneratingReport,
    analyzeSymptoms,
    generateReport,
    reset,
  }
}
