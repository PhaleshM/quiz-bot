from django.shortcuts import render
import redis

def test_redis_connection():
    r = redis.Redis(host='localhost', port=6379, db=0)
    if r.ping():
        return True
    else:
        return False
    

def chat(request):
    if not request.session.session_key:
        request.session.create()
    return render(request, 'chat.html')
