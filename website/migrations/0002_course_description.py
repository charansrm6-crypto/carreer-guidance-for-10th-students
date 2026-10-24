from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
    ]
