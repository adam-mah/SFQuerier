##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Contact.py

import collections

from simple_salesforce import SalesforceMalformedRequest, SalesforceResourceNotFound

from SFQuerier import Parser
from SFQuerier.Case import Case


class Contact:
    def __init__(self, sf):
        self._sf = sf
        self.Case = Case(sf)

    def get_by_id(self, contactId=None):
        """
                    Get SF contact
                    :param contactId: contact ID
                    :return: Account/False if contact was queried
                    """
        if contactId is not None:
            try:
                contact = self._sf.Contact.get(contactId)
                return Parser.parse(contact)
            except SalesforceResourceNotFound as e:  # Not found
                print(
                    "[GET]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                    name=e.resource_name,
                                                                                    errorCode=e.content[0][
                                                                                        'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Field doesn't exist
                print("[GET]{errorCode}: Malformed request {url}. {message} ID: {id}".format(
                    message=e.content[0]['message'],
                    url=e.url,
                    errorCode=e.content[0][
                        'errorCode'], id=contactId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contact ID is missing!")
            return False

    def get_account_contacts(self, accountId=None):
        contacts = self._sf.query(
            f"SELECT Id,FirstName,LastName,Email,Phone,AccountId FROM Contact WHERE AccountId='{accountId}'")
        return Parser.parse(contacts)

    def get_cases(self, contactId=None):
        cases = self._sf.query(f"SELECT Id,CaseNumber,ContactId,AccountId FROM Case WHERE ContactId='{contactId}'")
        return Parser.parse(cases)

    def get_count(self):
        """
        Number of contacts in database
        :return: Integer
        """
        return (self._sf.query("SELECT Count() from Contact"))['totalSize']

    def purge(self, contactId=None):
        """
                Delete SF contact and its records
                :param contactId: Contact ID to be deleted
                :return: Dict [bool, cases]
                """
        if contactId is not None:
            try:
                """Delete cases"""
                cases = self.get_cases(contactId=contactId)
                if len(cases) != 0:
                    for case in cases:
                        if self.Case.delete(caseId=case.Id):
                            print(f"Deleted case #{case.CaseNumber}")
                        else:
                            print(f"Failed to delete case #{case.CaseNumber}")
                else:
                    print(f"No cases were found for contact ID: {contactId}")

                """Delete contact"""
                status = self._sf.Account.delete(contactId)
                if status == 204:
                    print("Deleted account ID:{0}".format(contactId))
                    return {'bool': True, 'cases': cases}
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message} ID: {contactId}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'],
                    contactId=contactId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)
                return False
        else:
            print("Contact ID is missing!")
            return False

    def create(self, json={}):
        """
        Create new contact, 'LastName' field is required!
        :param json: JSON Formatted contact data
        :return: Created account ID
        """
        try:
            status = self._sf.Contact.create(json)
            if isinstance(status, collections.OrderedDict):
                if status['success'] == True:
                    return status['id']
                else:
                    raise Exception("Contact creation failed")
            else:
                raise Exception("Contact creation failed")

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

    def update(self, id=None, json={}):
        """
        Update SF contact
        :param id: contact ID
        :param json: JSON attributes object to be updated ex: {'LastName': 'Mahameed', 'FirstName': 'Adam'}
        :return: True/False if account was updated/!updated
        """
        if id is not None:
            try:
                status = self._sf.Contact.update(id,
                                                 json)  # Status code 204 is returned if info was updated succesfully
                if status == 204:
                    return True
            except SalesforceResourceNotFound as e:  # Not found
                print(
                    "[UPDATE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Field doesn't exist
                print("[UPDATE]{errorCode}: Malformed request {url}. {message} ID: {id}".format(
                    message=e.content[0]['message'],
                    url=e.url,
                    errorCode=e.content[0][
                        'errorCode'], id=id))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contact ID is missing!")
            return False

    def delete(self, id=None):
        """
        Delete SF contact
        :param id: contact ID to be deleted
        :return: True/False
        """
        if id is not None:
            try:
                status = self._sf.Contact.delete(id)
                if status == 204:
                    print("Deleted contact ID:{0}".format(id))
                    return True
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message},contact ID: {id}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'], id=id))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contact ID is missing!")
            return False

    def delete_cases(self, contactId=None):
        if contactId is not None:
            cases = self.get_cases(contactId)
            if len(cases) != 0:
                for case in cases:
                    if self.Case.delete(caseId=case.Id):
                        print(f"Deleted case #{case.CaseNumber}")
                    else:
                        print(f"Failed to delete case #{case.CaseNumber}")
            else:
                print(f"No cases were found for contact ID: {contactId}")
            return True
        else:
            print("Contact ID is missing!")
            return False
