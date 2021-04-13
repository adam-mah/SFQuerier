##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Account.py

import collections
from simple_salesforce import SalesforceResourceNotFound, SalesforceMalformedRequest
from SFQuerier import Parser
from SFQuerier.Case import Case
from SFQuerier.Contact import Contact
from SFQuerier.Opportunity import Opportunity


class Account:
    def __init__(self, sf):
        self._sf = sf
        self.Contact = Contact(sf)
        self.Case = Case(sf)
        self.Opportunity = Opportunity(sf)

    def get_all(self):  # TODO: A LIMIT must be added, or Bulk API should be used instead
        accounts = self._sf.query("SELECT Id,AccountNumber,Name,CreatedDate,Website FROM Account")
        accounts = Parser.parse(accounts)
        return accounts

    def get_all_where(self, where_query=None):
        accounts = self._sf.query(
            "SELECT Id,AccountNumber,Name,CreatedDate,Website FROM Account WHERE {0}".format(where_query))
        return Parser.parse_to_object(accounts)

    def get_count(self):
        """
        Number of accounts in database
        :return: Integer
        """
        return (self._sf.query("SELECT Count() from Account"))['totalSize']

    def get_by_id(self, accountId=None):
        """
            Get SF account
            :param accountId: ID string / list of IDs
            :return: JSON, JSON format list / False if account was not queried
            """
        if accountId is not None:
            try:
                if isinstance(accountId, str):
                    account = self._sf.Account.get(accountId)
                    return [Parser.parse(account)]
                elif isinstance(accountId, list):
                    accounts = []
                    for acc_id in accountId:
                        account = self._sf.Account.get(acc_id)
                        accounts.append(Parser.parse(account))
                    return accounts
            except SalesforceResourceNotFound as e:  # Not found
                print(
                    "[GET]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                    name=e.resource_name,
                                                                                    errorCode=e.content[0][
                                                                                        'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Field doesn't exist
                print("[GET]{errorCode}: Malformed request {url}. {message} ID: {accountId}".format(
                    message=e.content[0]['message'],
                    url=e.url,
                    errorCode=e.content[0][
                        'errorCode'], accountId=accountId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Account ID is missing!")
            return False

    def get_by_domain(self, website):
        accounts = self._sf.query(
            "SELECT Id,AccountNumber,Name,CreatedDate,Website FROM Account WHERE Website='{website}'".format(
                website=website))
        return Parser.parse(accounts)

    def get_by_name(self, name):
        accounts = self._sf.query(
            "SELECT Id,AccountNumber,Name,CreatedDate,Website FROM Account WHERE Name='{name}'".format(name=name))
        return Parser.parse(accounts)  # Returns list of accounts

    def get_cases(self, accountId=None):
        cases = self._sf.query(f"SELECT Id,CaseNumber,ContactId,AccountId,Type,Status,Subject,Description FROM Case "
                               f"WHERE AccountId='{accountId}'")
        return Parser.parse(cases)

    def get_contacts(self, accountId=None):
        contacts = self._sf.query(
            f"SELECT Id,FirstName,LastName,Email,Phone,AccountId FROM Contact WHERE AccountId='{accountId}'")
        return Parser.parse(contacts)

    def purge(self, accountId=None):
        """
                Delete SF account and its records
                :param accountId:
                :return: Dict [bool, cases, opportunities]
                """
        if accountId is not None:
            try:
                """Delete cases"""
                cases = self.get_cases(accountId=accountId)
                if len(cases) != 0:
                    for case in cases:
                        if self.Case.delete(caseId=case.Id):
                            print(f"Deleted case #{case.CaseNumber}")
                        else:
                            print(f"Failed to delete case #{case.CaseNumber}")
                else:
                    print(f"No cases were found for account ID: {accountId}")

                """Delete opportunities"""
                opportunities = self.Opportunity.get_opportunities(accountId=accountId)
                if len(opportunities) != 0:
                    for opportunity in opportunities:
                        if self.Opportunity.delete(opportunityId=opportunity.Id):
                            print(f"Deleted opportunity ID: {opportunity.Id}")
                        else:
                            print(f"Failed to delete opportunity ID: {opportunity.Id}")
                else:
                    print(f"No opportunities were found for account ID: {accountId}")

                """Delete account"""
                status = self._sf.Account.delete(accountId)
                if status == 204:
                    print("Deleted account ID:{0}".format(accountId))
                    return {'bool': True, 'cases': cases, 'opportunities': opportunities}
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message} ID: {accountId}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'],
                    accountId=accountId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)
                return False
        else:
            print("Account ID is missing!")
            return False

    def create(self, json={}):
        """
        Create new account, 'Name' field is required!
        :param json: JSON Formatted account data
        :return: Created account ID
        """
        try:
            status = self._sf.Account.create(json)
            if isinstance(status, collections.OrderedDict):
                if status['success'] == True:
                    return status['id']
                else:
                    raise Exception("Account creation failed")
            else:
                raise Exception("Account creation failed")

        except SalesforceResourceNotFound as e:
            print(
                "[CREATE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                   name=e.resource_name,
                                                                                   errorCode=e.content[0][
                                                                                       'errorCode']))
            return False
        except SalesforceMalformedRequest as e:  # Field doesn't exist / Required fields are missing
            print("[CREATE]{errorCode}: Malformed request {url}. {message}".format(message=e.content[0]['message'],
                                                                                   url=e.url,
                                                                                   errorCode=e.content[0][
                                                                                       'errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False

    def update(self, accountId=None, json={}):
        """
        Update SF account
        :param accountId:
        :param json: JSON attributes object to be updated ex: {'Name': 'Mahameed'}
        :return: True/False if account was updated/!updated
        """
        if accountId is not None:
            try:
                status = self._sf.Account.update(accountId,
                                                 json)  # Status code 204 is returned if info was updated succesfully
                if status == 204:
                    print("Updated account ID: " + str(accountId))
                    return True
            except SalesforceResourceNotFound as e:  # Not found
                print(
                    "[UPDATE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Field doesn't exist
                print("[UPDATE]{errorCode}: Malformed request {url}. {message} ID: {accountId}".format(
                    message=e.content[0]['message'],
                    url=e.url,
                    errorCode=e.content[0][
                        'errorCode'], accountId=accountId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Account ID is missing!")
            return False

    def delete(self, accountId=None):
        """
        Delete SF account
        :param accountId:
        :return: True/False
        """
        if accountId is not None:
            try:
                status = self._sf.Account.delete(accountId)
                if status == 204:
                    print("Deleted account ID:{0}".format(accountId))
                    return True
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message} ID: {accountId}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'],
                    accountId=accountId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Account ID is missing!")
            return False
