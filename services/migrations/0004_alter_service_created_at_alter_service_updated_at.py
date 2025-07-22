import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_service_created_at_alter_service_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='service',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=False,
        ),
    ]
