const ws = new WebSocket('ws://' + window.location.host + '/manage/admin/message')

ws.onopen = function(msgEvent) {
  console.log('[article] Message Server Connected')
}

ws.onmessage = function(msgEvent) {
  console.log('[article] OnMessage', msgEvent.data)
}

function Send(msg) {
  ws.send('MESSAGE_TYPE_SNACK_BAR|' + msg)
}

export default { ws, Send }
