from rest_framework.routers import APIRootView
from netbox.api.viewsets import NetBoxModelViewSet

from netbox_load_balancing.models import (
    LBService,
    LBServiceAssignment,
    Listener,
    HealthMonitor,
    HealthMonitorAssignment,
    Pool,
    PoolAssignment,
    Member,
    MemberAssignment,
)

from .serializers import (
    LBServiceSerializer,
    LBServiceAssignmentSerializer,
    ListenerSerializer,
    HealthMonitorSerializer,
    HealthMonitorAssignmentSerializer,
    PoolSerializer,
    PoolAssignmentSerializer,
    MemberSerializer,
    MemberAssignmentSerializer,
)

from netbox_load_balancing.filtersets import (
    LBServiceFilterSet,
    LBServiceAssignmentFilterSet,
    ListenerFilterSet,
    HealthMonitorFilterSet,
    HealthMonitorAssignmentFilterSet,
    PoolFilterSet,
    PoolAssignmentFilterSet,
    MemberFilterSet,
    MemberAssignmentFilterSet,
)


class NetBoxLoadBalancerRootView(APIRootView):
    def get_view_name(self):
        return "NetBoxLoadBalancer"


class LBServiceViewSet(NetBoxModelViewSet):
    queryset = LBService.objects.prefetch_related("tenant", "tags")
    serializer_class = LBServiceSerializer
    filterset_class = LBServiceFilterSet


class LBServiceAssignmentViewSet(NetBoxModelViewSet):
    queryset = LBServiceAssignment.objects.all()
    serializer_class = LBServiceAssignmentSerializer
    filterset_class = LBServiceAssignmentFilterSet


class HealthMonitorViewSet(NetBoxModelViewSet):
    queryset = HealthMonitor.objects.prefetch_related("tags")
    serializer_class = HealthMonitorSerializer
    filterset_class = HealthMonitorFilterSet


class HealthMonitorAssignmentViewSet(NetBoxModelViewSet):
    queryset = HealthMonitorAssignment.objects.all()
    serializer_class = HealthMonitorAssignmentSerializer
    filterset_class = HealthMonitorAssignmentFilterSet


class PoolViewSet(NetBoxModelViewSet):
    queryset = Pool.objects.prefetch_related("tags")
    serializer_class = PoolSerializer
    filterset_class = PoolFilterSet


class PoolAssignmentViewSet(NetBoxModelViewSet):
    queryset = PoolAssignment.objects.all()
    serializer_class = PoolAssignmentSerializer
    filterset_class = PoolAssignmentFilterSet


class MemberViewSet(NetBoxModelViewSet):
    queryset = Member.objects.prefetch_related("tags")
    serializer_class = MemberSerializer
    filterset_class = MemberFilterSet


class MemberAssignmentViewSet(NetBoxModelViewSet):
    queryset = MemberAssignment.objects.all()
    serializer_class = MemberAssignmentSerializer
    filterset_class = MemberAssignmentFilterSet


class ListenerViewSet(NetBoxModelViewSet):
    queryset = Listener.objects.prefetch_related("tags")
    serializer_class = ListenerSerializer
    filterset_class = ListenerFilterSet
