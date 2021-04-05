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

from SFQuerier.Account import Account
from SFQuerier.Case import Case
from SFQuerier.Contact import Contact
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

            elif organizationId is not None:
                self.organizationId = organizationId
                self.sf = Salesforce(instance=self.instance, username=self.username, password=self.password,
                                     organizationId=self.organizationId, domain=domain)

                self.Account = Account(self.sf)
                self.Contact = Contact(self.sf)
                self.Case = Case(self.sf)
                self.Opportunity = Opportunity(self.sf)

            if self.sf is None:
                raise SalesforceAuthenticationFailed('INVALID AUTH',
                                                     'You must submit username and password either a security token or '
                                                     'organizationId for authentication')
        else:
            raise SalesforceAuthenticationFailed('INVALID AUTH',
                                                 'You must submit username and password either a security token or '
                                                 'organizationId for authentication')