===========
Python Push Notification Manager
===========

Current State
=============

| This library is still in its very early stages.
| I expect to completely support the first two platforms for December.

10/2/2012:
_________
| Now we support "ping" pushes to Android GCMs and Blackberries devices.
| A "ping" push is a push which carries no content, for GCM this means use collapse_key.
| These features are under development and not widely tested.
| Theoretically is possible to send push with content.

The demo application is already under development, this has:

* A Django Server that manages the devices and sends the pushes.
* The basic example of an Android App.
* The basic example of a Blackberry App.

As I said the demo application is under development so is not is not yet published, but when the basic examples are ready I will provide the link to the repo.


Platforms:
==========
At short term:

1. Android GCM
2. Blackberry Push Protocol.
3. iOS APN

At long term:

4. Windows Phone 7
5. Symbian
6. Browsers (With sockets)
7. Windows 8

Usage (for now):
================

Send a ping Push::

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

    bb_push_status = status_dict[BBPushService.type]
    print 'Blackberry Status Code %i:\n%s\n'\
        % (bb_push_status.code, bb_push_status.description)

    gcm_push_status = status_dict[GCMPushService.type]
    print 'GCM Status Code %i:\n' % (gcm_push_status.code)
