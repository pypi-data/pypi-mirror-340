from typing import List

import strawberry
import strawberry_django

from .types import (
    NetBoxLoadBalancerLBServiceType,
    NetBoxLoadBalancerListenerType,
    NetBoxLoadBalancerPoolType,
    NetBoxLoadBalancerMemberType,
    NetBoxLoadBalancerHealthMonitorType,
)


@strawberry.type(name="Query")
class NetBoxLoadBalancerLBServiceQuery:
    netbox_load_balancing_lbservice: NetBoxLoadBalancerLBServiceType = (
        strawberry_django.field()
    )
    netbox_load_balancing_lbservice_list: List[NetBoxLoadBalancerLBServiceType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancerListenerQuery:
    netbox_load_balancing_listener: NetBoxLoadBalancerListenerType = (
        strawberry_django.field()
    )
    netbox_load_balancing_listener_list: List[NetBoxLoadBalancerListenerType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancerPoolQuery:
    netbox_load_balancing_pool: NetBoxLoadBalancerPoolType = strawberry_django.field()
    netbox_load_balancing_pool_list: List[NetBoxLoadBalancerPoolType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancerMemberQuery:
    netbox_load_balancing_member: NetBoxLoadBalancerMemberType = (
        strawberry_django.field()
    )
    netbox_load_balancing_member_list: List[NetBoxLoadBalancerMemberType] = (
        strawberry_django.field()
    )


@strawberry.type(name="Query")
class NetBoxLoadBalancerHealthMonitorQuery:
    netbox_load_balancing_healthmonitor: NetBoxLoadBalancerHealthMonitorType = (
        strawberry_django.field()
    )
    netbox_load_balancing_healthmonitor_list: List[
        NetBoxLoadBalancerHealthMonitorType
    ] = strawberry_django.field()
