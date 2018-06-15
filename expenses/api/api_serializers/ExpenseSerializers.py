from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ( 'id', 'expense_name', 'expense_amount', 'expense_tag', 'expense_date')
        #fields = '__all__'
