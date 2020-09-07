# Generated by Django 3.0.3 on 2020-07-30 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0004_auto_20200730_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='yelpReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=10)),
                ('comment', models.TextField()),
                ('timeCreated', models.DateTimeField()),
                ('tag', models.TextField(default='')),
                ('yelpBusinessId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.ApiMap')),
            ],
        ),
    ]
