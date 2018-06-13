from __future__ import print_function
from __future__ import unicode_literals

from expenses.models import Expense
from expenses.models import Tag
from expenses.api.api_serializers.ExpenseSerializers import ExpenseSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth
from expenses.api.permissions import Permissions


class ExpensesCreateListView(generics.mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ExpenseSerializer
    permission_classes = [Permissions]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        qs = Expense.objects.all()
        query = self.request.GET.get("q")

        if query is not None:
            date_splits = query.split("-")

            if len(date_splits) == 3:
                splitTotal = query.split('_')

                if len(splitTotal) == 2 and splitTotal[1] == 'total':
                    qs = qs.filter(
                        Q(expense_date=splitTotal[0])
                    ).values('expense_date')
                    print(qs)
                    qs = qs.annotate(total=Sum('expense_amount'))
                    print(qs)

                    return qs[0] if len(qs) > 0 else {'total': 0}

                qs = qs.filter(
                    Q(expense_date=query)
                ).distinct()
                return qs

            elif len(date_splits) == 2:
                year = date_splits[0]
                month = date_splits[1]

                month_split = month.split("_")

                if len(month_split) == 2:
                    month = month_split[0]
                    qs = qs.filter(
                        Q(expense_date__year=year,
                          expense_date__month=month)
                    )
                    qs = qs \
                        .annotate(month=TruncMonth('expense_date')) \
                        .values('month') \
                        .annotate(total=Sum('expense_amount'))

                    return qs[0] if len(qs) > 0 else {'total': 0}

                qs = qs.filter(
                    Q(expense_date__year=year,
                      expense_date__month=month)
                )

                qs = qs.values('expense_date') \
                    .annotate(date_expense=Sum('expense_amount')) \
                    .order_by('expense_date')

        return qs

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        if query is not None:
            date_splits = query.split("-")
            total_splits = query.split("_")

            if len(date_splits) == 2 or (len(date_splits) == 3 and len(total_splits) == 2):
                res = self.get_queryset()

                if not isinstance(res, dict):
                    res = res[:]

                return Response(status=200, data=res)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data

        request_tag = data['expense_tag']

        tags = Tag.objects.all()

        found_tag = tags.filter(
            Q(tag_name=request_tag)
        ).first()

        if found_tag is None:
            # ToDo
            print("unknown tag in request")
        else:
            request.data['expense_tag'] = found_tag.id
        return self.create(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        result = Expense.objects.all().delete()
        if result[0] == 0:
            print("nothing to be deleted")
            return Response(status=404)

        return Response(status=301)


class ExpensesRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [Permissions]

    def get_queryset(self):
        qs = Expense.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(expense_name__icontains=query)
            ).distinct()

        return qs
