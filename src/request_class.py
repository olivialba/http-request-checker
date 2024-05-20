import requests


class RequestInfo():
    
    GET = 'GET'
    POST = 'POST'
    GREEN = (170, 255, 0)
    RED = (238, 75, 43)
    
    def __init__(self, url, type, header, cookies):
        self.url = url
        self.type = self.POST if type == self.POST else self.GET
        self.header = header
        self.cookies = cookies
        
        if self.type == self.GET: self.response = self._get_request()
        if self.type == self.POST: self.response = self._post_request()
        
        # Response Info
        self.status_code = self.response.status_code
        self.reason = self.response.reason
        self.color = self.GREEN if self.status_code < 300 else self.RED
        self.response_time = str(round(self.response.elapsed.total_seconds(), 3))
        self.content_type = self.response.headers['content-type']
    
    def _get_request(self) -> dict:
        response = requests.get(url=self.url, 
                                headers=self.get_header(), 
                                cookies=self.get_cookies())
        return response
         
    def _post_request(self) -> dict:
        response = requests.post(url=self.url, 
                                headers=self.get_header(), 
                                cookies=self.get_cookies())
        return response
    
    def get_header(self):
        return self.header
    
    def get_cookies(self):
        return self.cookies