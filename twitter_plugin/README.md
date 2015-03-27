##Twitter URL Parser##
Recognizes Twitter URLs and posts the Tweet text to the channel.

**Commands:**

* _twitter help_

    * Returns: Help message.


**Pattern Matches:**

* ht&#8203;tp://twitter.com/&lt;user&gt;/status/&lt;tweet_id&gt;

    * https included.


**Requirements**

* Tweepy module.

* Twitter API keys (read only).


**config.py Changes**

* twitter_apikey = Twitter API Key.

* twitter_secret = Twitter Secret.

* twitter_auth_t = Twitter Auth Token.

* twitter_auth_ts = Twitter Auth Token Secret.
