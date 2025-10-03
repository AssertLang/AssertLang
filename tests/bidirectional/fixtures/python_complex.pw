lang python
agent complex-test-agent
port 23472

tools:
  - http
  - storage
  - logger

expose task.create@v1:
  params:
    title string
    description string
    priority int
  returns:
    task_id string
    status string
    created_at string

expose task.get@v1:
  params:
    task_id string
  returns:
    task_id string
    title string
    description string
    priority int
    status string
    created_at string

expose task.update@v1:
  params:
    task_id string
    status string
  returns:
    task_id string
    status string
    updated_at string

expose task.list@v1:
  params:
    limit int
    offset int
  returns:
    tasks array
    total int
