from django.db.models import Lookup

class SplitAndContains(Lookup):
    lookup_name = 'scontains'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'FIND_IN_SET(%s,%s)' % (rhs, lhs), params

class SplitAndGT(Lookup):
    lookup_name = 'sgt'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'TIME(%s) > TIME(%s)' % (lhs, rhs), params

class SplitAndLT(Lookup):
    lookup_name = 'slt'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'TIME(%s) < TIME(%s)' % (lhs, rhs), params