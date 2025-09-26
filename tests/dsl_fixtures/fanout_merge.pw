lang python

tool echo as send

call send message="hi"
fanout send:
case:
  let info.value = ${send.data.message}
case:
  let info.value = "fallback"
merge into summary send.case_0 send.case_1
