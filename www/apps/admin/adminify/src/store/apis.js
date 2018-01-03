import http from '../js/http'

export function DO_LOGIN(data) {
  return http.post('/api/login/cookie', data)
}

export function DO_LOGOUT(data) {
  return http.post('/api/logout')
}

export function DO_GET_MENU(data) {
  return http.get('/api/menus')
}

export function DO_AUTH_COOKIE_ME() {
  return http.get('/api/auth/cookie/me')
}
