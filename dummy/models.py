from django.db import models
from .connector import switch_lamp, set_level


class BaseLamp(models.Model):
    class LampTypes(models.IntegerChoices):
        LED = 1
        HALOGEN = 2
        COMMON = 3
        FLOURESCENT = 4

    is_switched_on = models.BooleanField(
        "On/Off Flag",
        blank=True,
        null=False,
        default=False
    )

    address = models.CharField(
        "Address",
        max_length=200,
        blank=False,
        null=False,
        unique=True,
        help_text="Unique device address"
    )

    lamp_type = models.IntegerField(
        "Type",
        choices=LampTypes.choices,
        blank=False,
        null=False
    )

    power = models.IntegerField(
        "Power",
        blank=True,
        null=True
    )

    colorful_temperature = models.IntegerField(
        "Color Temperature",
        blank=True,
        null=True
    )

    voltage = models.IntegerField(
        "Supply Voltage",
        blank=True,
        null=True
    )

    chandelier = models.ForeignKey(
        'Chandelier',
        on_delete=models.SET_NULL,
        related_name="%(class)ss",
        related_query_name="%(app_label)s_%(class)ss",
        blank=True,
        null=True
    )

    def switch_on(self):
        self.is_switched_on = switch_lamp(self.address, True)
        self.save()

    def switch_off(self):
        self.is_switched_on = switch_lamp(self.address, False)
        self.save()

    def __str__(self):
        return f"{self.id}. {self.address}: ON {self.is_switched_on}"

    class Meta:
        abstract = True


class SimpleLamp(BaseLamp):
    pass


class DimmableLamp(BaseLamp):
    level = models.IntegerField(
        "Brightness Level",
        blank=True,
        null=True
    )

    def set_level(self, level):
        self.level = set_level(self.address, level)


class Chandelier(models.Model):
    location = models.CharField(
        "Location",
        max_length=200,
        blank=False,
        null=False,
        unique=True
    )

    def all_lamps(self):
        return list(self.simplelamps.all()) + list(self.dimmablelamps.all())

    def switch_on(self):
        for lamp in self.all_lamps():
            lamp.switch_on()

    def switch_off(self):
        for lamp in self.all_lamps():
            lamp.switch_off()

    def __str__(self):
        return f"{self.id}. {self.location}"


class Airport(models.Model):
    iata_code = models.CharField(
        "IATA Airport Code",
        max_length=3,
        blank=False,
        null=False,
        unique=True
    )
    name = models.CharField(
        "Airport Name",
        max_length=30,
        blank=False,
        null=False,
        unique=True
    )


class Ticket(models.Model):
    airport_from = models.ForeignKey(
        'Airport',
        on_delete=models.PROTECT,
        related_name="departure_tickets",
        related_query_name="%(app_label)s_departure_tickets",
        blank=False,
        null=False,
    )

    airport_to = models.ForeignKey(
        'Airport',
        on_delete=models.PROTECT,
        related_name="arrival_tickets",
        related_query_name="%(app_label)s_arrival_tickets",
        blank=False,
        null=False,
    )
    direct_date_time = models.DateTimeField(
        "Departure Date/Time",
        blank=False,
        null=False,
    )
    return_date_time = models.DateTimeField(
        "Return Flight Date/Time",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        "Price",
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=10,
    )

    def get_return_date(self):
        try:
            return self.return_date_time.strptime("d.m.Y")
        except AttributeError:
            return None

    def get_return_time(self):
        if not self.return_date_time:
            return None
        return self.return_date_time.strptime("H:i")


class PassangerInfo(models.Model):
    firstname = models.CharField(
        "First Name",
        max_length=30,
        blank=False,
        null=False,
        unique=True,
    )
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )


