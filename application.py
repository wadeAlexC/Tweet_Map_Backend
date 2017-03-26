from flask import Flask, request, jsonify
import os, requests, base64, ast, json


app_key = "qPIbkhY5XAXt87oaVzPFuXtjh"
app_secret = "g4nHdDftVKbjNkHKWbuAs2zDe8lnEWGOcpdwoY0Lncr1gNfQ05"

#app_key + ":" + app_secret
app_secret_b64 = base64.b64encode(b'qPIbkhY5XAXt87oaVzPFuXtjh:g4nHdDftVKbjNkHKWbuAs2zDe8lnEWGOcpdwoY0Lncr1gNfQ05')


# Returns the access_token for api calls
def authenticate():
    headers = {'host': 'api.twitter.com',
               'User-Agent': 'TweetMapHackEmory',
               'Authorization': 'Basic cVBJYmtoWTVYQVh0ODdvYVZ6UEZ1WHRqaDpnNG5IZERmdFZLYmpOa0hLV2J1QXMyekRlOGxuRVdHT2NwZHdvWTBMbmNyMWdOZlEwNQ==',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    ret = requests.post("https://api.twitter.com/oauth2/token", headers=headers, data='grant_type=client_credentials')

    # Decode the return value from bytes to str
    content = ret.content.decode('ascii')
    # Convert the str representation of a dict to a dict
    content_dict = ast.literal_eval(content)

    #If the incorrect token was given to us, we return None
    if not content_dict['token_type'] == 'bearer':
        return None

    return content_dict['access_token']


access_token = authenticate()

print("KEY: " + app_key)
print("SECRET: " + app_secret)
print("B64: " + str(app_secret_b64))

application = Flask(__name__)


@application.route('/')
def index():
    return "Hello, world! Up and running!"


@application.route('/location/<float:lat>/<float:long>', methods=['GET'])
def tweet_request(lat, long):
    #First, check auth status:
    ratelimit = get_rate_limit()

    if ratelimit == -1:
        return jsonify({"status":400, "message":"Too many requests have been processed and the Twitter API ratelimit has expired."})
    elif ratelimit == -2:
        return jsonify({"status":401, "message":"Bad Auth Data"})
    elif ratelimit == -3:
        access_token = authenticate() # Try to reauthenticate


    headers = {'host': 'api.twitter.com',
               'User-Agent': 'TweetMapHackEmory',
               'Authorization': "Bearer " + access_token}

    tweets = requests.get("https://api.twitter.com/1.1/search/tweets.json?q=%20&geocode=33.792341,-84.325308,50mi",
                          headers=headers)

    tweet_dict = json.loads(tweets.content.decode('ascii'))

    # print("NUM TWEETS FOUND: " + str(len(tweet_dict['statuses'])))

    # TODO here we pass tweet_dict to the NLP algorithm, and return jsonify(results)

    return jsonify(tweet_dict)


#Returns the rate_limit for the Twitter API, or various error values associated with OAuth
def get_rate_limit():
    headers = {'host':'api.twitter.com',
               'User-Agent':'TweetMapHackEmory',
               'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
               'Authorization':'Bearer ' + access_token}

    ret = requests.get("https://api.twitter.com/1.1/application/rate_limit_status.json?resources=search", headers=headers)
    ret_dict = json.loads(ret.content.decode('ascii'))

    if 'errors' in ret_dict:
        if ret_dict['errors'][0]['code'] == 89:
            return -3 # Triggers a reauthentication
        else:
            return -2 # Error val for a bad request
    elif 'resources' in ret_dict:
        remaining_rate_limit = ret_dict['resources']['search']['/search/tweets']['remaining']
        if remaining_rate_limit <= 0:
            return -1
        else:
            return remaining_rate_limit

    return 0


if __name__ == "__main__":
    application.debug = True
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port, debug=True)
