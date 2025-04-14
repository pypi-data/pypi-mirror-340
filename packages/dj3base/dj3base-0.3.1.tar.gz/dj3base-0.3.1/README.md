# dj3base

English | [简体中文](README_ZH.md)

`dj3base` contains some small tools for `Django`.

## 1. Introduction

* `admin`: Use `OrderedAdminSite` to customize the order of apps and models.
* `views`: Use `PostJsonView` to handle POST-JSON-style requests.
* `utils`: Some utility functions.

## 2. Usage

### Install

```shell
pip install dj3base

```
### Examples

* OrderedAdminSite

```python
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.apps import AppConfig
from dj3base.admin.ordered_admin_site import OrderedAdminSite


class MyAdminSite(OrderedAdminSite):
    ordered_apps = {
        AppConfig: {
            "index": 1,
            "models": {
                Group: {"index": 1},
                User: {"index": 2},
            }
        }
    }


my_admin_site = OrderedAdminSite(name='my_admin')
my_admin_site.register(User, UserAdmin)
my_admin_site.register(Group, GroupAdmin)

# in urls.py
from django.urls import path

urlpatterns = [
    path('admin/', my_admin_site.urls),
]

```

* PostJsonView

```python
from dj3base.views import PostJsonView
from a3json_struct import struct


class RequestStruct(struct.JsonStruct):
    message: str = struct.CharField(min_length=1, max_length=10)

    
class EchoView(PostJsonView):
    request_struct_cls = RequestStruct

    def handle_post(self, request_struct: RequestStruct, custom_params: dict) -> dict:
        return {"message": f"hello {request_struct.message}"}

```
