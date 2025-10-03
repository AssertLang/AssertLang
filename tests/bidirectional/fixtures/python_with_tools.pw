lang python
agent tool-test-agent
port 23471

tools:
  - http
  - storage

expose fetch.data@v1:
  params:
    url string
  returns:
    status int
    data string
    cached bool

expose store.item@v1:
  params:
    key string
    value string
  returns:
    stored bool
    key string
    timestamp string

expose retrieve.item@v1:
  params:
    key string
  returns:
    found bool
    value string
    key string
