from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination


from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.permissions import GoalPermissions
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [GoalPermissions]


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.ARCHIVED
        instance.save()
        return instance


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ["due_date", "priority"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)
