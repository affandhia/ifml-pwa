from main.utils.naming_management import dasherize

class WorkerConfig(object):

    def __init__(self, name):
        self.cache_config = '\"cacheConfig\": {\"strategy\": \"freshness\", \"maxSize\": 100, \"maxAge": \"1h\"}'
        self.name = name
        self.urls = []

    def add_url(self, url):
        self.urls.append('\"/'+url+'**\"')

    def render(self):
        name_key = '\"name\": \"{name}\"'.format(name=self.name)
        urls_key = '\"urls\": [{urls}]'.format(urls=','.join(self.urls))

        return '{'+ ','.join([name_key,urls_key, self.cache_config]) +'}'
