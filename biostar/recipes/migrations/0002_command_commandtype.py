# Generated by Django 2.2 on 2019-10-15 22:52

import biostar.recipes.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, max_length=1024, upload_to=biostar.recipes.models.images)),
                ('uid', models.CharField(max_length=10000, unique=True)),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_text', models.CharField(max_length=10000)),
                ('uid', models.CharField(max_length=10000, unique=True)),
                ('command', models.CharField(max_length=10000, null=True, unique=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.CommandType')),
            ],
        ),
    ]
