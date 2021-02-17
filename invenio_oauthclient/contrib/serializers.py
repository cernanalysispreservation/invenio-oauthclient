# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2021 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""CERN Serializers."""

from __future__ import absolute_import, print_function
from marshmallow import Schema, fields


class CERNUserInfoSchema(Schema):
    """Schema for CERN general user info."""
    external_id = fields.Method('get_external_id', dump_only=True)
    email = fields.Method('get_email', dump_only=True)
    groups = fields.Method('get_groups', dump_only=True)
    profile = fields.Method('get_profile', dump_only=True)

    def get_external_id(self, obj):
        person_id = obj.get('PersonID', [None])
        external_id = obj.get('uidNumber', person_id)[0]
        return external_id

    def get_email(self, obj):
        return obj.get('EmailAddress', [None])[0]

    def get_groups(self, obj):
        from .cern import fetch_groups
        return fetch_groups(obj.get('Group', []))

    def get_profile(self, obj):
        return {
            'common_name': obj.get('CommonName', [None])[0],
            'display_name': obj.get('DisplayName', [None])[0],
            'first_name': obj.get('Firstname', [None])[0],
            'last_name': obj.get('Lastname', [None])[0],

            'department': obj.get('Department', [None])[0],
            'building': obj.get('Building', [None])[0],
            'home_institute': obj.get('HomeInstitute', [None])[0]
        }
