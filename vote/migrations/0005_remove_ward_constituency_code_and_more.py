# Generated by Django 4.2.7 on 2024-06-15 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_alter_voter_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ward',
            name='constituency_code',
        ),
        migrations.RenameField(
            model_name='voter',
            old_name='id_serial_number',
            new_name='registration_number',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='voter',
            name='ward_code',
        ),
        migrations.DeleteModel(
            name='Constituency',
        ),
        migrations.DeleteModel(
            name='County',
        ),
        migrations.DeleteModel(
            name='Ward',
        ),
    ]
