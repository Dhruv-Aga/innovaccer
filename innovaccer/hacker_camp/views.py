# from django.shortcuts import render
# from django.http import HttpResponse,JsonResponse
# from twitter import *

# # Create your views here.
# def test(request):
# 	# twitter = Twitter(auth = OAuth(config.access_key,
#  #                  config.access_secret,
#  #                  config.consumer_key,
#  #                  config.consumer_secret))
	
# 	twitter = Twitter(auth = OAuth('4556636492-EaBSdrTnzRflBOUCIkb9PkOLtvNVktaePX8lL6Y',
#                   'vLJlA47q0AFksISE5u2a7PvtfLT8dRdGDKLZfucB1PyvG',
#                   'd3z0wqpOSFN9X04Zy0lj1d473',
#                   'qbCqPPUn1VeGT69D2azsL9SDGym2vjJg1FJr0Zhi57BLiUz9Co'))

# 	query = twitter.search.tweets(q = "377")

# 	print("Search complete (%.3f seconds)" % (query["search_metadata"]["completed_in"]))

# 	for result in query["statuses"]:
# 	    print("(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"]))
# 	return JsonResponse(data={'msg':'helo','data':query},status=200,safe=False)	



from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from django.http import JsonResponse,HttpResponse
import json
from .models import *
import csv


class listener(StreamListener):

	def on_data(self, data):
		all_data = json.loads(data)
		user=all_data['user']
		user_id=user['id']

		user_update_or_create = UserProfile.objects.update_or_create(user_id=user_id,defaults={'profile_image_url':user['profile_image_url'],'profile_background_image_url':user['profile_background_image_url'],'friends_count':user['friends_count'],'statuses_count':user['statuses_count'],'description':user['description'],'screen_name':user['screen_name'],'name':user['name'],'favourites_count':user['favourites_count'],'followers_count':user['followers_count'],'created_at':user['created_at'],'location':user['location']})
		
		user=UserProfile.objects.filter(user_id=user_id).values('id')
		tweet_update_or_create=Tweets.objects.update_or_create(tweet_id=all_data['id'],defaults={'lang':all_data['lang'],'retweet_count':all_data['retweet_count'],'source':all_data['source'],'user_id':UserProfile.objects.get(id=user[0]['id']),'text':all_data['text'],'timestamp_ms':all_data['timestamp_ms']})

		tweet=Tweets.objects.filter(tweet_id=all_data['id']).values('id')
		for ur in all_data['entities']['urls']:
			q_del=Urls.objects.filter(tweet_id=tweet[0]['id']).delete()
			q_url=Urls.objects.create(tweet_id=Tweets.objects.get(id=tweet[0]['id']),expanded_url=ur['expanded_url'],display_url=ur['display_url'],url=ur['url'])
		
		for um in all_data['entities']['user_mentions']:
			q_del=User_mentions.objects.filter(tweet_id=tweet[0]['id']).delete()
			q_url=User_mentions.objects.create(tweet_id=Tweets.objects.get(id=tweet[0]['id']),name=um['name'],screen_name=um['screen_name'],u_id=um['id'])
		
		for has in all_data['entities']['hashtags']:
			q_del=Hashtags.objects.filter(tweet_id=tweet[0]['id']).delete()
			q_url=Hashtags.objects.create(tweet_id=Tweets.objects.get(id=tweet[0]['id']),text=has['text'])
		
		return True

	def on_error(self, status):
	    print(status)


def api1(request):
	ckey="d3z0wqpOSFN9X04Zy0lj1d473"
	csecret="qbCqPPUn1VeGT69D2azsL9SDGym2vjJg1FJr0Zhi57BLiUz9Co"
	atoken="4556636492-EaBSdrTnzRflBOUCIkb9PkOLtvNVktaePX8lL6Y"
	asecret="vLJlA47q0AFksISE5u2a7PvtfLT8dRdGDKLZfucB1PyvG"

	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)


	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[request.GET['keyword']])


def api2(request):
	start=int(request.GET['start'])
	offset=int(request.GET['offset'])
	filter=json.loads(request.GET['data'])
	qry=Tweets.objects.filter(**filter).values()[start:start+offset]
	for q in qry:
		q['user']=UserProfile.objects.filter(id=q['user_id_id']).values()[0]
		q['urls']=list(Urls.objects.filter(tweet_id=q['id']).values())
		q['hashtags']=list(Hashtags.objects.filter(tweet_id=q['id']).values())
		q['user_mentions']=list(User_mentions.objects.filter(tweet_id=q['id']).values())
		
	return JsonResponse(data={'data':list(qry)},status=200,safe=False)	


def api3(request):
	start=int(request.GET['start'])
	offset=int(request.GET['offset'])
	filter=json.loads(request.GET['data'])
	qry=Tweets.objects.filter(**filter).values()[start:start+offset]
	for q in qry:
		q['user']=UserProfile.objects.filter(id=q['user_id_id']).values()[0]
		q['urls']=list(Urls.objects.filter(tweet_id=q['id']).values())
		q['hashtags']=list(Hashtags.objects.filter(tweet_id=q['id']).values())
		q['user_mentions']=list(User_mentions.objects.filter(tweet_id=q['id']).values())
		
	keys = qry[0].keys()
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="download.csv"'
	writer = csv.writer(response)

	writer.writerow(keys)
	for q in qry:
		writer.writerow(q.values())

	return response



# http://127.0.0.1:8000/api2/?data={"text__startswith":"the","retweet_count__gt":0,"source__contains":"Android","lang":"en","user_id__location__contains":"Pakistan","user_id__screen_name__endswith":"s"}&start=10&offset=20

# http://127.0.0.1:8000/api3/?data={"text__contains":"car"}&start=10&offset=20