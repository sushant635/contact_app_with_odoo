# Generated by Django 3.2.5 on 2021-07-11 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_id', models.CharField(max_length=50, null=True)),
                ('display_name', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]