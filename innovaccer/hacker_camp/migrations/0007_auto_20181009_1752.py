# Generated by Django 2.1.1 on 2018-10-09 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hacker_camp', '0006_auto_20181009_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('tweet_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='T1', to='hacker_camp.Tweets')),
            ],
            options={
                'managed': True,
                'db_table': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expanded_url', models.CharField(max_length=1000)),
                ('display_url', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=1000)),
                ('tweet_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='T3', to='hacker_camp.Tweets')),
            ],
            options={
                'managed': True,
                'db_table': 'Urls',
            },
        ),
        migrations.CreateModel(
            name='User_mentions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('screen_name', models.CharField(max_length=1000)),
                ('u_id', models.BigIntegerField()),
                ('tweet_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='T2', to='hacker_camp.Tweets')),
            ],
            options={
                'managed': True,
                'db_table': 'User_mentions',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image_url',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]