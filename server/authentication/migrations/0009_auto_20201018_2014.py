# Generated by Django 3.1.2 on 2020-10-18 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20201004_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='description',
            field=models.CharField(blank=True, default='', help_text='Short user bio', max_length=500),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='picture',
            field=models.URLField(default='https://static.productionready.io/images/smiley-cyrus.jpg', help_text='Profile picture URL', max_length=2000),
        ),
    ]
