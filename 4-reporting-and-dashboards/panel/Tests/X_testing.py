import tweepy


class MyStreamListener(tweepy.StreamingClient):
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False in on_error disconnects the stream
            return False

# Authenticate to Twitter
auth = tweepy.OAuthHandler("rUINI5Hi1YGjTpWVEGF3CyZDR", "LjW4K9o0zmwiGJSiaJJGZgXvDPAgxFlWtrXEHV58xXggzjcTJY")
auth.set_access_token("1663120075971260419-NPb5hYhjTcbcVtWwQgMFxlCmCp5JfX", "nTzl2qGVndDGoYoaLZwVZE3wkuonwTThn8cWi2603Gw5e")


# Create a stream
listener = MyStreamListener("AAAAAAAAAAAAAAAAAAAAAKVZnwEAAAAAVXXyTvTYUOtDBm2gywcu3Z4I2vA%3Dv9utfvggle9gp8dNw2uvXSdXDC76T7yqULA8Px54bqcfKR6VYs")
stream = tweepy.Stream(auth=auth, listener=listener)

# Start streaming tweets
# print(stream.filter(track=['python', 'data science', 'machine learning']))

# stream.filter(locations=[-74.25909,40.477399,-73.700181,40.916178])

