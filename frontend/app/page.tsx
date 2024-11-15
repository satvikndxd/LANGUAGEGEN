'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

// API URL from environment variable with fallback
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:9000'

interface Language {
  id: string
  phonemes: string[]
  syllable_structure: string[]
  example_words: string[]
}

interface Translation {
  original: string
  translated: string
  word_mapping: Record<string, string>
}

export default function Home() {
  const [currentLanguage, setCurrentLanguage] = useState<Language | null>(null)
  const [inputText, setInputText] = useState('')
  const [translation, setTranslation] = useState<Translation | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createNewLanguage = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/api/create-language`, {
        method: 'POST',
      })
      const data = await response.json()
      if (data.error) {
        setError(data.error)
        console.error('Server error:', data.error)
        return
      }
      setCurrentLanguage(data)
      setTranslation(null)
    } catch (error) {
      console.error('Error creating language:', error)
      setError('Failed to create language. Please try again.')
    }
    setIsLoading(false)
  }

  const translateText = async () => {
    if (!currentLanguage || !inputText) return

    setIsLoading(true)
    setError(null)
    try {
      const response = await fetch(
        `${API_URL}/api/translate/${currentLanguage.id}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: inputText }),
        }
      )
      const data = await response.json()
      if (data.error) {
        setError(data.error)
        console.error('Server error:', data.error)
        return
      }
      setTranslation(data)
    } catch (error) {
      console.error('Error translating text:', error)
      setError('Failed to translate text. Please try again.')
    }
    setIsLoading(false)
  }

  return (
    <main className="container mx-auto p-4 max-w-4xl">
      <h1 className="text-4xl font-bold text-center mb-8">
        AI Language Generator
      </h1>

      <div className="space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>Create New Language</CardTitle>
            <CardDescription>
              Generate a new constructed language with unique phonology
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              onClick={createNewLanguage}
              disabled={isLoading}
              className="w-full"
            >
              {isLoading ? 'Creating...' : 'Create New Language'}
            </Button>
            {error && (
              <p className="text-red-500 mt-2 text-sm">{error}</p>
            )}
          </CardContent>
        </Card>

        {currentLanguage && (
          <Card>
            <CardHeader>
              <CardTitle>Current Language</CardTitle>
              <CardDescription>
                Language ID: {currentLanguage.id?.slice(0, 8)}...
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold mb-2">Example Words:</h3>
                  <ul className="list-disc pl-5">
                    {currentLanguage.example_words?.map((word, index) => (
                      <li key={index}>{word}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">Translate Text:</h3>
                  <div className="space-y-2">
                    <Input
                      type="text"
                      placeholder="Enter text to translate..."
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                    />
                    <Button
                      onClick={translateText}
                      disabled={isLoading || !inputText}
                      className="w-full"
                    >
                      {isLoading ? 'Translating...' : 'Translate'}
                    </Button>
                  </div>
                </div>

                {translation && (
                  <div>
                    <h3 className="font-semibold mb-2">Translation:</h3>
                    <p className="mb-2">{translation.translated}</p>
                    <h4 className="font-semibold mb-1">Word Mapping:</h4>
                    <ul className="list-disc pl-5">
                      {Object.entries(translation.word_mapping).map(([original, translated], index) => (
                        <li key={index}>
                          {original} → {translated}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  )
}
