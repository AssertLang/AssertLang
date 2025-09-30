lang python
agent order-service
port 23451

tools:
  - storage
  - http

expose order.create@v1:
  params:
    user_id string
    items array
    total_amount string
  returns:
    order_id string
    user_id string
    user_name string
    items array
    total_amount string
    status string
    created_at string

expose order.get@v1:
  params:
    order_id string
  returns:
    order_id string
    user_id string
    items array
    total_amount string
    status string
    created_at string

expose order.list@v1:
  params:
    user_id string
    limit int
    offset int
  returns:
    orders array
    total int
