# Generated by Django 5.0.7 on 2024-08-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0005_orden_documento_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='diario',
            name='documento_pdf',
            field=models.FileField(blank=True, null=True, upload_to='documentos_pdf/'),
        ),
    ]
