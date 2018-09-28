#!/usr/bin/env python
# coding: utf-8

'''
A single-threaded python implementation of the rate limit interface
'''

import time
from datetime import datetime
import thriftpy


class RateLimitHandler:

    def __init__(self):
        '''
        initialize the bucket storage
        '''
        self.buckets = {}

    def _get_bucket(self, bucket_name):
        '''
        get bucket by bucket name.
        override this to store buckets in different storage
        '''
        return self.buckets.get(bucket_name)

    def _add_bucket(self, bucket):
        '''
        add a bucket by given configuration
        override this to store buckets in different storage
        '''
        self.buckets[bucket.bucket_name] = bucket

    def get_token(self, request):
        '''
        get token from bucket
        param request(GetTokenRequest)
        '''
        bucket = self._get_bucket(request.bucket_name)
        if not bucket:
            return RateLimitResponse(has_limit=False)
        current = time.time() * 1000
        # by default last_checked is 0, so that's alway ok
        time_passed = current - bucket.last_checked
        bucket.last_checked = current
        bucket.tokens += time_passed * (bucket.rate / bucket.timespan)
        if bucket.tokens > rate:
            bucket.tokens = rate
        if bucket.tokens < 1.0:
            return RateLimitResponse(allow=False, next_allow_time=current+bucket.timespan)
        else:
            bucket.tokens -= 1.0
            return RateLimiteResponse(allow=True, next_allow_time=current)

    def add_bucket(self, request):
        '''
        add a bucket to the rate limit store
        '''
        self._add_bucket(request.bucket)

def get_server():
    return make_server(RateLimiter, RateLimiteHandler, '0.0.0.0', 8005)

def main():
    server = get_server()
    server.serve()

if __name__ == '__main__':
    main()


