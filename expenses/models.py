from __future__ import unicode_literals

from django.db import models
from datetime import date
from django.conf import settings


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name


class Expense(models.Model):
    expense_name = models.CharField(max_length=50)
    expense_amount = models.FloatField()
    expense_date = models.DateField(default=date.today)
    expense_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    expense_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.expense_name

    @property
    def tag_name(self):
        return self.expense_tag.tag_name

    def has_permission(self, user):
        return user == self.expense_owner
