lang python
agent minimal-test-agent
port 23470

expose health.check@v1:
  params:
  returns:
    status string
    uptime int

expose echo.message@v1:
  params:
    message string
  returns:
    echo string
    timestamp string
