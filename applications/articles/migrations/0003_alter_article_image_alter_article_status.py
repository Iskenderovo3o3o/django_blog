# Generated by Django 4.1.7 on 2023-03-23 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='aticles'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('CLOSE', 'Closed')], default='CLOSED', max_length=6),
        ),
    ]
