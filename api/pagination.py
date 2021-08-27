from rest_framework.pagination import LimitOffsetPagination, _positive_int

class CustomPagination(LimitOffsetPagination):
    max_limit = 20000
    default_limit = 20000

    # Same as get_limit except strict=False
    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    strict=False,
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit

class CandidatePagination(LimitOffsetPagination):
    max_limit = 1000
    default_limit = 10
