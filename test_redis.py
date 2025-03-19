import json
import redis


client = redis.Redis("patriot-music.online", port=6379)

key = input("Введите ключь, который хотите получить: ")

value = client.get(key)
print(json.loads(value))