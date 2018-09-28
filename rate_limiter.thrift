struct GetTokenRequest {
    1: string bucket_name;  // which bucket to use
    2: i64 request_time;    // override current time as rate limit time
    3: string caller;
}

struct GetTokenResponse {
    1: bool allow;          // is the rate limit request allowed
    2: i64 next_allow_time; // if not allowed, this the next possible time
    3: bool has_bucket;     // if there is not corresponding bucket, has_bucket is false
}

struct RateLimitBucket {
    1: i64 rate;
    2: i64 timespan;
    3: i64 last_check;
    4: i64 name;
    5: i64 tokens;
}

struct AddBucketRequest {
    1: RateLimitBucket bucket;
    2: string caller;
}

service RateLimiter {
    1: RateLimitResponse get_token(1: GetTokenRequest);
    2: bool add_bucket(1: AddBucketRequest);
}
