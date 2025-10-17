lang python

tool echo as send

call send message="hi"
fanout send:
case ${send.data.ok}:
  let info.status = "ready"
case:
  let info.status = "fallback"
