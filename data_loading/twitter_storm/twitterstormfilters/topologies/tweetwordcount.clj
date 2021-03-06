(ns tweetwordcount
  (:use     [streamparse.specs])
  (:gen-class))

(defn tweetwordcount [options]
   [
    ;; spout configuration
    {"tweet-spout1" (python-spout-spec
          options
          "spouts.tweets1.Tweets"
          ["tweet"]
          :p 1
          )
	"tweet-spout2" (python-spout-spec
          options
          "spouts.tweets2.Tweets"
          ["tweet"]
          :p 1
          )
	"tweet-spout3" (python-spout-spec
          options
          "spouts.tweets3.Tweets"
          ["tweet"]
          :p 1
          )
    }
    ;; bolt configuration
    {"parse-tweet-bolt1" (python-bolt-spec
          options
          {"tweet-spout1" :all}
          "bolts.parse.ParseTweet"
          ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]
          :p 1
          )
	  "parse-tweet-bolt2" (python-bolt-spec
          options
          {"tweet-spout2" :all}
          "bolts.parse.ParseTweet"
          ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]
          :p 1
          )
	  "parse-tweet-bolt3" (python-bolt-spec
          options
          {"tweet-spout3" :all}
          "bolts.parse.ParseTweet"
          ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]
          :p 1
          )
     "count-bolt1" (python-bolt-spec
          options
          {"parse-tweet-bolt1" ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]}
          "bolts.wordcount.WordCounter"
          ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]
          :p 1
       )
	 "count-bolt2" (python-bolt-spec
          options
          {"parse-tweet-bolt2" ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]}
          "bolts.wordcount.WordCounter"
          ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]
          :p 1
          )
	"count-bolt3" (python-bolt-spec
          options
          {"parse-tweet-bolt3" ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]}
          "bolts.wordcount.WordCounter"
          ["created_at" "tweet_id" "tweet_text" "source" "quote_count" "reply_count" "retweet_count" "favorite_count" "lang" "coordinates" "place_coordinates" "place_country" "place_country_code" "place_full_name" "place_id" "place_name" "place_type" "entities_hashtags" "entities_urls" "entities_expanded_url" "entities_user_mentions" "entities_symbols" "user_id" "user_name" "user_screen_name" "user_location" "user_url" "user_description" "user_time_zone" "user_lang" "geo" "timestamp"]
          :p 1
          )
    }
  ]
)
