import django_filters
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from tenancy.filtersets import TenancyFilterSet
from utilities.filters import (
    ContentTypeFilter,
    MultiValueCharFilter,
    MultiValueNumberFilter,
)

from ipam.models import IPAddress

from netbox_load_balancing.models import (
    LBService,
    LBServiceAssignment,
)


class LBServiceFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    disabled = django_filters.BooleanFilter()

    class Meta:
        model = LBService
        fields = ["id", "name", "description", "reference"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value)
            | Q(description__icontains=value)
            | Q(reference__icontains=value)
        )
        return queryset.filter(qs_filter)


class LBServiceAssignmentFilterSet(NetBoxModelFilterSet):
    assigned_object_type = ContentTypeFilter()
    service_id = django_filters.ModelMultipleChoiceFilter(
        queryset=LBService.objects.all(),
        label=_("LBService (ID)"),
    )
    ip_address = MultiValueCharFilter(
        method="filter_address",
        field_name="address",
        label=_("IP Address (Address)"),
    )
    ip_address_id = MultiValueNumberFilter(
        method="filter_address",
        field_name="pk",
        label=_("IP Address (ID)"),
    )

    class Meta:
        model = LBServiceAssignment
        fields = ("id", "service_id", "assigned_object_type", "assigned_object_id")

    def filter_address(self, queryset, name, value):
        if not (
            addresses := IPAddress.objects.filter(**{f"{name}__in": value})
        ).exists():
            return queryset.none()
        return queryset.filter(
            assigned_object_type=ContentType.objects.get_for_model(IPAddress),
            assigned_object_id__in=addresses.values_list("id", flat=True),
        )
