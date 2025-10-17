lang dotnet
agent dotnet-http-agent
port 5001

tools:
  - http

expose fetch.data@v1:
  params:
    url string
  returns:
    status int
    body string
    success bool
