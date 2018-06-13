from __future__ import print_function
from __future__ import unicode_literals

from expenses.models import Expense
from expenses.models import Tag
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q, Sum
from expenses.api.permissions import Permissions
from django.db.models.functions import TruncDate, TruncMonth, TruncYear


class GeneralViews(generics.ListAPIView):
    permission_classes = [Permissions]

    def get(self, request, *args, **kwargs):
        query = Expense.objects \
            .annotate(month=TruncMonth('expense_date')) \
            .values('month') \
            .distinct()

        months = set()

        for q in query[:]:
            m = q['month'].month
            months.add(m)

        query = Expense.objects \
            .annotate(year=TruncYear('expense_date')) \
            .values('year') \
            .distinct()

        years = set()

        for q in query[:]:
            m = q['year'].year
            years.add(m)

        print(months, years)

        dict = {'available_months': months, 'available_years': years}

        return Response(dict)
