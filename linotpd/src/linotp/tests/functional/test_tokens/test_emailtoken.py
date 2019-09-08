# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2019 KeyIdentity GmbH
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
  Test linotp.tokens.emailtoken with template file and inline template
"""

import os
from mock import patch
import json
import smtplib


from linotp.tests import TestController
from linotp.provider.emailprovider import EMAIL_PROVIDER_TEMPLATE_KEY

class TestEmailtoken(TestController):

    def setUp(self):
        """ setup for std resolver / realms"""

        TestController.setUp(self)
        self.create_common_resolvers()
        self.create_common_realms()

    def tearDown(self):
        """ clean up for all token and resolver / realms """

        self.delete_all_realms()
        self.delete_all_resolvers()
        self.delete_all_token()

        TestController.tearDown(self)

    def test_email_template_with_file_ref(self):
        """
        verify that email with template file reference does work
        """
        # ------------------------------------------------------------------ --

        # first define that the fixture path could be an
        # email_provider_template root directory - we will use the email.eml
        # template

        params = {
            EMAIL_PROVIDER_TEMPLATE_KEY: self.fixture_path
            }

        response = self.make_system_request('setConfig', params=params)
        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # now define the email provider

        email_provider_config = {
            "SMTP_SERVER": "mail.example.com",
            "SMTP_USER": "secret_user",
            "SMTP_PASSWORD": "secret_pasword",
            "EMAIL_SUBJECT": "Your requested otp ${otp} for token ${serial}",
            "TEMPLATE": "file://email.eml"
        }

        email_provider_definition = {
            'name': 'TemplEMailProvider', 
            'timeout': '3', 
            'type': 'email', 
            'config': json.dumps(email_provider_config),
            'class': 'linotp.provider.emailprovider.SMTPEmailProvider'
            }

        response = self.make_system_request(
            'setProvider', params=email_provider_definition)

        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # and make hime the default email provider

        params = {
            'type': 'email', 
            'name': 'TemplEMailProvider'
        }
        response = self.make_system_request(
            'setDefaultProvider', params=params)

        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # enroll email token for user

        user = 'root'
        serial = 'EMAIL_TOKEN_001'

        params = {
            'user': user,
            'type': 'email',
            'pin': '123',
            'email_address': 'test@example.com',
            'serial': serial
        }
        response = self.make_admin_request('init', params=params)
        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # setup the mocking smtp client from which we get the sendmal args
        # to verify the template prcessing

        patch_smtp = patch('smtplib.SMTP', spec=smtplib.SMTP)
        mock_smtp_class = patch_smtp.start()
        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.sendmail.return_value = []

        try:

            # now trigger a challenge for the user

            params = {
                'user': user,
                'pass': '123'
                }
            response = self.make_validate_request('check', params=params)
            assert 'false' in response
            assert '"message": "e-mail sent successfully"' in response

            call_args = mock_smtp_instance.sendmail.call_args
            _from, _to, message = call_args.args

            assert 'Content-Type: multipart/related;' in message
            assert '${otp}' not in message
            assert "${serial}" not in message
            assert serial in message

        finally:

            patch_smtp.stop()


    def test_email_template_with_inline(self):
        """
        verify that email with template file reference does work
        """
        # ------------------------------------------------------------------ --

        # first define that the fixture path could be an
        # email_provider_template root directory - we will use the email.eml
        # template

        params = {
            EMAIL_PROVIDER_TEMPLATE_KEY: self.fixture_path
            }

        response = self.make_system_request('setConfig', params=params)
        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # define an email message policy which should be 
        # overruled by the template

        params = {
            'name': 'email_message',
            'active': True,
            'scope': 'authentication',
            'action': ("emailtext='text from policy',"
                       "emailsubject='subject from policy'"),
            'user': '*',
            'realm': '*'
            }

        response = self.make_system_request('setPolicy', params=params)
        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # now define the email provider

        filename = os.path.join(self.fixture_path, 'email.eml')
        with open(filename, "rb") as f:
            content = f.read()
        inline_template = '"' + content.replace('"', '\"') + '"'

        email_provider_config = {
            "SMTP_SERVER": "mail.example.com",
            "SMTP_USER": "secret_user",
            "SMTP_PASSWORD": "secret_pasword",
            "EMAIL_SUBJECT": ("Your requested otp ${otp} for "
                        "token ${serial} and ${user}"),

            "TEMPLATE": inline_template
        }
        email_provider_definition = {
            'name': 'TemplEMailProvider', 
            'timeout': '3', 
            'type': 'email', 
            'config': json.dumps(email_provider_config),
            'class': 'linotp.provider.emailprovider.SMTPEmailProvider'
            }

        response = self.make_system_request(
            'setProvider', params=email_provider_definition)

        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # and make him the default email provider

        params = {
            'type': 'email', 
            'name': 'TemplEMailProvider'
        }
        response = self.make_system_request(
            'setDefaultProvider', params=params)

        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # enroll email token for user

        user = 'root'
        serial = 'EMAIL_TOKEN_001'

        params = {
            'user': user,
            'type': 'email',
            'pin': '123',
            'email_address': 'test@example.com',
            'serial': serial
        }
        response = self.make_admin_request('init', params=params)
        assert 'false' not in response

        # ------------------------------------------------------------------ --

        # setup the mocking smtp client from which we get the sendmal args
        # to verify the template prcessing

        patch_smtp = patch('smtplib.SMTP', spec=smtplib.SMTP)
        mock_smtp_class = patch_smtp.start()
        mock_smtp_instance = mock_smtp_class.return_value
        mock_smtp_instance.sendmail.return_value = []

        try:

            # now trigger a challenge for the user

            params = {
                'user': user,
                'pass': '123'
                }
            response = self.make_validate_request('check', params=params)

            assert 'false' in response
            assert '"message": "e-mail sent successfully"' in response

            call_args = mock_smtp_instance.sendmail.call_args
            _from, _to, message = call_args.args

            # verify that the template is used instead of the message
            assert 'Content-Type: multipart/related;' in message

            # verify that otp and serial are replaced in message
            assert '${otp}' not in message
            assert "${serial}" not in message
            assert serial in message

            # verify that unknown vars are not replaced
            assert "${user}" in message

            # verify that the policy did not overrule the template
            assert 'from policy' not in message

        finally:

            patch_smtp.stop()

# eof
