# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from dj3base.utils.request_utils import get_ip


THROTTLED_LOGIN_EXPIRED_RATE_SECONDS = 60 * 60
THROTTLED_LOGIN_MAX_ERROR_COUNT = 10


class ThrottledLoginForm(AuthenticationForm):
    expired_rate_seconds = getattr(
        settings, "THROTTLED_LOGIN_EXPIRED_RATE_SECONDS", THROTTLED_LOGIN_EXPIRED_RATE_SECONDS
    )
    max_error_count = getattr(settings, "THROTTLED_LOGIN_MAX_ERROR_COUNT", THROTTLED_LOGIN_MAX_ERROR_COUNT)

    def clean(self):
        # Check whether the error count of the IP has reached the max_error_count.
        ip = get_ip(self.request)
        cache_key = f"admin:login:error_count:{ip}"
        if cache.get(cache_key, 0) >= self.max_error_count:
            raise ValidationError(
                _("Too many incorrect login attempts. You will not be able to login for the time being!"),
                code="invalid",
            )

        try:
            cleaned_data = super().clean()
        except ValidationError as e:
            # Update the error count and expired time of the IP.
            try:
                count = cache.incr(cache_key)
            except ValueError:
                count = 1
            cache.set(cache_key, count, self.expired_rate_seconds)
            raise e

        # Login success, clear the error count of the IP.
        cache.delete(cache_key)
        return cleaned_data
