'use client'

import Link from 'next/link'
import { SparklesIcon, CameraIcon, ShoppingBagIcon, HeartIcon } from '@heroicons/react/24/outline'
import { useAuth } from '@/lib/contexts/AuthContext'

export default function HomePage() {
    const { isAuthenticated } = useAuth()

    return (
        <div className="min-h-screen">
            {/* Navigation */}
            <nav className="fixed top-0 left-0 right-0 z-50 glass">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center space-x-2">
                            <SparklesIcon className="h-8 w-8 text-primary-600" />
                            <span className="text-2xl font-display font-bold gradient-text">BeyondFit</span>
                        </div>

                        <div className="flex items-center space-x-4">
                            {isAuthenticated ? (
                                <>
                                    <Link href="/dashboard" className="text-gray-700 hover:text-primary-600 font-medium transition-colors">
                                        Dashboard
                                    </Link>
                                    <Link href="/scan" className="btn-primary">
                                        Body Scan
                                    </Link>
                                </>
                            ) : (
                                <>
                                    <Link href="/login" className="text-gray-700 hover:text-primary-600 font-medium transition-colors">
                                        Sign In
                                    </Link>
                                    <Link href="/login" className="btn-primary">
                                        Get Started
                                    </Link>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 px-4 overflow-hidden">
                {/* Animated background elements */}
                <div className="absolute inset-0 -z-10">
                    <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-300/30 rounded-full blur-3xl animate-bounce-slow"></div>
                    <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary-300/30 rounded-full blur-3xl animate-bounce-slow" style={{ animationDelay: '1s' }}></div>
                </div>

                <div className="max-w-7xl mx-auto text-center animate-fade-in">
                    <h1 className="text-6xl md:text-7xl font-display font-bold mb-6 leading-tight">
                        Discover Style That
                        <br />
                        <span className="gradient-text">Flatters Your Body</span>
                    </h1>

                    <p className="text-xl md:text-2xl text-gray-600 mb-12 max-w-3xl mx-auto font-light">
                        AI-powered body analysis meets personalized fashion recommendations.
                        Look stunning in clothes designed for your unique shape.
                    </p>

                    <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                        <Link href={isAuthenticated ? "/scan" : "/login"} className="btn-primary text-lg px-8 py-4">
                            <CameraIcon className="h-6 w-6 inline mr-2" />
                            Start Your Body Scan
                        </Link>
                        <Link href="/how-it-works" className="btn-secondary text-lg px-8 py-4">
                            How It Works
                        </Link>
                    </div>

                    <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
                        {[
                            { value: '10K+', label: 'Happy Users' },
                            { value: '98%', label: 'Satisfaction' },
                            { value: '5K+', label: 'Products' },
                            { value: '50+', label: 'Brands' },
                        ].map((stat) => (
                            <div key={stat.label} className="animate-slide-up">
                                <div className="text-4xl font-display font-bold gradient-text">{stat.value}</div>
                                <div className="text-gray-600 mt-1">{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 px-4 bg-white/50">
                <div className="max-w-7xl mx-auto">
                    <h2 className="text-4xl md:text-5xl font-display font-bold text-center mb-16">
                        How <span className="gradient-text">BeyondFit</span> Works
                    </h2>

                    <div className="grid md:grid-cols-3 gap-8">
                        {[
                            {
                                icon: CameraIcon,
                                title: 'Body Scan',
                                description: 'Upload or take photos with your camera. Our AI analyzes your body ratios and determines your shape.',
                                color: 'from-purple-500 to-pink-500',
                            },
                            {
                                icon: SparklesIcon,
                                title: 'AI Analysis',
                                description: 'Get your body type classification with personalized insights and flattering silhouette recommendations.',
                                color: 'from-pink-500 to-rose-500',
                            },
                            {
                                icon: ShoppingBagIcon,
                                title: 'Perfect Matches',
                                description: 'Browse curated products tailored to your body type, style, and budget. Shop with confidence.',
                                color: 'from-rose-500 to-orange-500',
                            },
                        ].map((feature, index) => (
                            <div key={index} className="card-interactive group">
                                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.color} p-4 mb-6 group-hover:scale-110 transition-transform duration-300`}>
                                    <feature.icon className="w-full h-full text-white" />
                                </div>

                                <h3 className="text-2xl font-display font-bold mb-4">{feature.title}</h3>
                                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Body Types Section */}
            <section className="py-20 px-4">
                <div className="max-w-7xl mx-auto">
                    <h2 className="text-4xl md:text-5xl font-display font-bold text-center mb-6">
                        Designed For <span className="gradient-text">Every Body</span>
                    </h2>

                    <p className="text-xl text-gray-600 text-center mb-16 max-w-3xl mx-auto">
                        We celebrate all body types. Our AI understands your unique proportions and
                        recommends styles that enhance your natural beauty.
                    </p>

                    <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
                        {['Pear', 'Apple', 'Hourglass', 'Rectangle', 'Inverted Triangle'].map((type) => (
                            <div key={type} className="card text-center group">
                                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-primary-400 to-secondary-400 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                    <HeartIcon className="w-10 h-10 text-white" />
                                </div>
                                <h3 className="font-display font-semibold text-lg">{type}</h3>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-4">
                <div className="max-w-4xl mx-auto text-center card animated-gradient text-white">
                    <h2 className="text-4xl md:text-5xl font-display font-bold mb-6">
                        Ready to Find Your Perfect Fit?
                    </h2>

                    <p className="text-xl mb-8 opacity-90">
                        Join thousands of women who've discovered their most flattering styles
                    </p>

                    <Link href={isAuthenticated ? "/scan" : "/login"}
                        className="inline-block px-8 py-4 bg-white text-primary-700 font-bold rounded-xl hover:shadow-2xl hover:scale-105 transition-all duration-300">
                        Get Started - It's Free
                    </Link>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-12 px-4">
                <div className="max-w-7xl mx-auto text-center">
                    <div className="flex items-center justify-center space-x-2 mb-4">
                        <SparklesIcon className="h-8 w-8 text-primary-400" />
                        <span className="text-2xl font-display font-bold">BeyondFit</span>
                    </div>

                    <p className="text-gray-400 mb-6">
                        AI-powered style recommendations for every body
                    </p>

                    <div className="flex justify-center space-x-8 text-sm text-gray-400">
                        <Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link>
                        <Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link>
                        <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
                    </div>

                    <div className="mt-8 text-sm text-gray-500">
                        © 2024 BeyondFit. All rights reserved.
                    </div>
                </div>
            </footer>
        </div>
    )
}
