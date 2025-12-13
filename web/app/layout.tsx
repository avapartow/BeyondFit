import './globals.css'
import type { Metadata } from 'next'
import { Inter, Outfit } from 'next/font/google'
import { AuthProvider } from '@/lib/contexts/AuthContext'

const inter = Inter({
    subsets: ['latin'],
    variable: '--font-inter',
    display: 'swap',
})

const outfit = Outfit({
    subsets: ['latin'],
    variable: '--font-outfit',
    display: 'swap',
})

export const metadata: Metadata = {
    title: 'BeyondFit - AI-Powered Style Recommendations',
    description: 'Discover clothing that flatters your unique body type with personalized AI-powered recommendations.',
    keywords: 'fashion, style, body type, AI recommendations, personalized shopping',
    openGraph: {
        title: 'BeyondFit - AI-Powered Style Recommendations',
        description: 'Discover clothing that flatters your unique body type',
        type: 'website',
    },
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en" className={`${inter.variable} ${outfit.variable}`}>
            <body className="min-h-screen">
                <AuthProvider>
                    {children}
                </AuthProvider>
            </body>
        </html>
    )
}
