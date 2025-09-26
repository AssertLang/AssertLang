lang python

tool http as fetch

call fetch method="GET" url="https://example.com" expect.ok=true
let summary = ${fetch.data.summary}
let attempt_limit = 3
