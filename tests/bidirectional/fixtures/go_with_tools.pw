lang go
agent go-http-agent
port 8081

tools:
  - http

expose fetch.data@v1:
  params:
    url string
    method string
  returns:
    status int
    body string
    headers object
