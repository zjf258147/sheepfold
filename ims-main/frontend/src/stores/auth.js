import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { login as loginApi, getMe } from '@/api/auth'
import { PERMISSION_MAP } from '@/constants/permissions'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const role = computed(() => user.value?.role || '')
  const isAdmin = computed(() => role.value === 'ADMIN')
  const isWarehouse = computed(() => role.value === 'WAREHOUSE')
  const isQuality = computed(() => role.value === 'QUALITY')
  const isProduction = computed(() => role.value === 'PRODUCTION')
  const isTestEngineer = computed(() => role.value === 'TEST_ENGINEER')
  const isStaff = computed(() => role.value === 'STAFF')

  function hasRole(...roles) {
    return isAdmin.value || roles.includes(role.value)
  }

  function canEdit(permKey) {
    if (isAdmin.value) return true
    const roles = PERMISSION_MAP[permKey]
    if (!roles) return false
    return roles.includes(role.value)
  }

  async function login(username, password) {
    const res = await loginApi({ username, password })
    token.value = res.data.access_token
    localStorage.setItem('token', token.value)
    await fetchUser()
  }

  async function fetchUser() {
    if (!token.value) return
    const res = await getMe()
    user.value = res.data
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { token, user, role, isAdmin, isWarehouse, isQuality, isProduction, isTestEngineer, isStaff, hasRole, canEdit, login, fetchUser, logout }
})