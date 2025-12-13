import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/v1'

// Create axios instance with auth headers
export const api = axios.create({
    baseURL: API_URL,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

// Auth
export const authAPI = {
    requestOTP: (email: string) =>
        api.post('/auth/request-otp', { email }),

    verifyOTP: (email: string, otpCode: string) =>
        api.post('/auth/verify-otp', { email, otp_code: otpCode }),
}

// Users
export const usersAPI = {
    getMe: () => api.get('/users/me'),

    updateProfile: (data: any) =>
        api.post('/users/me/profile', data),

    getProfile: () =>
        api.get('/users/me/profile'),

    deleteAccount: () =>
        api.delete('/users/me'),

    getFavorites: () =>
        api.get('/users/me/favorites'),

    addFavorite: (productId: number) =>
        api.post(`/users/me/favorites/${productId}`),

    removeFavorite: (productId: number) =>
        api.delete(`/users/me/favorites/${productId}`),

    getLookbooks: () =>
        api.get('/users/me/lookbooks'),

    createLookbook: (data: any) =>
        api.post('/users/me/lookbooks', data),
}

// Body Analysis
export const bodyAPI = {
    analyze: (frontPhoto: File, sidePhoto?: File) => {
        const formData = new FormData()
        formData.append('front_photo', frontPhoto)
        if (sidePhoto) {
            formData.append('side_photo', sidePhoto)
        }
        return api.post('/body/analyze', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
    },

    getHistory: () =>
        api.get('/body/history'),

    getLatest: () =>
        api.get('/body/latest'),
}

// Recommendations
export const recommendationsAPI = {
    get: (filters?: {
        occasion?: string
        min_price?: number
        max_price?: number
        category?: string
        limit?: number
        offset?: number
    }) => api.get('/recommendations/', { params: filters }),
}

// Products
export const productsAPI = {
    list: (filters?: {
        category?: string
        brand_id?: number
        min_price?: number
        max_price?: number
        limit?: number
        offset?: number
    }) => api.get('/products/', { params: filters }),

    get: (id: number) =>
        api.get(`/products/${id}`),

    getAffiliateLink: (id: number) =>
        api.get(`/products/${id}/affiliate-link`),
}

// Brands
export const brandsAPI = {
    list: () => api.get('/brands/'),
    get: (id: number) => api.get(`/brands/${id}`),
}

export default api
