lang rust
agent tool-rust-agent
port 9091

tools:
  - http

expose fetch.data@v1:
  params:
    url string
  returns:
    status int
    data string
    cached bool

expose process.data@v1:
  params:
    input string
    transform string
  returns:
    output string
    success bool
