from celery import shared_task

@shared_task
def send_push_notification(user_id, message=None, **kwargs):
    # For FCM/GCM and APNS the message input should be a dict like this:
    # message={"title" : "foo", "body" : "bar"}

    from push_notifications.models import APNSDevice, GCMDevice, WNSDevice, WebPushDevice

    message_data = {'message': message} if message is not None else {}
    message_data.update(kwargs)

    # send messages to all Apple devices
    apple_devices = APNSDevice.objects.filter(user__id=user_id)
    apple_devices.send_message(**message_data)

    # send messages to all Android devices
    android_devices = GCMDevice.objects.filter(user__id=user_id)
    android_devices.send_message(**message_data)

    # send messages to all Windows devices
    windows_devices = WNSDevice.objects.filter(user__id=user_id)
    windows_devices.send_message(**message_data)

    # send messages to all Web devices
    web_devices = WebPushDevice.objects.filter(user__id=user_id)
    web_devices.send_message(**message_data)

    pass
