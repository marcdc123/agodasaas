# Generated by Django 4.1.7 on 2023-03-25 09:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0002_remove_agentscore_agent_remove_phonecall_agent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TCGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TeamDirector',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamManager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teamdirector')),
                ('tc_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tcgroup')),
            ],
        ),
        migrations.CreateModel(
            name='TeamCaptain',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teammanager')),
                ('tc_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tcgroup')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.agent')),
                ('team_captain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.teamcaptain')),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teamcaptain'),
        ),
        migrations.AddField(
            model_name='agent',
            name='tc_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.tcgroup'),
        ),
    ]
