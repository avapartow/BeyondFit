/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        domains: ['beyondfit-photos.s3.amazonaws.com', 'localhost'],
        remotePatterns: [
            {
                protocol: 'https',
                hostname: '**.supabase.co',
            },
            {
                protocol: 'https',
                hostname: '**.amazonaws.com',
            },
        ],
    },
    env: {
        NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    },
}

module.exports = nextConfig
