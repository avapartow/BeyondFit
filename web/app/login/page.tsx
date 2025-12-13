'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/contexts/AuthContext'
import { SparklesIcon, EnvelopeIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function LoginPage() {
    const [email, setEmail] = useState('')
    const [otpCode, setOtpCode] = useState('')
    const [step, setStep] = useState<'email' | 'otp'>('email')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const { requestOTP, login } = useAuth()
    const router = useRouter()

    const handleRequestOTP = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            await requestOTP(email)
            setStep('otp')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to send code')
        } finally {
            setLoading(false)
        }
    }

    const handleVerifyOTP = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            await login(email, otpCode)
            router.push('/dashboard')
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Invalid code')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center px-4 py-12 relative overflow-hidden">
            {/* Animated background */}
            <div className="absolute inset-0 -z-10">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-300/30 rounded-full blur-3xl"></div>
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary-300/30 rounded-full blur-3xl"></div>
            </div>

            <div className="w-full max-w-md">
                {/* Logo */}
                <Link href="/" className="flex items-center justify-center space-x-2 mb-8">
                    <SparklesIcon className="h-10 w-10 text-primary-600" />
                    <span className="text-3xl font-display font-bold gradient-text">BeyondFit</span>
                </Link>

                {/* Card */}
                <div className="card animate-slide-up">
                    <div className="text-center mb-8">
                        <h1 className="text-3xl font-display font-bold mb-2">
                            {step === 'email' ? 'Welcome Back' : 'Verify Your Code'}
                        </h1>
                        <p className="text-gray-600">
                            {step === 'email'
                                ? 'Enter your email to receive a magic link'
                                : `We sent a 6-digit code to ${email}`}
                        </p>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
                            {error}
                        </div>
                    )}

                    {step === 'email' ? (
                        <form onSubmit={handleRequestOTP} className="space-y-6">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Email Address
                                </label>
                                <div className="relative">
                                    <EnvelopeIcon className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
                                    <input
                                        type="email"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        placeholder="you@example.com"
                                        className="input-field pl-12"
                                        required
                                    />
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? 'Sending...' : 'Send Magic Code'}
                            </button>
                        </form>
                    ) : (
                        <form onSubmit={handleVerifyOTP} className="space-y-6">
                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Verification Code
                                </label>
                                <input
                                    type="text"
                                    value={otpCode}
                                    onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                                    placeholder="000000"
                                    className="input-field text-center text-2xl tracking-widest font-mono"
                                    maxLength={6}
                                    required
                                />
                            </div>

                            <button
                                type="submit"
                                disabled={loading || otpCode.length !== 6}
                                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? 'Verifying...' : 'Verify & Continue'}
                            </button>

                            <button
                                type="button"
                                onClick={() => setStep('email')}
                                className="w-full text-sm text-gray-600 hover:text-primary-600 transition-colors"
                            >
                                ← Back to email
                            </button>
                        </form>
                    )}

                    <div className="mt-8 pt-6 border-t border-gray-200 text-center text-sm text-gray-600">
                        By continuing, you agree to our{' '}
                        <Link href="/terms" className="text-primary-600 hover:underline">Terms</Link>
                        {' '}and{' '}
                        <Link href="/privacy" className="text-primary-600 hover:underline">Privacy Policy</Link>
                    </div>
                </div>

                <p className="mt-6 text-center text-sm text-gray-600">
                    New to BeyondFit? Get started with a free body scan!
                </p>
            </div>
        </div>
    )
}
