# TinyTurret

Because sometimes a <a href="https://github.com/getsentry/sentry" target="_blank">Sentry</a> is just too much.

### Introduction

Sometimes a full tracing and error exception solution is just too much, costs and complicates too much.
Tiny Turret is a minimum viable version of Sentry.

The realisation is that 90% of cases you just want to have `top` for exceptions that occur in your project; and you want to do this quick and easy; without having to setup register, API keys and tune various settings.

### Storage Design

Tiny Turret will always try it's absolute best to get your exception logged and stored. For this reason it writes to multiple storage engines, if it can't write to a storage engine it fails silenty. This is important for an error logger; as you storage engine could be the cause of the excption, and by using the best effort approach to recording you can have multiple tiers of reporting.

In other words; if you DB fails - you should still be able to see what happened via a secondary storage. Tiny turret will always try and write to all setup storage types; and always return from the first available storage type.

### Default Tiny Turret Settings

```python
BASE_TINY_TURRET_SETTINGS = {
    'MAX_EXCEPTION_PER_GROUP': 100,
    'MAX_EXCEPTION_GROUPS': 10,
    'CLEANUP_TRIGGER_RATE': 0.05,
    'IGNORE_STORAGE_ERRORS': True,
    'CAPTURE_LOCALS': True,
    'STORAGE_BACKENDS': [
        {
            'class': 'tinyturret.storage_backends.shelve_store.ShelveStore',
            'settings': {
                'path': '/tmp/'
            }
        }
    ]
}

```

### Supported Storage Types

* Shelve
* Django Cache
* Django DB

### Django Support and usage

Add tiny-turret to your *INSTALLED_APPS*.

```python
INSTALLED_APPS = [
    # ...
    "tiny-turret"
]
```

This will add `tinyturret.middleware.DjangoExceptionMiddleware` Middleware as you first middleware in your `MIDDLEWARE` setting - this ensures you can catch and log all exceptions in the request cycle.

#### Django settings
Setting TinyTurret settings via django can be done as follows:

```python
TINY_TURRET_SETTINGS = {
    'MAX_EXCEPTION_PER_GROUP': 2,
}
TINY_TURRET_SHOW_ADMIN_LINK = False
```

*TINY_TURRET_SHOW_ADMIN_LINK = True* enables show tiny-turret base interface on django admin. Be careful it overrides the default admin view.


Include tinyturret.urls in your urls.py:
```python
urlpatterns += [
    path('tiny-turret/', include('tinyturret.urls'))
]
```
