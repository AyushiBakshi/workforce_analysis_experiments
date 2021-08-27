
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.models import User
from django.contrib.auth.models import Group
from alerts.models import Notification

class_user_map = {
    'Notification':'recipient',
    'ScheduledBooking':'service_user',
    'SuWeeklyBooking':'service_user',
    'BookingChangeRequest': 'service_user'
}

def notify_to_sync(instance=None,requester=None, instance_name=None, trigerred_from_bg=False):
    if trigerred_from_bg:
        from utils.helpers import UrlHelper
        is_success, token = UrlHelper.get_token(email='sys@hcms.com', password='hcms@sys')
        print(token)
        if is_success:
            url = 'notify_to_sync'
            UrlHelper.call_api(token=token,
                               relative_url=url,
                               method='POST',
                               payload={'instance_name': instance_name})

    else:
        channel_layer = get_channel_layer()
        groups = Group.objects.all()
        if not instance and not instance_name : return
        if instance_name:
            for group in groups:
                short_name = User.SHORT_NAMES.get(group.name,None)
                if not short_name: continue
                async_to_sync(channel_layer.group_send)(
                    short_name,
                    {
                        'type': 'data.change',
                        'message': {
                            'object_id': None,
                            'object_type': instance_name,
                            'user_name': None,
                            'user_type': None,
                            'requester': requester
                        }
                    }
                )
        else:

            instance = instance if type(instance) == list else [instance]

            msg = []

            for group in groups:
                short_name = User.SHORT_NAMES.get(group.name,None)
                if not short_name: continue
                for i in instance:
                    if not i: continue
                    user_identifier = class_user_map.get(type(i).__name__,'user')
                    user = getattr(i,user_identifier,None) if type(i) != User else i
                    user_name = user.user_name if user else None
                    user_type = user.group if user else None

                    async_to_sync(channel_layer.group_send)(
                        short_name,
                        {
                            'type': 'data.change',
                            'message': {
                                'object_id': i.pk,
                                'object_type': type(i).__name__,
                                'user_name': user_name,
                                'user_type': user_type,
                                'requester': requester
                            }
                        }
                    )

def notify_new_notification(instance):
    from api.serializers.notification_serializer import NotificationListSerializer

    channel_layer = get_channel_layer()
    channel_name = instance.recipient.channel_name
    if channel_name:
        data = NotificationListSerializer(
                Notification.objects.filter(notification_id = instance.pk),
                many=True
                ).data
        if data:
            async_to_sync(channel_layer.send)(
                channel_name,
                {
                    'type': 'new.notification',
                    'message': data[0]
                }
            )
