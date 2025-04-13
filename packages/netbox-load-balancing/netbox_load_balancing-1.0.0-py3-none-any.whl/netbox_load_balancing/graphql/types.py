from typing import Annotated, List

import strawberry
import strawberry_django

from netbox.graphql.types import NetBoxObjectType
from ipam.graphql.types import IPAddressType
from tenancy.graphql.types import TenantType

from netbox_load_balancing.models import (
    LBService,
    Listener,
    HealthMonitor,
    Pool,
    Member,
)

from .filters import (
    NetBoxLoadBalancerLBServiceFilter,
    NetBoxLoadBalancerListenerFilter,
    NetBoxLoadBalancerHealthMonitorFilter,
    NetBoxLoadBalancerPoolFilter,
    NetBoxLoadBalancerMemberFilter,
)


@strawberry_django.type(
    LBService, fields="__all__", filters=NetBoxLoadBalancerLBServiceFilter
)
class NetBoxLoadBalancerLBServiceType(NetBoxObjectType):
    tenant: Annotated["TenantType", strawberry.lazy("tenancy.graphql.types")] | None
    name: str
    reference: str
    disabled: bool


@strawberry_django.type(
    Listener, fields="__all__", filters=NetBoxLoadBalancerListenerFilter
)
class NetBoxLoadBalancerListenerType(NetBoxObjectType):
    name: str
    service: (
        Annotated[
            "NetBoxLoadBalancerLBServiceType",
            strawberry.lazy("netbox_load_balancing.graphql.types"),
        ]
        | None
    )
    port: int
    protocol: str
    source_nat: bool
    use_proxy_port: bool
    max_clients: int
    max_requests: int
    client_timeout: int
    server_timeout: int
    client_keepalive: bool
    surge_protection: bool
    tcp_buffering: bool
    compression: bool


@strawberry_django.type(
    HealthMonitor, fields="__all__", filters=NetBoxLoadBalancerHealthMonitorFilter
)
class NetBoxLoadBalancerHealthMonitorType(NetBoxObjectType):
    name: str
    template: str | None
    type: str
    monitor_url: str | None
    http_response: str | None
    monitor_host: str | None
    http_version: str
    monitor_port: int
    http_secure: bool
    http_response_codes: List[int] | None
    probe_interval: int | None
    response_timeout: int | None
    disabled: bool


@strawberry_django.type(Pool, fields="__all__", filters=NetBoxLoadBalancerPoolFilter)
class NetBoxLoadBalancerPoolType(NetBoxObjectType):
    listeners: (
        List[
            Annotated[
                "NetBoxLoadBalancerListenerType",
                strawberry.lazy("netbox_load_balancing.graphql.types"),
            ]
        ]
        | None
    )
    name: str
    algorythm: str
    session_persistence: str
    backup_persistence: str
    persistence_timeout: int
    backup_timeout: int
    member_port: int
    disabled: bool


@strawberry_django.type(
    Member, fields="__all__", filters=NetBoxLoadBalancerMemberFilter
)
class NetBoxLoadBalancerMemberType(NetBoxObjectType):
    ip_address: Annotated["IPAddressType", strawberry.lazy("ipam.graphql.types")] | None
    name: str
    reference: str
    disabled: bool
