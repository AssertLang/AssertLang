lang python
agent user-service
port 23450

tools:
  - storage

expose user.create@v1:
  params:
    email string
    name string
  returns:
    user_id string
    email string
    name string
    status string
    created_at string

expose user.get@v1:
  params:
    user_id string
  returns:
    user_id string
    email string
    name string
    status string
    created_at string

expose user.list@v1:
  params:
    limit int
    offset int
  returns:
    users array
    total int
