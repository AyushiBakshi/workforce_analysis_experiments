# Generated by Django 2.1.3 on 2019-11-18 03:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20191118_0256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingchangerequest',
            name='prev_booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='change_booking_prev', to='booking.ScheduledBooking'),
        ),
    ]