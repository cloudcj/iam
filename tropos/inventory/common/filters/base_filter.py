# utils/filters/base_filter.py
from django_filters import rest_framework as filters
from django.db.models import Q

# ---------------------------------------------------------
# Generic multi-value IN filters
# ---------------------------------------------------------
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    """Allows ?id=1,2,3 → id__in=[1,2,3]"""
    pass

class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    """Allows ?field=val1,val2 → field__in=[val1, val2]"""
    pass

class BaseFilter(filters.FilterSet):
    """
    Reusable base filter for Django REST Framework & Django.
    
    Features:
    - search_fields: list of fields to OR-search with ?search=
    - add_search_field → partial match (icontains)
    - add_exact_field → exact match
    - add_number_field → exact numeric match
    - add_number_list_field → Multi-value numeric (NumberInFilter)
    - add_string_list_field → Multi-value string (CharInFilter)
    """

    # fields included in OR search
    search_fields = []

    # global OR-search param (like DRF SearchFilter)
    search = filters.CharFilter(method="filter_search")

    class Meta:
        abstract = True

    # ---------------------------------------------------------
    # Global search handler (?search=...)
    # ---------------------------------------------------------

    def filter_search(self, queryset, name, value):
        """
        OR search across all fields defined in search_fields.
        """
        if not value or not getattr(self, "search_fields", []):
            return queryset
        q = Q()
        for field in self.search_fields:
            q |= Q(**{f"{field}__icontains": value})

        return queryset.filter(q)


    # =========================================================
    # Dynamic Field Builders
    # =========================================================
    @classmethod
    def _init_base_filters(cls):
        """Ensure base_filters exists before dynamic assignment."""
        if not hasattr(cls, "base_filters"):
            cls.base_filters = {}

    @classmethod
    def add_search_field(cls, field_name, param_name=None):
        """
        Dynamically add a search field (partial match)
        """
        param_name = param_name or field_name
        # Ensure base_filters exists
        cls.base_filters.setdefault(param_name, filters.CharFilter(
            field_name=field_name,
            lookup_expr="icontains"
        ))

    @classmethod
    def add_search_list_field(cls, *fields):
        """
        Add one or more multi-value partial search fields in a single call.

        Each field can be:
        - string: field_name = param_name (query param defaults to field_name)
        - tuple: (field_name, param_name) → custom query param

        Example usage:

            add_search_list_field("name")  
            add_search_list_field("name", "description")  
            add_search_list_field(("server_name", "name"))
        
        URL example:
            ?name=ncr,az → matches 'ncr' OR 'az' in server_name
        """
        cls._init_base_filters()

        for f in fields:
            if isinstance(f, (tuple, list)):
                field_name = f[0]
                param_name = f[1] if len(f) > 1 else None
            else:
                field_name = f
                param_name = None

            param_name = param_name or field_name

            def _filter(qs, name, value, field=field_name):
                if not value:
                    return qs
                terms = [v.strip() for v in value.split(",") if v.strip()]
                if not terms:
                    return qs
                q = Q()
                for term in terms:
                    q |= Q(**{f"{field}__icontains": term})
                return qs.filter(q)

            cls.base_filters[param_name] = filters.CharFilter(method=_filter)


    # @classmethod
    # def add_search_list_field(cls, field_name, param_name=None):
    #     """
    #     Multi-value partial search field
    #     Example:
    #     ?name=ncr,az → name__icontains=ncr OR name__icontains=az
    #     """
    #     cls._init_base_filters()
    #     param = param_name or field_name

    #     def _filter(qs, name, value):
    #         if not value:
    #             return qs

    #         terms = [v.strip() for v in value.split(",") if v.strip()]
    #         if not terms:
    #             return qs

    #         q = Q()
    #         for term in terms:
    #             q |= Q(**{f"{field_name}__icontains": term})

    #         return qs.filter(q)

    #     cls.base_filters[param] = filters.CharFilter(method=_filter)

    # @classmethod
    # def add_exact_field(cls, field_name, param_name=None):
    #     """
    #     Dynamically add an exact match field (buttons/dropdowns)
    #     """
    #     param_name = param_name or field_name
    #     cls.base_filters.setdefault(param_name, filters.CharFilter(
    #         field_name=field_name,
    #         lookup_expr="exact"
    #     ))

    @classmethod
    def add_exact_field(cls, *fields):
        """
        fields can be:
        - strings: param_name = field_name
        - tuples: (field_name, param_name)
        """
        cls._init_base_filters()
        for f in fields:
            if isinstance(f, (tuple, list)):
                field_name = f[0]
                param_name = f[1] if len(f) > 1 else None
            else:
                field_name = f
                param_name = None

            param_name = param_name or field_name

            cls.base_filters[param_name] = filters.CharFilter(
                field_name=field_name,
                lookup_expr="exact"
            )


    @classmethod
    def add_number_field(cls, field_name, param_name=None):
        """
        Dynamically add an exact number field (IDs, related fields)
        """
        param_name = param_name or field_name
        cls.base_filters.setdefault(param_name, filters.NumberFilter(
            field_name=field_name,
            lookup_expr="exact"            
        ))
    
    # @classmethod
    # def add_number_list_field(cls, field_name, param_name=None):
    #     """
    #     Add multi-value numeric match
    #     Example: ?rack_id=1,3,7 → rack_id__in=[1,3,7]
    #     """
    #     cls._init_base_filters()
    #     param = param_name or field_name
    #     cls.base_filters[param] = NumberInFilter(
    #         field_name=field_name,
    #         lookup_expr="in"
    #     )

    @classmethod
    def add_number_list_field(cls, *fields):
        """
        Add one or more multi-value numeric (IN) filters in one line.

        Each field can be:
        - string: field_name = param_name (query param defaults to field_name)
        - tuple: (field_name, param_name) → allows custom query param

        Example usage:

            add_number_list_field('id', 'fan_units')
            add_number_list_field(('number_of_interfaces','active_interfaces'))
        """
        cls._init_base_filters()
        for f in fields:
            # Handle tuple: (field_name, param_name)
            if isinstance(f, (tuple, list)):
                field_name = f[0]
                param_name = f[1] if len(f) > 1 else None
            else:
                field_name = f
                param_name = None

            param_name = param_name or field_name
            cls.base_filters[param_name] = NumberInFilter(
                field_name=field_name,
                lookup_expr="in"
            )


    # @classmethod
    # def add_string_list_field(cls, field_name, param_name=None):
    #     """Multi-value string match (?field=active,inactive)"""
    #     cls._init_base_filters()
    #     param = param_name or field_name
    #     cls.base_filters[param] = CharInFilter(
    #         field_name=field_name,
    #         lookup_expr="in"
    #     )

    @classmethod
    def add_string_list_field(cls, *fields):
        """
        Add one or more multi-value string (IN) filters in one line.

        Each field can be:
        - string: field_name = param_name (query param defaults to field_name)
        - tuple: (field_name, param_name) → allows custom query param

        Example usage:

            add_string_list_field('status', 'type')
            add_string_list_field(('appliance_type__name','type'))
        """
        cls._init_base_filters()
        
        for f in fields:
            # Handle tuple: (field_name, param_name)
            if isinstance(f, (tuple, list)):
                field_name = f[0]
                param_name = f[1] if len(f) > 1 else None
            else:
                field_name = f
                param_name = None

            param_name = param_name or field_name
            cls.base_filters[param_name] = CharInFilter(
                field_name=field_name,
                lookup_expr="in"
            )


# # filters.py (or same file as your viewset)
# import django_filters

# class BaseFilter(django_filters.FilterSet):
#     """
#     Reusable filter base:
#     - Search fields (partial match) -> use icontains
#     - Exact match fields (buttons, dropdowns) -> use exact
#     """
    
#     @classmethod
#     def add_search_field(cls, field_name, param_name=None):
#         """
#         Dynamically add a search field (partial match)
#         """
#         param_name = param_name or field_name
#         setattr(cls, param_name, django_filters.CharFilter(field_name=field_name, lookup_expr="icontains"))
    
#     @classmethod
#     def add_exact_field(cls, field_name, param_name=None):
#         """
#         Dynamically add an exact match field (buttons/dropdowns)
#         """
#         param_name = param_name or field_name
#         setattr(cls, param_name, django_filters.CharFilter(field_name=field_name, lookup_expr="exact"))
    
#     @classmethod
#     def add_number_field(cls, field_name, param_name=None):
#         """
#         Add exact number field (for ids, related fields)
#         """
#         param_name = param_name or field_name
#         setattr(cls, param_name, django_filters.NumberFilter(field_name=field_name, lookup_expr="exact"))