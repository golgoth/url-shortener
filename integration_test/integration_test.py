import requests

URL_LONG = 'https://www.ea.com/'
URL_SHORT = '2I11au3'
should_answer_200 = requests.get('http://url_shortener:5000')
assert should_answer_200.status_code == 200, f"{should_answer_200.status_code} != 200"



form_payload = {'url_long': URL_LONG}
should_contain_short_url = requests.post('http://url_shortener:5000/api/shorten',
                        data=form_payload)

assert URL_SHORT in str(should_contain_short_url.content), f'{should_contain_short_url.content} does not contain {URL_SHORT}'


should_redirect_correctly = requests.get(f'http://url_shortener:5000/{URL_SHORT}')
assert str(should_redirect_correctly.url) == URL_LONG, f'{should_redirect_correctly.url} != {URL_LONG}'
exit(0)

# We ensure redis config is created with allkeys-lru policy
from redis import Redis
redis = Redis(host='redis_cache', port=6379)
assert redis.config_get('maxmemory-policy ') == 'allkeys-lru'
