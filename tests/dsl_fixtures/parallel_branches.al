lang python

tool http as fetch

parallel:
  branch primary:
    call fetch method="GET" url="https://example.com" expect.ok=true
  branch backup:
    call fetch method="GET" url="https://backup.example.com"
