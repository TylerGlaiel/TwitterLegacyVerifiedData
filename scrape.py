import tweepy
import time
import json

def get_twitter():
    CONSUMER_KEY = 'PUT OATH KEY HERE'
    CONSUMER_SECRET = 'PUT OATH KEY HERE'
    ACCESS_KEY = 'PUT OATH KEY HERE'
    ACCESS_SECRET = 'PUT OATH KEY HERE'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return tweepy.API(auth)
    
twitter = get_twitter()

print("gathering following ids")
ids = []
for page in tweepy.Cursor(twitter.friends_ids, screen_name="verified").pages():
    ids.extend(page)
    print("ids gathered: "+str(len(ids)))
    time.sleep(60)

file = open("verified_following_ids.txt", "w")
file.write(str(ids))


#print("loading following ids")
#with open("verified_following_ids.json", "r") as f:
#    ids = json.load(f)



print("gathering following data")
users = []
idChunks = [ids[i:i + 100] for i in range(0, len(ids), 100)]
users = []
for idChunk in idChunks:
    success = False
    sleep_time = 16
    while not success:
        try:
            users.extend(twitter.lookup_users(user_ids=idChunk))
            print("users gathered: "+str(len(users)))
            success = True
        except Exception:
            print("RATE EXCEDED. SLEEPING FOR "+str(sleep_time)+" MINUTES")
            time.sleep(sleep_time*60)
            sleep_time = sleep_time * 1.5
            
        if not success:
            twitter = get_twitter()

print("grabbing usernames")
user_map = []
for u in users:
    user_map.append((u.id_str, u.screen_name))
    
print("saving usernames")
file3 = open("verified_following_usernames.txt", "w", encoding='utf-8')
file3.write(str(user_map))

print("saving data")
file2 = open("verified_following_data.txt", "w", encoding='utf-8')
file2.write(str(users))
