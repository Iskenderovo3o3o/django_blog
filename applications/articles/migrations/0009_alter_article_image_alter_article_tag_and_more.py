# Generated by Django 4.1.7 on 2023-04-04 13:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0008_alter_rating_options_alter_rating_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(related_name='articles', to='articles.tag'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'article')},
        ),
    ]
