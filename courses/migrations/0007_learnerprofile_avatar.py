from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_learnerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='learnerprofile',
            name='avatar',
            field=models.ImageField(
                blank=True,
                upload_to='profile-pictures/%Y/%m/',
            ),
        ),
    ]
