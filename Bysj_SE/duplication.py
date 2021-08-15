class RepeatFilter:
    def __init__(self):
        self.visited_url = set()


    @classmethod
    def from_settings(cls, settings):
        print('...................')
        return cls()

    def request_seen(self, request):
        if request.url in self.visited_url:
            return True
        self.visited_url.add(request.url)
        return False

    def open(self):  # can return deferred
        # print('open')
        pass

    def close(self, reason):  # can return a deferred
        # print('close ')
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass