import requests
import boto3
from redis import Redis
redis = Redis(host='redis_cache', port=6379)

# Basic: index is returning correct status
URL_LONG = 'https://www.ea.com/'
URL_SHORT = '2I11au3'
should_answer_200 = requests.get('http://url_shortener:5000')
assert should_answer_200.status_code == 200, f"{should_answer_200.status_code} != 200"


# Calling the endpoint to shorten should shorten, and return somewhere in the page
# the short url. It should also have saved it in the db and the redis cache
form_payload = {'url_long': URL_LONG}
should_contain_short_url = requests.post('http://url_shortener:5000/api/shorten',
                        data=form_payload)
# user facing answer is fine
assert URL_SHORT in str(should_contain_short_url.content), f'{should_contain_short_url.content} does not contain {URL_SHORT}'
# redis correctly cached it
assert str(redis.get(URL_SHORT), 'utf-8') == URL_LONG

# dynamo correctly stored it
resource = boto3.resource('dynamodb',
                           endpoint_url='http://dynamodb:8000',
                           region_name='eu-west-1',
                           aws_access_key_id='dummy',
                           aws_secret_access_key='dummy')
url_table = resource.Table('urls-test') # 'urls' is the table name and the 'env' environment variable is 'test'
value = url_table.get_item(
    Key={
         'short_url': URL_SHORT
    }
)
assert value.get('Item').get('long_url') == URL_LONG


# Now test the redirection to the LONG URL when going to the short url
should_redirect_correctly = requests.get(f'http://url_shortener:5000/{URL_SHORT}')
assert str(should_redirect_correctly.url) == URL_LONG, f'{should_redirect_correctly.url} != {URL_LONG}'

# Should handle wwww. or dummy.com urls
URL_LONG_NO_HTTP = 'www.ea.com/'
URL_SHORT_NO_HTTP = '3KXb5cM'
form_payload_no_http = {'url_long': URL_LONG_NO_HTTP}
r = requests.post('http://url_shortener:5000/api/shorten',
                        data=form_payload_no_http)
should_redirect_correctly_no_http = requests.get(f'http://url_shortener:5000/{URL_SHORT_NO_HTTP}')
assert str(should_redirect_correctly_no_http.url) == f'https://{URL_LONG_NO_HTTP}', f'{should_redirect_correctly_no_http.url} != https://{URL_LONG_NO_HTTP}'


# We ensure redis config is created with allkeys-lru policy
redis_mem_policy = redis.config_get('maxmemory-policy')
assert redis_mem_policy == {'maxmemory-policy': 'allkeys-lru'}, f'redis mem policy is {redis_mem_policy}'

# Empty urls should be handled by server
form_payload = {'url_long': URL_LONG}
should_contain_short_url = requests.post('http://url_shortener:5000/api/shorten',
                        data=form_payload)




exit(0)
