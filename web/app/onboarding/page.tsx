'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/contexts/AuthContext'
import { usersAPI } from '@/lib/api'
import { SparklesIcon } from '@heroicons/react/24/outline'

const STYLE_OPTIONS = [
    { value: 'minimal', label: 'Minimal', emoji: '✨' },
    { value: 'classic', label: 'Classic', emoji: '👔' },
    { value: 'party', label: 'Party', emoji: '🎉' },
    { value: 'casual', label: 'Casual', emoji: '👕' },
    { value: 'bohemian', label: 'Bohemian', emoji: '🌸' },
    { value: 'sporty', label: 'Sporty', emoji: '⚡' },
]

const COLOR_OPTIONS = [
    { value: 'black', label: 'Black', color: '#000000' },
    { value: 'white', label: 'White', color: '#FFFFFF' },
    { value: 'red', label: 'Red', color: '#EF4444' },
    { value: 'blue', label: 'Blue', color: '#3B82F6' },
    { value: 'pink', label: 'Pink', color: '#EC4899' },
    { value: 'purple', label: 'Purple', color: '#8B5CF6' },
    { value: 'green', label: 'Green', color: '#10B981' },
    { value: 'yellow', label: 'Yellow', color: '#F59E0B' },
    { value: 'navy', label: 'Navy', color: '#1E40AF' },
    { value: 'beige', label: 'Beige', color: '#D4B5A0' },
]

