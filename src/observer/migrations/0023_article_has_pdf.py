# Generated by Django 3.2.18 on 2023-03-07 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observer', '0022_alter_article_has_digest'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='has_pdf',
            field=models.BooleanField(blank=True, help_text="Null/None means I don't know!", null=True),
        ),
    ]