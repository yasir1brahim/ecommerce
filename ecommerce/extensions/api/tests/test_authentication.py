# -*- coding: utf-8 -*-
import json
from urlparse import urljoin

import httpretty
import mock
from django.test import RequestFactory

from ecommerce.core.url_utils import get_oauth2_provider_url
from ecommerce.extensions.api.authentication import BearerAuthentication
from ecommerce.tests.testcases import TestCase


class AccessTokenMixin(object):
    DEFAULT_TOKEN = 'abc123'

    def mock_user_info_response(self, status=200, username='fake-user'):
        data = {
            'preferred_username': username,
            'email': '{}@example.com'.format(username),
            'family_name': 'Doe',
            'given_name': 'Jane',
        }
        httpretty.register_uri(
            httpretty.GET, '{}/user_info/'.format(get_oauth2_provider_url()),
            body=json.dumps(data),
            content_type="application/json",
            status=status
        )


class BearerAuthenticationTests(TestCase):
    """ Tests for the BearerAuthentication class. """

    def setUp(self):
        super(BearerAuthenticationTests, self).setUp()
        self.auth = BearerAuthentication()
        self.factory = RequestFactory()

    def create_request(self, token=AccessTokenMixin.DEFAULT_TOKEN):
        """ Returns a Request with the correct authorization header and Site. """
        auth_header = 'Bearer {}'.format(token)
        request = self.factory.get('/', HTTP_AUTHORIZATION=auth_header)
        request.site = self.site
        return request

    def test_get_user_info_url(self):
        """ Verify the method returns a user info URL specific to the Site's LMS instance. """
        request = self.create_request()
        with mock.patch('ecommerce.extensions.order.utils.get_current_request', mock.Mock(return_value=request)):
            actual = self.auth.get_user_info_url()
            expected = urljoin(self.site.siteconfiguration.lms_url_root, '/oauth2/user_info/')
            self.assertEqual(actual, expected)
