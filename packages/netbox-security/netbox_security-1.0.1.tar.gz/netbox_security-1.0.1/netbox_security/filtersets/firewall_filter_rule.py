import django_filters
from django.db.models import Q
from django.utils.translation import gettext as _

from netbox.filtersets import NetBoxModelFilterSet

from netbox_security.choices import (
    FirewallRuleFromSettingChoices,
    FirewallRuleThenSettingChoices,
)
from netbox_security.models import (
    FirewallFilterRule,
    FirewallFilter,
    FirewallRuleFromSetting,
    FirewallRuleThenSetting,
)


__all__ = (
    "FirewallFilterRuleFilterSet",
    "FirewallFilterRuleFromSettingFilterSet",
    "FirewallFilterRuleThenSettingFilterSet",
)


class FirewallFilterRuleFilterSet(NetBoxModelFilterSet):
    filter_id = django_filters.ModelMultipleChoiceFilter(
        field_name="filter",
        queryset=FirewallFilter.objects.all(),
        label=_("Firewall Filter (ID)"),
    )
    filter = django_filters.ModelMultipleChoiceFilter(
        field_name="filter__name",
        queryset=FirewallFilter.objects.all(),
        to_field_name="name",
        label=_("Firewall Filter (name)"),
    )

    class Meta:
        model = FirewallFilterRule
        fields = ["name", "description", "index"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value) | Q(description__icontains=value)
        return queryset.filter(qs_filter).distinct()


class FirewallFilterRuleFromSettingFilterSet(NetBoxModelFilterSet):
    key = django_filters.MultipleChoiceFilter(
        choices=FirewallRuleFromSettingChoices, null_value=None, label=_("Setting Name")
    )

    class Meta:
        model = FirewallRuleFromSetting
        fields = [
            "key",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(key__icontains=value)
        return queryset.filter(qs_filter).distinct()


class FirewallFilterRuleThenSettingFilterSet(NetBoxModelFilterSet):
    key = django_filters.MultipleChoiceFilter(
        choices=FirewallRuleThenSettingChoices, null_value=None, label=_("Setting Name")
    )

    class Meta:
        model = FirewallRuleThenSetting
        fields = [
            "key",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = Q(key__icontains=value)
        return queryset.filter(qs_filter).distinct()
