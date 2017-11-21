from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
from clarifai.rest import ClarifaiApp
import  requests
import urllib


APP_ACCESS_TOKEN='1525979253.7d7ade8.a2d201f6ad2a4bbf9eded13b9094308f'
BASE_URL = 'https://api.instagram.com/v1/'
ar=[]
my_dict = {
    'imageurl': None,
    'words': ''

}
user_lis=['shadan_fcb','mmehndiratta']

for user in user_lis:
    def get_user_id(user):
        request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (user, APP_ACCESS_TOKEN)
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


app = ClarifaiApp(api_key='eeaa1edfc07f45a7ad2c2b8551e4c2f6')

# get the general model
model = app.models.get('food-items-v1.0')
for user in user_lis:
    def get_user_post(user):
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
                model=app.models.get('food-items-v1.0')
                response = model.predict_by_url(url=image_url)
                for x in response['outputs'][0]['data']['concepts']:
                    print x['name'], x['value']
                    if x['value']>.7:
                        strr= x['name']
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


get_user_post(user)

