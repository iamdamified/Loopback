import redis

r = redis.Redis(host='localhost', port=6379, db=0)

try:
    r.ping()
    print("✅ Redis connection successful!")
except redis.ConnectionError:
    print("❌ Redis connection failed.")

# After running python manage.py runserver, and Linux(Ubuntu) has started redis, Test redis in VSCODE CLI  : python test_redis.py
