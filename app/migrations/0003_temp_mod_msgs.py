# Generated by Django 5.1.6 on 2025-02-12 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_mod_msgs_create_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp_mod_msgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('if_user', models.BooleanField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('msg', models.TextField()),
            ],
        ),
    ]
