

class HttpRequestor:

    url: str

    def __init__(self, url: str):
        self.url = url

    def send_post(self, path: str):
        print("Sending POST request COMING SOON")
        