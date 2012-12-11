===========
Python Push Notification Manager
===========
| Python Push is a Python server-side library for sending Push Notifications to multiple mobile platforms.
| This library is still in its very early stages, for now it is only supported Ping Pushes, which means that no data is sent in the push, but the `Demo Application <https://github.com/maxrevilo/python-push-demo/>`_ shows a way to handle this using post syncronization wich is even better than send the info in the push.

Supported Platforms:
==========
1. Android GCM
2. Blackberry Push Protocol.

In development:
_______________
3. iOS APN
4. Windows Phone 7
5. Symbian
6. Browsers (With sockets)
7. Windows 8

Usage:
======
For a full project with mobile apps see the `Demo Application <https://github.com/maxrevilo/python-push-demo/>`_.

Sending a ping Push::

    from python_push.push_manager import PushManager
    from python_push.gcm.gcm_push_service import GCMPushService
    from python_push.blackberry.bb_push_service import BBPushService
    from python_push.message import Message
    from python_push.device import Device

    push_manager = PushManager([
        GCMPushService({'api_id': 'GCM API KEY'}),
        BBPushService({'api_id': 'BLACKBERRY APP ID', 'password': 'BLACKBERRY APP PASSWORD'})
    ])

    msg = Message()
    device_list = [
        Device(BBPushService.type, 'BLACKBERRY DEVICE PIN'),
        Device(GCMPushService.type, 'GCM DEVICE TOKEN')
    ]

    status_dict = push_manager.send(msg, device_list)

    for type, status in status_dict.iteritems():
            print 'Service %s: Status %i, Content %s\n' % (type, status.code, status.raw)


Updates:
=========
12/11/2012:
_________
| The demo proyect is ready and has its own repo: https://github.com/maxrevilo/python-push-demo
| It features a Django Server using Python Push and four navite apps, two of Android and Two of Blackberry.

10/2/2012:
_________
| Now we support "ping" pushes to Android GCMs and Blackberries devices.
| A "ping" push is a push which carries no content, for GCM this means use collapse_key.
| These features are under development and not widely tested.
| Theoretically is possible to send push with content.