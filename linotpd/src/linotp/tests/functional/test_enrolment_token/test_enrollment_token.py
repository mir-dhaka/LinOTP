# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2018 KeyIdentity GmbH
#
#    This file is part of LinOTP server.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@keyidentity.com
#    Contact: www.linotp.org
#    Support: www.keyidentity.com
#


"""
Test the onetime token for the selfservice login
"""
import json
from linotp.tests import TestController

import unittest2


class TestRolloutToken(TestController):
    """
    Test the one time login token
    """

    def setUp(self):
        TestController.setUp(self)
        self.delete_all_policies()
        self.delete_all_token()
        self.delete_all_realms()
        self.delete_all_resolvers()
        self.create_common_resolvers()
        self.create_common_realms()

    def tearDown(self):
        TestController.tearDown(self)

    def user_service_login(self, user, password, otp):
        """
        """
        response, auth_cookie = self._user_service_login(
                                 auth_user=user,
                                 password=password,
                                 otp=otp)

        return response

    def validate_check(self, user, pin, password):
        params = {
            "user": user,
            "pass": pin+password
        }
        response = self.make_validate_request("check", params=params)

        return response

    # ---------------------------------------------------------------------- --

    def test_scope_both(self):
        """
        test token with both scopes defined
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)


        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token",
            "scope": json.dumps({
                "path": ["validate", "userservice"]})
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": true' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": true' in response, response)

        return

    def test_scope_both2(self):
        """
        test token with both scopes defined
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)


        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token"
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": true' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": true' in response, response)

        return

    def test_scope_selfservice(self):
        """
        test token with both scopes defined
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)

        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token",
            "scope": json.dumps({
                "path": ["userservice"]})
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": false' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": true' in response, response)

        return

    def test_scope_selfservice_alias(self):
        """
        test token with both scopes defined
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)

        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token",
            "rollout": "True"
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": false' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": true' in response, response)

        return

    def test_scope_validate(self):
        """
        test token with both scopes defined
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)

        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token",
            "scope": json.dumps({
                "path": ["validate"]})
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": true' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": false' in response, response)

        return

    def test_enrollment_janitor(self):
        """
        test janitor - remove rollout token via validate/check
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)

        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token",
            "scope": json.dumps({
                "path": ["userservice"]})
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        # enroll second token - the enrollment token should disapear now

        params = {
            "otpkey": 'second',
            "user": user,
            "pin": "Test123!",
            "type": "pw",
            "description": "second token",
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        # ------------------------------------------------------------------ --

        # ensure the rollout is only valid in scope userservice

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": false' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": true' in response, response)

        response = self.make_admin_request('show', params=params)
        self.assertTrue('KIPW0815' in response, response)

        # ------------------------------------------------------------------ --

        # after the valid authentication with the second token
        # the rollout token should have disappeared

        response = self.validate_check(user, pin="Test123!", password='second')
        self.assertTrue(' "value": true' in response, response)

        response = self.make_admin_request('show', params=params)
        self.assertTrue('KIPW0815' not in response, response)

        return

    def test_enrollment_janitor2(self):
        """
        test janitor - remove rollout token via selfservice login
        """
        params = {
            'name': 'mfa',
            'scope': 'selfservice',
            'action': 'mfa_login, mfa_3_fields',
            'user': '*',
            'realm': '*',
            'active': True
            }

        response = self.make_system_request('setPolicy', params)
        self.assertTrue('false' not in response, response)

        user = 'passthru_user1@myDefRealm'
        password = 'geheim1'
        otp = 'verry_verry_secret'
        pin = '1234567890'

        params = {
            "otpkey": otp,
            "user": user,
            "pin": pin,

            "type": "pw",
            "serial": "KIPW0815",
            "description": "enrollment test token",
            "scope": json.dumps({
                "path": ["userservice"]})
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        # enroll second token

        params = {
            "otpkey": 'second',
            "user": user,
            "pin": "Test123!",
            "type": "pw",
            "description": "second token",
        }

        response = self.make_admin_request('init', params=params)
        self.assertTrue('"value": true' in response, response)

        # ------------------------------------------------------------------ --
        # ensure that login with rollout token is only
        # possible in the selfservice

        response = self.validate_check(user, pin, otp)
        self.assertTrue(' "value": false' in response, response)

        response = self.user_service_login(user, password, otp)
        self.assertTrue(' "value": true' in response, response)

        # ------------------------------------------------------------------ --

        # the valid authentication with the rollout token
        # should make the rollout token not disappeared

        response = self.make_admin_request('show', params=params)
        self.assertTrue('KIPW0815' in response, response)

        # ------------------------------------------------------------------ --

        # after the valid authentication with the second token
        # the rollout token should have disappeared

        response = self.user_service_login(user, password, otp='second')
        self.assertTrue(' "value": true' in response, response)

        response = self.make_admin_request('show', params=params)
        self.assertTrue('KIPW0815' not in response, response)

        return