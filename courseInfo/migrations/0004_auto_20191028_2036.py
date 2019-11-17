# Generated by Django 2.2.1 on 2019-10-28 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseInfo', '0003_auto_20190927_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='registrations', to='courseInfo.Section'),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('semester', 'course', 'section_name')},
        ),
    ]