from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.BigIntegerField()
    location = models.CharField(max_length=1000,null=True)
    profile_image_url = models.CharField(max_length=1000,null=True)
    profile_background_image_url = models.CharField(max_length=1000,null=True)
    friends_count = models.IntegerField()
    statuses_count = models.IntegerField()
    description = models.TextField(null=True)
    screen_name = models.CharField(null=True,max_length=1000)
    name = models.CharField(max_length=500,null=True)
    favourites_count = models.IntegerField()
    followers_count = models.IntegerField()
    created_at = models.CharField(max_length=500,null=True)

    class Meta:
        managed = True
        db_table = 'user_profile'

class Tweets(models.Model):
    tweet_id = models.BigIntegerField(null=True)
    lang = models.CharField(max_length=100,null=True)
    retweet_count = models.IntegerField()
    source = models.CharField(max_length=1000,null=True)
    user_id = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    text = models.TextField(null=True)
    timestamp_ms = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'tweets'

class Hashtags(models.Model):
    tweet_id = models.ForeignKey(Tweets,on_delete=models.SET_NULL,null=True,related_name='T1')
    text=models.CharField(max_length=1000)
    class Meta:
        managed = True
        db_table = 'Hashtags'

class User_mentions(models.Model):
    tweet_id = models.ForeignKey(Tweets,related_name='T2',on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=1000)
    screen_name=models.CharField(max_length=1000)
    u_id=models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'User_mentions'

class Urls(models.Model):
    tweet_id = models.ForeignKey(Tweets,related_name='T3',on_delete=models.SET_NULL,null=True)
    expanded_url=models.CharField(max_length=1000)
    display_url=models.CharField(max_length=1000)
    url=models.CharField(max_length=1000)
    
    class Meta:
        managed = True
        db_table = 'Urls'