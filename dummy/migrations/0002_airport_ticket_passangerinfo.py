# Generated by Django 4.1.1 on 2022-10-14 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dummy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iata_code', models.CharField(max_length=3, unique=True, verbose_name='Airport IATA code')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Airport name')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direct_date_time', models.DateTimeField(verbose_name='Departure date/time')),
                ('return_date_time', models.DateTimeField(blank=True, null=True, verbose_name='Return flight date/time')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cost')),
                ('airport_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departure_tickets', related_query_name='%(app_label)s_departure_tickets', to='dummy.airport')),
                ('airport_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='arrival_tickets', related_query_name='%(app_label)s_arrival_tickets', to='dummy.airport')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=30, unique=True, verbose_name='First name')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dummy.ticket')),
            ],
        ),
    ]
