# Generated by Django 3.2.6 on 2021-09-24 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0005_auto_20210924_0951"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentgroup",
            name="_students",
            field=models.TextField(
                blank=True,
                help_text="V vsako vrstico vnesite ime enega učenca.",
                verbose_name="učenci",
            ),
        ),
    ]
