'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1'

interface User {
    id: number
    email: string
    created_at: string
    is_active: boolean
}

interface AuthContextType {
    user: User | null
    token: string | null
    login: (email: string, otpCode: string) => Promise<void>
    requestOTP: (email: string) => Promise<void>
    logout: () => void
    isAuthenticated: boolean
    loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null)
    const [token, setToken] = useState<string | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // Load token from localStorage on mount
        const storedToken = localStorage.getItem('token')
        if (storedToken) {
            setToken(storedToken)
            fetchUser(storedToken)
        } else {
            setLoading(false)
        }
    }, [])

    const fetchUser = async (authToken: string) => {
        try {
            const response = await axios.get(`${API_URL}/users/me`, {
                headers: { Authorization: `Bearer ${authToken}` }
            })
            setUser(response.data)
        } catch (error) {
            console.error('Failed to fetch user:', error)
            localStorage.removeItem('token')
            setToken(null)
        } finally {
            setLoading(false)
        }
    }

    const requestOTP = async (email: string) => {
        await axios.post(`${API_URL}/auth/request-otp`, { email })
    }

    const login = async (email: string, otpCode: string) => {
        const response = await axios.post(`${API_URL}/auth/verify-otp`, {
            email,
            otp_code: otpCode
        })

        const { access_token } = response.data
        setToken(access_token)
        localStorage.setItem('token', access_token)

        await fetchUser(access_token)
    }

    const logout = () => {
        setToken(null)
        setUser(null)
        localStorage.removeItem('token')
    }

    return (
        <AuthContext.Provider value={{
            user,
            token,
            login,
            requestOTP,
            logout,
            isAuthenticated: !!token,
            loading
        }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }
    return context
}
