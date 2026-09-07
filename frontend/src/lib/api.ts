import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken
          })
          const { access_token, refresh_token } = response.data
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        }
      } catch (err) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/auth/login'
      }
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data: { email: string; password: string; full_name?: string; preferred_language?: string }) =>
    api.post('/auth/register', data),
  login: (email: string, password: string) =>
    api.post('/auth/login', { username: email, password }),
  refresh: (refresh_token: string) =>
    api.post('/auth/refresh', { refresh_token }),
  logout: (refresh_token: string) =>
    api.post('/auth/logout', { refresh_token }),
  me: () => api.get('/auth/me'),
}

export const triageAPI = {
  analyze: (data: { symptoms: string; language: string; age?: number; gender?: string }) =>
    api.post('/triage/analyze', data),
  history: (patientId: string) =>
    api.get(`/triage/history/${patientId}`),
  getResult: (triageId: string) =>
    api.get(`/triage/${triageId}`),
}

export const reportsAPI = {
  generate: (data: { triage_id: string; format?: string; language?: string }) =>
    api.post('/reports/generate', data),
  download: (reportId: string) =>
    api.get(`/reports/download/${reportId}`),
  templates: () =>
    api.get('/reports/templates'),
}

export const guidelinesAPI = {
  search: (query: string, limit: number = 10) =>
    api.get('/guidelines/search', { params: { q: query, limit } }),
  get: (guidelineId: string) =>
    api.get(`/guidelines/${guidelineId}`),
  categories: () =>
    api.get('/guidelines/categories'),
}

export default api
