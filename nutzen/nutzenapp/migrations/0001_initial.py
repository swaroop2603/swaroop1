# Generated by Django 4.2.4 on 2023-11-09 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('offer_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('offer_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutzenapp.offer_type')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nutzenapp.user')),
            ],
        ),
    ]
