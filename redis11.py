import redis

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
r.set('foo', 'bar')
print(r.get('foo'))