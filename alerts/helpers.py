from django.utils import timezone
from utils.models import Data
from channel.sync import notify_to_sync
from alerts.models import Notification
from users.models import Address
from cw.models import Certificate
import copy

class NotificationMarker:

    def overdue_address_actions_mark_unresolved():
        notifications = Notification.objects.filter(info_trigger__label__in=['address_change_unhandled_bookings',
                                                                             'address_restore_unhandled_bookings'],
                                                    is_unresolved=False,
                                                    ).exclude(
            notification_status_mc_id=Data.code('NOTIFICATION_STATUS', 'Closed')
        )
        if notifications:
            address_id_list = list(notifications.values_list('action_object_object_id', flat=True))
            unresolved_address_id_list = list(Address.objects.filter(address_id__in=address_id_list,
                                                                     handle_bookings_until__lt=timezone.now(),
                                                                     bookings_handled=False).values_list('address_id',
                                                                                                         flat=True))
            if unresolved_address_id_list:
                notifications_to_update = notifications.filter(action_object_object_id__in=unresolved_address_id_list)
                notifications_to_sync = copy.copy(notifications_to_update)
                notifications_to_update.update(
                    notification_status_mc_id=Data.code('NOTIFICATION_STATUS', 'Closed'),
                    closure_type_mc_id=Data.code("NOTIFICATION_CLOUSURE_TYPE", "Force"),
                    closure_reason="Unresolved",
                    is_unresolved=True,
                    closed_date=timezone.now()
                )
                notify_to_sync(list(notifications_to_sync))


    def overdue_certificate_actions_mark_unresolved():
        notifications = Notification.objects.filter(info_trigger__label__in=['certificate_expiry_unhandled_bookings'],
                                                    is_unresolved=False,
                                                    ).exclude(
            notification_status_mc_id = Data.code("NOTIFICATION_STATUS", "Closed")
        )
        if notifications:
            certificate_id_list = list(notifications.values_list('action_object_object_id', flat=True))
            unresolved_certificate_id_list = list(Certificate.objects.filter(certificate_id__in=certificate_id_list,
                                                                             handle_bookings_until__lt=timezone.now(),
                                                                             bookings_handled=False).values_list(
                'certificate_id', flat=True))
            if unresolved_certificate_id_list:
                notifications_to_update = notifications.filter(action_object_object_id__in=unresolved_certificate_id_list)
                notifications_to_sync = copy.copy(notifications_to_update)
                notifications_to_update.update(
                    notification_status_mc_id=Data.code('NOTIFICATION_STATUS', 'Closed'),
                    closure_type_mc_id=Data.code("NOTIFICATION_CLOUSURE_TYPE", "Force"),
                    closure_reason="Unresolved",
                    is_unresolved=True,
                    closed_date = timezone.now()
                )
                notify_to_sync(list(notifications_to_sync))

    def mark_unresolved_by_action_object_id(action_object_id):
        notifications = Notification.objects.filter(action_object_object_id=action_object_id,
                                                    info_trigger__notification_purpose_mc_id=Data.code('NOTIFICATION_PURPOSE',
                                                                                         'Task'),
                                                    is_unresolved=False,
                                                    ).exclude(
            notification_status_mc_id=Data.code('NOTIFICATION_STATUS', 'Closed'))

        if notifications:
            for notification in notifications:
                notification.is_unresolved = True
                notification.notification_status_mc_id = Data.code("NOTIFICATION_STATUS", "Closed")
                notification.closure_type_mc_id = Data.code("NOTIFICATION_CLOUSURE_TYPE","Force")
                notification.closure_reason = "Unresolved Action"
                notification.closed_date = timezone.now()
                notification.save()
                notify_to_sync(notification)