import os
port = os.environ.get("SERVER_PORT", "8888")

wsgi_app = "wsgi"
bind = f"0.0.0.0:{port}"
workers = 2
loglevel = "debug"
