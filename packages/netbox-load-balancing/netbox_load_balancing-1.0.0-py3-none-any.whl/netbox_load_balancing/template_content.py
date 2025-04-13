from netbox.plugins import PluginTemplateExtension

from netbox_load_balancing.models import (
    LBServiceAssignment,
    PoolAssignment,
    HealthMonitorAssignment,
    MemberAssignment,
    HealthMonitor,
    Pool,
)

from netbox_load_balancing.tables import (
    LBServiceAssignmentTable,
    PoolAssignmentTable,
    HealthMonitorAssignmentTable,
    MemberAssignmentTable,
)


class IPAddressContextInfo(PluginTemplateExtension):
    models = ["ipam.ipaddress"]

    def right_page(self):
        """ """
        if self.context["config"].get("service_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("service_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("service_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        service_lists = LBServiceAssignment.objects.filter(lbservice=obj)
        service_table = LBServiceAssignmentTable(service_lists)
        return self.render(
            "netbox_load_balancing/assignments/service.html",
            extra_context={"related_service_table": service_table},
        )


class IPRangeContextInfo(PluginTemplateExtension):
    models = ["ipam.iprange"]

    def right_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("pool_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        pool_lists = PoolAssignment.objects.filter(iprange=obj)
        pool_table = PoolAssignmentTable(pool_lists)
        return self.render(
            "netbox_load_balancing/assignments/pool.html",
            extra_context={"related_pool_table": pool_table},
        )


class MemberContextInfo(PluginTemplateExtension):
    models = ["netbox_load_balancing.healthmonitor", "netbox_load_balancing.pool"]

    def right_page(self):
        """ """
        if self.context["config"].get("member_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("member_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("member_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        if isinstance(obj, HealthMonitor):
            member_lists = MemberAssignment.objects.filter(health_monitor=obj)
        elif isinstance(obj, Pool):
            member_lists = MemberAssignment.objects.filter(pool=obj)
        else:
            return ""
        member_table = MemberAssignmentTable(member_lists)
        return self.render(
            "netbox_load_balancing/assignments/member.html",
            extra_context={"related_member_table": member_table},
        )


class HealthMonitorContextInfo(PluginTemplateExtension):
    models = ["netbox_load_balancing.pool"]

    def right_page(self):
        """ """
        if self.context["config"].get("monitor_ext_page") == "right":
            return self.x_page()
        return ""

    def left_page(self):
        """ """
        if self.context["config"].get("monitor_ext_page") == "left":
            return self.x_page()
        return ""

    def full_width_page(self):
        """ """
        if self.context["config"].get("monitor_ext_page") == "full_width":
            return self.x_page()
        return ""

    def x_page(self):
        obj = self.context["object"]
        monitor_lists = HealthMonitorAssignment.objects.filter(health_monitor=obj)
        monitor_table = HealthMonitorAssignmentTable(monitor_lists)
        return self.render(
            "netbox_load_balancing/assignments/monitor.html",
            extra_context={"related_monitor_table": monitor_table},
        )


template_extensions = [
    IPAddressContextInfo,
    IPRangeContextInfo,
    MemberContextInfo,
    HealthMonitorContextInfo,
]
