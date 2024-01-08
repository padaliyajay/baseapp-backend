from celery import shared_task

@shared_task
def send_push_notification(user_id, data):
    from push_notifications.models import APNSDevice, GCMDevice, WNSDevice, WebPushDevice

    # send messages to all Apple devices
    apple_devices = APNSDevice.objects.filter(user__id=user_id)
    apple_devices.send_message(data)

    # send messages to all Android devices
    android_devices = GCMDevice.objects.filter(user__id=user_id)
    android_devices.send_message(data)

    # send messages to all Windows devices
    windows_devices = WNSDevice.objects.filter(user__id=user_id)
    windows_devices.send_message(data)

    # send messages to all Web devices
    web_devices = WebPushDevice.objects.filter(user__id=user_id)
    web_devices.send_message(data)

    pass
