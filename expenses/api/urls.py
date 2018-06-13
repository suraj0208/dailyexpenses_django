from django.conf.urls import url
from .api_views.TagViews import TagRUDView, TagCreateListView
from .api_views.ExpenseViews import ExpensesRUDView, ExpensesCreateListView
from .api_views.GeneralViews import GeneralViews

urlpatterns = [
    url(r'^tags/$', TagCreateListView.as_view(), name='tags-listcreate'),
    url(r'^tags/(?P<pk>\d+)/$', TagRUDView.as_view(), name='tags-rud'),

    url(r'^expenses/$', ExpensesCreateListView.as_view(), name='expenses-listcreate'),
    url(r'^expenses/(?P<pk>\d+)/$', ExpensesRUDView.as_view(), name='expenses-rud'),

    url(r'^db/general/$', GeneralViews.as_view(), name='general-list')
]
