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


**config.ini Changes**

[twitter]

* apikey=Twitter API Key.
* secret=Twitter Secret.
* auth_t=Twitter Auth Token.
* auth_ts=Twitter Auth Token Secret.
