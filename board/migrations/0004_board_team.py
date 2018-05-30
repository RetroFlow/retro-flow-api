# Generated by Django 2.0.5 on 2018-05-30 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20180529_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='team',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='board', to='board.Team'),
        ),
    ]
