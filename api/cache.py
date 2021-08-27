from rest_framework_extensions.key_constructor.constructors import (
    DefaultKeyConstructor
)
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    ListSqlQueryKeyBit,
    PaginationKeyBit
)
from django.utils.encoding import force_text
from django.utils import timezone
from django.core.cache import cache

class UpdatedAtKeyBit(KeyBitBase):

    def get_data(self, **kwargs):
        key = 'user_list_timestamp'
        value = cache.get(key, None)
        if not value:
            value = timezone.now()
            cache.set(key, value=value)
        return force_text(value)

class CustomListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = UpdatedAtKeyBit()
