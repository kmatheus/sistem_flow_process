# Generated by Django 4.0.6 on 2022-07-17 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_baixa_numero_maquinario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=300)),
                ('alt_text', models.CharField(max_length=300)),
            ],
        ),
    ]
