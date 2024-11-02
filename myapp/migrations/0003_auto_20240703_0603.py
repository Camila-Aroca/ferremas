# Generated by Django 3.2.12 on 2024-07-03 06:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_cliente_tarjeta_tipotarjeta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarjeta',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tarjeta',
            name='nombre',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(message='El correo electrónico debe ser válido y tener una estructura correcta.')]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='cvv',
            field=models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(code='invalid_cvv', message='El CVV debe tener 3 o 4 dígitos.', regex='^\\d{3,4}$')]),
        ),
        migrations.AlterField(
            model_name='tarjeta',
            name='numero_tarjeta',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(code='invalid_card_number', message='El número de tarjeta debe tener 16 dígitos.', regex='^\\d{16}$')]),
        ),
    ]
