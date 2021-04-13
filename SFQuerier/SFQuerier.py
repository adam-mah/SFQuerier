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
                """SOQL queries: 
                
                query:  #Equivalent to .get(path='query', params='q=SELECT Id, Name FROM Contact WHERE LastName = 'Adam'')
                    .query("SELECT Id, Name FROM Contact WHERE LastName = 'Adam'") 
                
                query_more:
                If, due to an especially large result, Salesforce adds a nextRecordsUrl to your query result, 
                such as "nextRecordsUrl" : "/services/data/v26.0/query/01gD0000002HU6KIAW-2000", you can pull the 
                additional results with either the ID or the full URL (if using the full URL, you must pass 'True' as 
                your second argument) 
                
                    .query_more("01gD0000002HU6KIAW-2000")
                    .query_more("/services/data/v26.0/query/01gD0000002HU6KIAW-2000", True)
                
                query_all:
                A convenience of query_more, to retrieve all of the results in a single local method call use
                    .query_all("SELECT Id, Email FROM Contact WHERE LastName = 'Jones'")
                """
                self.query = self.sf.query
                self.query_more = self.sf.query_more
                self.query_all = self.sf.query_all
                self.search = self.sf.search
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

    def get_sobject(self, sobject=None, sobject_id=None):
        """Allows you to make a direct GET REST call if you know the path
        EXAMPLE: .get(path='sobjects/Account/0017j00000VLkZtAAL', params={"fields" : "Name"}))
                Arguments:
                * path: The path of the request
                    Example: sobjects/User/ABC123/password'
                * params: dict of parameters to pass to the path
                * method: HTTP request method, default GET
                * other arguments supported by requests.request (e.g. json, timeout)
                :return JSON objects list / False if issue has occurred
                """
        try:
            if isinstance(sobject_id, str):
                sobject_data = self.__getattr__(sobject).get(sobject_id)
                return [Parser.parse(sobject_data)]
            elif isinstance(sobject_id, list):
                sobjects_data = []
                for sobject_sid in sobject_id:
                    sobject_data = self.__getattr__(sobject).get(sobject_sid)
                    sobjects_data.append(Parser.parse(sobject_data))
                return sobjects_data
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

    def get_sobject_type(self, sobject_id):
        """Get sobject type by ID"""
        try:
            res = self.get(path=f'ui-api/record-ui/{sobject_id}')
            od = collections.OrderedDict(sorted(res['layouts'].items(), key=lambda x: x[1]))
            return list(od.keys())[0]
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

    def __getattr__(self, name):
        """
        Every salesforce object without a written class can still access the following functions:
        metadata / describe / describe_layout / get / get_by_custom_id / create / upsert / update / delete / deleted / updated
        More information at SFType Class:
         https://github.com/simple-salesforce/simple-salesforce/blob/5d921f3dd32a69472b31d435544ce9c5a1d5eba3/simple_salesforce/api.py#L638
        :param name: sobject name
        :return: SFType object
        """
        return self.sf.__getattr__(name)
