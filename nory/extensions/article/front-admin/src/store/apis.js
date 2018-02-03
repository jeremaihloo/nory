import http from '../js/http'

export function SAVE(data) {
  return http.post('/api/articles', data)
}

export function PUBLISH(id) {
  return http.post(`/api/articles/${id}/publish`, {})
}

export function UN_PUBLISH(id) {
  return http.post(`/api/articles/${id}/un-publish`, {})
}

export function GET_ARTICLES() {
  return http.get('/api/articles')
}

export function ENABLE(id) {
  return http.post(`/api/articles/${id}/enable`, {})
}

export function DISABLE(id) {
  return http.post(`/api/articles/${id}/disable`, {})
}

export function GET_ARTICLE(id) {
  return http.get(`/api/articles/${id}`)
}
