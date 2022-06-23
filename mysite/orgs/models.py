from django.db import models
from django.db.models import Sum, Count


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def organizations(self):  # подсчет количества организаций для каждого клиента
        count = Organization.objects.filter(client_name=self.pk).aggregate(Count('id'))
        return count['id__count']

    def total_amount(self):  # подсчет суммы счетов по всем организациям для каждого клиента
        total = Bill.objects.filter(organization__in=Organization.objects.filter(client_name=self.pk)).aggregate(Sum('amount'))
        return total['amount__sum']


class Organization(models.Model):
    client_name = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    organization = models.CharField(max_length=100)

    def __str__(self):
        return self.organization

    class Meta:
        unique_together = ('client_name', 'organization')


class Bill(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    amount = models.FloatField()
    date = models.DateField()

    class Meta:
        unique_together = ('organization', 'number')
