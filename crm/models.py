from django.db import models


class City(models.Model):
    title = models.CharField(verbose_name='city_name', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'city'
        verbose_name = 'city'
