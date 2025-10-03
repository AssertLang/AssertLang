lang nodejs
agent tools-test-agent
port 20101

expose process.data@v1:
  params:
    input string
    format string
  returns:
    output string
    status string
    timestamp int

expose health.check@v1:
  params:
  returns:
    healthy bool
    uptime int
    version string
