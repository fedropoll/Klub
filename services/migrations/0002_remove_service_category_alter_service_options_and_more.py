from django.utils.timezone import now
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_userprofile_role_branch'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='category',
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.RemoveField(
            model_name='service',
            name='image',
        ),
        migrations.AddField(
            model_name='service',
            name='branch',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='services',
                to='main.branch',
                verbose_name='Филиал'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=now  # Важно: default - функция, возвращающая текущее время
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='duration_minutes',
            field=models.PositiveIntegerField(
                default=30,
                verbose_name='Длительность (мин)'
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='is_active',
            field=models.BooleanField(
                default=True,
                verbose_name='Активна'
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название услуги'),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
