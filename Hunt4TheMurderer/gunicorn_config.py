# Gunicorn configuration file
bind = "0.0.0.0:8080"
workers = 4
worker_class = 'sync'
timeout = 120
accesslog = '-'
errorlog = '-'
loglevel = 'debug'

# Server socket
backlog = 2048

# Worker processes
worker_connections = 1000
keepalive = 2

# Process naming
proc_name = 'hunt4themurderer'

# SSL (uncomment and configure if using HTTPS)
# keyfile = 'path/to/keyfile'
# certfile = 'path/to/certfile' 