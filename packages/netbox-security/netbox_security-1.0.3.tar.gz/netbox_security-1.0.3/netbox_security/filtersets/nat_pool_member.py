import django_filters
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import NumericArrayFilter

from ipam.models import IPAddress, Prefix, IPRange
from ipam.choices import IPAddressStatusChoices

from netbox_security.models import (
    NatPool,
    NatPoolMember,
)


class NatPoolMemberFilterSet(NetBoxModelFilterSet):
    pool_id = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        field_name="pool",
        to_field_name="id",
        label=_("NAT Pool (ID)"),
    )
    pool = django_filters.ModelMultipleChoiceFilter(
        queryset=NatPool.objects.all(),
        field_name="pool",
        to_field_name="name",
        label=_("NAT Pool (Name)"),
    )
    status = django_filters.MultipleChoiceFilter(
        choices=IPAddressStatusChoices,
        required=False,
    )
    address = django_filters.ModelMultipleChoiceFilter(
        field_name="address",
        queryset=IPAddress.objects.all(),
        to_field_name="address",
        label=_("Address"),
    )
    address_id = django_filters.ModelMultipleChoiceFilter(
        field_name="address",
        queryset=IPAddress.objects.all(),
        to_field_name="id",
        label=_("Address (ID)"),
    )
    prefix = django_filters.ModelMultipleChoiceFilter(
        field_name="prefix",
        queryset=Prefix.objects.all(),
        to_field_name="prefix",
        label=_("Prefix"),
    )
    prefix_id = django_filters.ModelMultipleChoiceFilter(
        field_name="prefix",
        queryset=Prefix.objects.all(),
        to_field_name="id",
        label=_("Prefix (ID)"),
    )
    address_range = django_filters.ModelMultipleChoiceFilter(
        field_name="address_range",
        queryset=IPRange.objects.all(),
        to_field_name="start_address",
        label=_("IPRange (Start Address)"),
    )
    address_range_id = django_filters.ModelMultipleChoiceFilter(
        field_name="address_range",
        queryset=IPRange.objects.all(),
        to_field_name="id",
        label=_("IPRange (ID)"),
    )
    source_ports = NumericArrayFilter(field_name="source_ports", lookup_expr="contains")
    destination_ports = NumericArrayFilter(
        field_name="destination_ports", lookup_expr="contains"
    )

    class Meta:
        model = NatPoolMember
        fields = ["id", "name"]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(name__icontains=value)
        return queryset.filter(qs_filter)
