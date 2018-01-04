import http from '../js/http'

export function SAVE(data) {
  return http.post('/api/articles', data)
}

export function PUBLISH(data) {
  return http.post('/api/articles/publish', data)
}
