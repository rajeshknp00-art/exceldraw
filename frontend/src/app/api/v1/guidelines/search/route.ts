import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const q = searchParams.get('q') || ''
    const limit = searchParams.get('limit') || '10'
    
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
    const response = await fetch(`${backendUrl}/guidelines/search?q=${encodeURIComponent(q)}&limit=${limit}`)
    
    const data = await response.json()
    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Guidelines search error:', error)
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    )
  }
}
