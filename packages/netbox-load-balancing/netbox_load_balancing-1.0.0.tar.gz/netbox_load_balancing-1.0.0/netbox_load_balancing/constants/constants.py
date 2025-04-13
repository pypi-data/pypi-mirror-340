"""
Constants for filters
"""

from django.db.models import Q

SERVICE_ASSIGNMENT_MODELS = Q(
    Q(app_label="ipam", model="ipaddress"),
)

POOL_ASSIGNMENT_MODELS = Q(
    Q(app_label="ipam", model="iprange"),
)

HEALTH_MONITOR_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_load_balancing", model="pool"),
)

MEMBER_ASSIGNMENT_MODELS = Q(
    Q(app_label="netbox_load_balancing", model="pool"),
    Q(app_label="netbox_load_balancing", model="healthmonitor"),
)
