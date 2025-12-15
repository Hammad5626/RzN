from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.flag} {self.name}"

    def has_multiple_timezones(self):
        return self.timezones.count() > 1

class Timezone(models.Model):
    country = models.ForeignKey(Country, related_name='timezones', on_delete=models.CASCADE)
    zone_name = models.CharField(max_length=100)
    gmt_offset = models.IntegerField()
    gmt_offset_name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.zone_name} ({self.gmt_offset_name})"

class Player(models.Model):
    name = models.CharField(max_length=100)
    hq_level = models.IntegerField()
    power = models.BigIntegerField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    timezone = models.ForeignKey(Timezone, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_key_player = models.BooleanField(default=False)

    def __str__(self):
        return self.name
