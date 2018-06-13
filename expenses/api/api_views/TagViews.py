from __future__ import unicode_literals

from expenses.models import Tag
from expenses.api.api_serializers import TagSerliazers
from rest_framework import generics
from django.db.models import Q
from expenses.api.permissions import Permissions


class TagCreateListView(generics.mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = TagSerliazers.TagSerializer
    permission_classes = [Permissions]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        qs = Tag.objects.all()
        query = self.request.GET.get("q")

        if query is not None:
            qs = qs.filter(
                Q(tag_name__icontains=query)
            ).distinct()

        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)


class TagRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = Tag.objects.all()
    serializer_class = TagSerliazers.TagSerializer
    permission_classes = [Permissions]

    def get_queryset(self):
        qs = Tag.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(tag_name__icontains=query)
            ).distinct()

        return qs
