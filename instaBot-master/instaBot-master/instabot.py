from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from clarifai.rest import ClarifaiApp
import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN = '1525979253.7d7ade8.a2d201f6ad2a4bbf9eded13b9094308f'
# Token Owner : AVinstaBot.main
# Sandbox Users : AVinstaBot.test0, AVinstaBot.test1, AVinstaBot.test2...... AVinstaBot.test10

BASE_URL = 'https://api.instagram.com/v1/'
ar = []
my_dict = {
    'imageurl': None,
    'words': ''

}
user_lis = ['shadan_fcb', 'mmehndiratta']

#Function declaration to get your own info



def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'



#Function declaration to get the ID of a user by username



def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()



#Function declaration to get the info of a user by username



def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'



#Function declaration to get your recent post



def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'



#Function declaration to get the ID of the recent post of a user by username


def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


def unlike_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_unlike = requests.delete(request_url).json()
    if post_a_unlike['meta']['code'] == 200:
        print ' You have unLiked the pic successfully! '
    else:
        print ' status  code other than 200 received!'


# Function declaration to like the recent post of a user



def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


# Function declaration to make a comment on the recent post of the user



def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


# Function declaration to make delete negative comments from the recent post


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


app = ClarifaiApp(api_key='eeaa1edfc07f45a7ad2c2b8551e4c2f6')

# get the general model
model = app.models.get('food-items-v1.0')
for user in user_lis:
    def get_users_post(user):
        user_id = get_user_id(user)
        if user_id == None:
            print 'User does not exist!'
            exit()
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_media = requests.get(request_url).json()

        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                image_name = user_media['data'][0]['id'] + '.jpeg'
                image_url = user_media['data'][0]['images']['standard_resolution']['url']
                model = app.models.get('food-items-v1.0')
                response = model.predict_by_url(url=image_url)
                for x in response['outputs'][0]['data']['concepts']:
                    print x['name'], x['value']
                    if x['value'] > .7:
                        strr = x['name']
                        temp = my_dict['words']
                        temp = temp + ' ' + str(strr)
                        my_dict['words'] = temp
                String = my_dict['words']
                print
                wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=1200, height=1000).generate(
                    String)
                plt.imshow(wordcloud)
                plt.axis('off')
                plt.show()
                urllib.urlretrieve(image_url, image_name)
            else:
                print "error"

        else:
            print "error"


def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"

        print "f.Like the recent post of a user\n"
        print "g.Unlike the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.SHOW SUBTREND OF FOOD EATEN \n"
        print "k:To exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)

        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            unlike_a_post(insta_username)

        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "j":
            get_users_post(user)
        elif choice=="k":
            exit()


        else:
            print "wrong choice"


start_bot()