from django.contrib import admin, messages
from .models import Trigger, Followup, Rule
from django.utils import timezone
from django.db.models import Max
admin.site.site_header = "VISIT SCHEDULER CONFIG PAGE"


@admin.register(Rule)
class RulesConfigAdmin(admin.ModelAdmin):
    list_display = ('rule_name','threshold','threshold_type')
    list_editable = [
        'threshold'
    ]
    exclude = ('created_date','created_by','last_modified_date','last_modified_by','delete_ind',)
    ordering = ('rule_id',)
    search_fields = ('field',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return not request.user.is_anonymous and request.user.is_superuser

    def threshold_type(self,obj):
        return "in days"

    def get_queryset(self, request):
        qs = super(RulesConfigAdmin, self).get_queryset(request)
        return qs.exclude(rule_name__isnull = True).exclude(rule_name = "")

# @admin.register(Followup)
class FollowUpConfigAdmin(admin.ModelAdmin):
    list_display = (
        'trigger','next_triggers','closure_type'
    )
    list_editable = [
        'closure_type','next_triggers'
    ]
    exclude = ('created_date','created_by','last_modified_date','last_modified_by','delete_ind',)
    ordering = ('followup_id',)
    search_fields = ('next_triggers',)


    def has_add_permission(self, request):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_view_permission(self, request, obj=None):
        return request.user.is_admin


# @admin.register(Trigger)
class TriggerConfigAdmin(admin.ModelAdmin):
    list_display = ('label','level')
    list_editable = ['level']
    exclude = ('created_date','created_by','last_modified_date','last_modified_by','delete_ind',)
    ordering = ('trigger_id',)
    search_fields = ('label', 'description')
    list_display_links = None
    ordering = ('-level',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False