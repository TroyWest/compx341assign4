import time
import redis
from flask import Flask
from math import sqrt

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
	retries = 5
	while True:
		try:
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)

@app.route('/')
def hello():
	count = get_hit_count()
	return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<number>')
def isPrime(number):
	prime = True
	n = int(number)
	if n < 2 :
		prime = False
	else:
		if n == 2 or n == 3:
			prime = True
		elif (n % 2) == 0:
			prime = False
		else:
			for x in range(3, int(sqrt(n))):
				if (n % x) == 0:
					prime = False
		
	if prime:
		primes = cache.lrange('primes', 0, -1)
		primes.sort()
		exists = False		
		for num in primes:			
			if int(num) == n:
				exists = True				
		if exists == False:
			cache.rpush('primes', n)
		return '{} is prime'.format(number)
	else: 
		return '{} is not prime'.format(number)

@app.route('/primesStored')
def displayStoredPrimes():
	cachedPrimes = cache.lrange('primes', 0, -1)
	primes = []
	for num in cachedPrimes:
		primes.append(int(num))
	primes.sort()
	return "{}".format(primes)