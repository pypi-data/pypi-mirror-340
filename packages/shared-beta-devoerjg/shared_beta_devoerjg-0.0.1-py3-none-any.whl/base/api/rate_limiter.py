from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

"""_summary_
# How to use?

# In main funciton

## 1. Init the Flask app
app = Flask(__name__)         # -- init the Flask first
limiter.init_app(app=app)     # -- add limiter to wrap the app

## 2. Define the limit exceeds function
@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    return {"code": 1, "data": [], "msg": "429 Rate limit exceeded"}, 429
"""