export default function OnboardingPage() {
    const router = useRouter()
    const { user } = useAuth()

    const [step, setStep] = useState(1)
    const [loading, setLoading] = useState(false)
    const [formData, setFormData] = useState({
        style_preferences: [] as string[],
        budget_min: 50,
        budget_max: 200,
        region: 'US',
        favorite_colors: [] as string[],
        size_top: '',
        size_bottom: '',
        size_dress: '',
        height_cm: undefined,
        weight_kg: undefined,
        store_photos: false,
    })

    const handleSubmit = async () => {
        setLoading(true)
        try {
            await usersAPI.updateProfile(formData)
            router.push('/scan')
        } catch (error) {
            console.error('Failed to save profile:', error)
        } finally {
            setLoading(false)
        }
    }

    const toggleStyle = (style: string) => {
        setFormData(prev => ({
            ...prev,
            style_preferences: prev.style_preferences.includes(style)
                ? prev.style_preferences.filter(s => s !== style)
                : [...prev.style_preferences, style]
        }))
    }

    const toggleColor = (color: string) => {
        setFormData(prev => ({
            ...prev,
            favorite_colors: prev.favorite_colors.includes(color)
                ? prev.favorite_colors.filter(c => c !== color)
                : [...prev.favorite_colors, color]
        }))
    }

    return (
        <div className="min-h-screen py-12 px-4">
            <div className="max-w-3xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <SparklesIcon className="h-16 w-16 text-primary-600 mx-auto mb-4" />
                    <h1 className="text-4xl font-display font-bold mb-2">Welcome to BeyondFit!</h1>
                    <p className="text-gray-600">Let's personalize your experience</p>
                </div>

                {/* Progress */}
                <div className="flex justify-center mb-12">
                    {[1, 2, 3].map((s) => (
                        <div key={s} className="flex items-center">
                            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${step >= s ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white' : 'bg-gray-200 text-gray-500'
                                }`}>
                                {s}
                            </div>
                            {s < 3 && <div className={`w-16 h-1 ${step > s ? 'bg-primary-600' : 'bg-gray-200'}`} />}
                        </div>
                    ))}
                </div>

                {/* Step Content */}
                <div className="card">
                    {step === 1 && (
                        <div className="space-y-6">
                            <h2 className="text-2xl font-display font-bold">What's Your Style?</h2>
                            <p className="text-gray-600">Select all that apply (choose at least 1)</p>

                            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                {STYLE_OPTIONS.map((option) => (
                                    <button
                                        key={option.value}
                                        onClick={() => toggleStyle(option.value)}
                                        className={`p-6 rounded-xl border-2 transition-all hover:scale-105 ${formData.style_preferences.includes(option.value)
                                                ? 'border-primary-500 bg-primary-50'
                                                : 'border-gray-200 hover:border-primary-300'
                                            }`}
                                    >
                                        <div className="text-4xl mb-2">{option.emoji}</div>
                                        <div className="font-semibold">{option.label}</div>
                                    </button>
                                ))}
                            </div>

                            <button
                                onClick={() => setStep(2)}
                                disabled={formData.style_preferences.length === 0}
                                className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                Continue
                            </button>
                        </div>
                    )}

                    {step === 2 && (
                        <div className="space-y-6">
                            <h2 className="text-2xl font-display font-bold">Budget & Preferences</h2>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Budget Range (USD)
                                </label>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="text-xs text-gray-500">Min</label>
                                        <input
                                            type="number"
                                            value={formData.budget_min}
                                            onChange={(e) => setFormData(prev => ({ ...prev, budget_min: parseInt(e.target.value) }))}
                                            className="input-field"
                                        />
                                    </div>
                                    <div>
                                        <label className="text-xs text-gray-500">Max</label>
                                        <input
                                            type="number"
                                            value={formData.budget_max}
                                            onChange={(e) => setFormData(prev => ({ ...prev, budget_max: parseInt(e.target.value) }))}
                                            className="input-field"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-semibold text-gray-700 mb-2">
                                    Favorite Colors (select up to 3)
                                </label>
                                <div className="grid grid-cols-5 gap-3">
                                    {COLOR_OPTIONS.map((color) => (
                                        <button
                                            key={color.value}
                                            onClick={() => toggleColor(color.value)}
                                            disabled={!formData.favorite_colors.includes(color.value) && formData.favorite_colors.length >= 3}
                                            className={`aspect-square rounded-lg border-4 transition-all hover:scale-110 ${formData.favorite_colors.includes(color.value)
                                                    ? 'border-primary-500'
                                                    : 'border-transparent hover:border-gray-300'
                                                }`}
                                            style={{ backgroundColor: color.color }}
                                            title={color.label}
                                        />
                                    ))}
                                </div>
                            </div>

                            <div className="flex gap-4">
                                <button onClick={() => setStep(1)} className="btn-secondary flex-1">
                                    Back
                                </button>
                                <button onClick={() => setStep(3)} className="btn-primary flex-1">
                                    Continue
                                </button>
                            </div>
                        </div>
                    )}

                    {step === 3 && (
                        <div className="space-y-6">
                            <h2 className="text-2xl font-display font-bold">Size Information</h2>
                            <p className="text-gray-600">Help us find your perfect fit</p>

                            <div className="grid md:grid-cols-3 gap-4">
                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Top Size
                                    </label>
                                    <select
                                        value={formData.size_top}
                                        onChange={(e) => setFormData(prev => ({ ...prev, size_top: e.target.value }))}
                                        className="input-field"
                                    >
                                        <option value="">Select</option>
                                        <option value="XS">XS</option>
                                        <option value="S">S</option>
                                        <option value="M">M</option>
                                        <option value="L">L</option>
                                        <option value="XL">XL</option>
                                        <option value="XXL">XXL</option>
                                    </select>
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Bottom Size
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.size_bottom}
                                        onChange={(e) => setFormData(prev => ({ ...prev, size_bottom: e.target.value }))}
                                        placeholder="e.g., 28"
                                        className="input-field"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                                        Dress Size
                                    </label>
                                    <input
                                        type="text"
                                        value={formData.size_dress}
                                        onChange={(e) => setFormData(prev => ({ ...prev, size_dress: e.target.value }))}
                                        placeholder="e.g., 6"
                                        className="input-field"
                                    />
                                </div>
                            </div>

                            <div className="border-t border-gray-200 pt-6">
                                <label className="flex items-start space-x-3">
                                    <input
                                        type="checkbox"
                                        checked={formData.store_photos}
                                        onChange={(e) => setFormData(prev => ({ ...prev, store_photos: e.target.checked }))}
                                        className="mt-1 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                                    />
                                    <div>
                                        <div className="font-semibold">Save my photos</div>
                                        <div className="text-sm text-gray-600">
                                            By default, we delete photos after analysis. Check this to save them for future reference.
                                        </div>
                                    </div>
                                </label>
                            </div>

                            <div className="flex gap-4">
                                <button onClick={() => setStep(2)} className="btn-secondary flex-1">
                                    Back
                                </button>
                                <button
                                    onClick={handleSubmit}
                                    disabled={loading}
                                    className="btn-primary flex-1 disabled:opacity-50"
                                >
                                    {loading ? 'Saving...' : 'Complete Setup'}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}
