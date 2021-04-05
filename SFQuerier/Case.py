##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Case.py

import collections

from simple_salesforce import SalesforceMalformedRequest, SalesforceResourceNotFound

from SFQuerier import Parser
from SFQuerier.CaseComment import CaseComment


class Case:
    def __init__(self, sf):
        self._sf = sf
        self.CaseComment = CaseComment(sf)

    def get_by_number(self, caseNumber=None):
        """
        Get case details by case number
        :param caseNumber: SF case number
        :return: Queried case
        """
        if caseNumber is not None:
            case = self._sf.query(
                f"SELECT Id,AccountId,CaseNumber,ContactId,Description,ParentId,Status FROM Case WHERE CaseNumber='{caseNumber}'")
            if case['totalSize'] != 0:
                return Parser.parse(case)[0]
            else:
                print("Case was not found")
                return False
        else:
            print("Case number is missing!")
            return False

    def get_by_id(self, caseId=None):
        """
        Get SF case
        :param caseId: case ID
        :return: case/False if case was queried
        """
        if caseId is not None:
            try:
                case = self._sf.Account.get(caseId)
                # account =self.sf.query("SELECT Id,AccountNumber,Name,CreatedDate,Website FROM Account WHERE Id= '{id}'".format(id=id))
                return Parser.parse(case)
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
                        'errorCode'], id=caseId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Account ID is missing!")
            return False

    def get_count(self):
        """
        Number of cases in database
        :return: Integer
        """
        return (self._sf.query("SELECT Count() from Case"))['totalSize']

    def create(self, contactId=None, subject=None, description=None):
        """
        Create new user case via contactID,subject,description
        :param description: Case description
        :param subject: Case subject
        :param contactId: Contact ID
        :return: Created case ID
        """
        try:
            case = self._sf.Case.create({'ContactId': contactId, "Subject": subject, "Description": description})
            if isinstance(case, collections.OrderedDict):
                if case['success'] == True:
                    return case['id']
                else:
                    print(case['errors'])
                    raise Exception("Case creation failed")
            else:
                raise Exception("Case creation failed")

        except SalesforceResourceNotFound as e:
            print(
                "[CASE CREATE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                        name=e.resource_name,
                                                                                        errorCode=e.content[0][
                                                                                            'errorCode']))
            return False
        except SalesforceMalformedRequest as e:  # Field doesn't exist / Required fields are missing
            print("[CASE CREATE]{errorCode}: Malformed request {url}. {message}".format(message=e.content[0]['message'],
                                                                                        url=e.url,
                                                                                        errorCode=e.content[0][
                                                                                            'errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False

    # def create_case(self, json={}):
    #     """
    #     Create new case using JSON formatting
    #     :param json: JSON Formatted contact data
    #     :return: Created case ID
    #     """
    #     try:
    #         case = self.sf.Case.create(json)
    #         if isinstance(case, collections.OrderedDict):
    #             if case['success'] == True:
    #                 return case['id']
    #             else:
    #                 print(case['errors'])
    #                 raise Exception("Case creation failed")
    #         else:
    #             raise Exception("Case creation failed")
    #
    #     except SalesforceResourceNotFound as e:
    #         print(
    #             "[CASE CREATE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
    #                                                                                     name=e.resource_name,
    #                                                                                     errorCode=e.content[0][
    #                                                                                         'errorCode']))
    #         return False
    #     except SalesforceMalformedRequest as e:  # Field doesn't exist / Required fields are missing
    #         print("[CASE CREATE]{errorCode}: Malformed request {url}. {message}".format(message=e.content[0]['message'],
    #                                                                                     url=e.url,
    #                                                                                     errorCode=e.content[0][
    #                                                                                         'errorCode']))
    #         return False
    #     except Exception as e:
    #         print("Something went wrong!")
    #         print(e)
    #     return False

    def update(self, id=None, json={}):
        """
        Update SF contact
        :param id: contact ID
        :param json: JSON attributes object to be updated ex: {'LastName': 'Mahameed', 'FirstName': 'Adam'}
        :return: True/False if account was updated/!updated
        """
        if id is not None:
            try:
                status = self._sf.Case.update(id, json)  # Status code 204 is returned if info was updated succesfully
                if status == 204:
                    print("Case {id} was updated successfully!".format(id=id))
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

    def delete(self, caseId=None):
        """
        Delete SF case
        :param id: case ID to be deleted
        :return: True/False
        """
        if caseId is not None:
            try:
                status = self._sf.Case.delete(caseId)
                if status == 204:
                    print("Deleted case ID:{0}".format(caseId))
                    return True
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message},case ID: {id}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'], id=caseId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Case ID is missing!")
            return False
