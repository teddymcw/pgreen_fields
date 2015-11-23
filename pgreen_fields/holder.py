# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import copy
import datetime
import decimal
import math
import uuid
import warnings
from base64 import b64decode, b64encode
from functools import total_ordering

from django import forms
from django.apps import apps
from django.conf import settings
from django.core import checks, exceptions, validators
# When the _meta object was formalized, this exception was moved to
# django.core.exceptions. It is retained here for backwards compatibility
# purposes.
from django.core.exceptions import FieldDoesNotExist  # NOQA
from django.db import connection, connections, router
from django.db.models.query_utils import QueryWrapper, RegisterLookupMixin
from django.utils import six, timezone
from django.utils.datastructures import DictWrapper
from django.utils.dateparse import (
    parse_date, parse_datetime, parse_duration, parse_time,
)
from django.utils.deprecation import (
    RemovedInDjango20Warning, warn_about_renamed_method,
)

from django.utils.encoding import (
    force_bytes, force_text, python_2_unicode_compatible, smart_text,
)
from django.utils.functional import Promise, cached_property, 
from django.utils.translation import ugettext_lazy as _





class DecimalField(Field):
    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must be a decimal number."),
    }
    description = _("Decimal number")

    def __init__(self, verbose_name=None, name=None, max_digits=None,
                 decimal_places=None, **kwargs):
        self.max_digits, self.decimal_places = max_digits, decimal_places
        super(DecimalField, self).__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        errors = super(DecimalField, self).check(**kwargs)

        digits_errors = self._check_decimal_places()
        digits_errors.extend(self._check_max_digits())
        if not digits_errors:
            errors.extend(self._check_decimal_places_and_max_digits(**kwargs))
        else:
            errors.extend(digits_errors)
        return errors

    # _check attributes omitted 
    
    @cached_property
    def validators(self):
        return super(DecimalField, self).validators + [
            validators.DecimalValidator(self.max_digits, self.decimal_places)
        ]

    def deconstruct(self):
        name, path, args, kwargs = super(DecimalField, self).deconstruct()
        if self.max_digits is not None:
            kwargs['max_digits'] = self.max_digits
        if self.decimal_places is not None:
            kwargs['decimal_places'] = self.decimal_places
        return name, path, args, kwargs

    def get_internal_type(self):
        return "DecimalField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return decimal.Decimal(value)
        except decimal.InvalidOperation:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    # format_number(self): omitted, also has been moved to utils.py 
    # ensures 'requisite number of digits and decimal places'

    def get_db_prep_save(self, value, connection):
        return connection.ops.adapt_decimalfield_value(self.to_python(value),
                self.max_digits, self.decimal_places)

    # inserted from django.db.backends.base.operations
    def adapt_decimalfield_value(self, value, max_digits, decimal_places):
        """
        Transforms a decimal.Decimal value to an object compatible with what is
        expected by the backend driver for decimal (numeric) columns.
        """
        return utils.format_number(value, max_digits, decimal_places)


    def get_prep_value(self, value):
        value = super(DecimalField, self).get_prep_value(value)
        return self.to_python(value)

    def formfield(self, **kwargs):
        defaults = {
            'max_digits': self.max_digits,
            'decimal_places': self.decimal_places,
            'form_class': forms.DecimalField,
        }
        defaults.update(kwargs)
        return super(DecimalField, self).formfield(**defaults)