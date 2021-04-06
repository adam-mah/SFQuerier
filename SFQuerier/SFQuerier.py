##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : SFQuerier.py

import collections
from html import escape

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import *

__author__ = "Adam Mahameed"
__created__ = "24/03/2021"
__modified__ = "05/04/2021"
__version__ = "1.5"

"""
Please make sure to refer to REST API reference guide for more information how to use.
https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm

This module is an extension of simple-salesforce REST API 
https://github.com/simple-salesforce/simple-salesforce/
"""

from SFQuerier import Parser
from SFQuerier.Account import Account
from SFQuerier.Case import Case
from SFQuerier.Contact import Contact
from SFQuerier.Contract import Contract
from SFQuerier.Opportunity import Opportunity


class SalesforceQ:
    def __init__(self, instance=None, instance_url=None, username=None, password=None, security_token=None,
                 organizationId=None, domain='login'):
        self.username = escape(username) if username else None
        self.password = escape(password) if password else None
        self.instance = escape(instance) if instance else None
        self.instance_url = escape(instance_url) if instance_url else None

        self.sf = None
        if self.username is not None and self.password is not None and self.instance is not None or self.instance_url is not None or self.instance is not None:
            if security_token is not None:
                self.security_token = security_token
                self.sf = Salesforce(instance=self.instance, username=self.username, password=self.password,
                                     security_token=self.security_token, domain=domain)
                self.Account = Account(self.sf)
                self.Contact = Contact(self.sf)
                self.Case = Case(self.sf)
                self.Opportunity = Opportunity(self.sf)
                self.Contract = Contract(self.sf)

            elif organizationId is not None:
                self.organizationId = organizationId
                self.sf = Salesforce(instance=self.instance, username=self.username, password=self.password,
                                     organizationId=self.organizationId, domain=domain)

                self.Account = Account(self.sf)
                self.Contact = Contact(self.sf)
                self.Case = Case(self.sf)
                self.Opportunity = Opportunity(self.sf)
                self.Contract = Contract(self.sf)

            if self.sf is None:
                raise SalesforceAuthenticationFailed('INVALID AUTH',
                                                     'You must submit username and password either a security token or '
                                                     'organizationId for authentication')
        else:
            raise SalesforceAuthenticationFailed('INVALID AUTH',
                                                 'You must submit username and password either a security token or '
                                                 'organizationId for authentication')

    def get(self, path, params=None, **kwargs):
        """Allows you to make a direct GET REST call if you know the path
        EXAMPLE: .get(path='sobjects/Account/0017j00000VLkZtAAL', params={"fields" : "Name"}))
                Arguments:
                * path: The path of the request
                    Example: sobjects/User/ABC123/password'
                * params: dict of parameters to pass to the path
                * method: HTTP request method, default GET
                * other arguments supported by requests.request (e.g. json, timeout)
                :return JSON / False if issue has occurred
                """
        try:
            res = self.sf.restful(path=path, params=params, method='GET', **kwargs)
            return res
        except SalesforceResourceNotFound as e:
            print(
                "[GET]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                name=e.resource_name,
                                                                                errorCode=e.content[0][
                                                                                    'errorCode']))
            return False
        except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
            print("[GET]{errorCode}: Malformed request {url}. {message}".format(
                message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False

    def post(self, path, params=None, **kwargs):
        """Allows you to make a direct POST REST call if you know the path
        EXAMPLE: .post(path='sobjects/Account',params=None,json={"Name" : "MyREST Test account"})
                Arguments:
                * path: The path of the request
                    Example: sobjects/User/ABC123/password'
                * params: dict of parameters to pass to the path
                * method: HTTP request method, default GET
                * other arguments supported by requests.request (e.g. json, timeout)
                :return JSON
                """
        try:
            res = self.sf.restful(path=path, params=params, method='POST', **kwargs)
            return res
        except SalesforceResourceNotFound as e:
            print(
                "[POST]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                 name=e.resource_name,
                                                                                 errorCode=e.content[0][
                                                                                     'errorCode']))
            return False
        except SalesforceMalformedRequest as e:
            print("[POST]{errorCode}: Malformed request {url}. {message}".format(
                message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False

    def patch(self, path, params=None, **kwargs):
        """Allows you to make a direct POST REST call if you know the path
        EXAMPLE: .patch(path='sobjects/Account',params=None,json={"Name" : "MyREST Test account"})
                Arguments:
                * path: The path of the request
                    Example: sobjects/User/ABC123/password'
                * params: dict of parameters to pass to the path
                * method: HTTP request method, PATCH
                * other arguments supported by requests.request (e.g. json, timeout)
                :return JSON
                """
        try:
            res = self.sf.restful(path=path, params=params, method='PATCH', **kwargs)
            return res
        except SalesforceResourceNotFound as e:
            print(
                "[PATCH]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                  name=e.resource_name,
                                                                                  errorCode=e.content[0][
                                                                                      'errorCode']))
            return False
        except SalesforceMalformedRequest as e:
            print("[PATCH]{errorCode}: Malformed request {url}. {message}".format(
                message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False

    def delete(self, path, params=None, **kwargs):
        """Allows you to make a direct DELETE REST call if you know the path
        EXAMPLE: .delete(path='sobjects/Account/recordId')
                Arguments:
                * path: The path of the request
                    Example: sobjects/User/ABC123/password'
                * params: dict of parameters to pass to the path
                * method: HTTP request method, DELETE
                * other arguments supported by requests.request (e.g. json, timeout)
                :return JSON
                """
        try:
            res = self.sf.restful(path=path, params=params, method='DELETE', **kwargs)
            return res
        except SalesforceResourceNotFound as e:
            print(
                "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                  name=e.resource_name,
                                                                                  errorCode=e.content[0][
                                                                                      'errorCode']))
            return False
        except SalesforceMalformedRequest as e:
            print("[DELETE]{errorCode}: Malformed request {url}. {message}".format(
                message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False
