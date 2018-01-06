const ws = new WebSocket('ws://' + window.location.host + '/manage/admin/message')

ws.onopen = function(msgEvent) {
  console.log('[admin] Message Server Connected')
}
ws.onmessage = function(msgEvent) {
  const datas = msgEvent.data.split('|')
  global.store.commit(datas[0], datas[1])
  console.log('[admin] OnMessage', msgEvent.data)
}

export default ws

