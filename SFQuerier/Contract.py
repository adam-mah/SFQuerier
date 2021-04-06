##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Contract.py

"""
TODO:Contract.create
TODO:Contract.update
TODO:Contract.delete
TODO:Contract.get
"""
__author__ = "Adam Mahameed"
__created__ = "05/04/2021"

import collections

from simple_salesforce import SalesforceResourceNotFound, SalesforceMalformedRequest

from SFQuerier import Parser
from SFQuerier.Account import Account


class Contract:
    def __init__(self, sf):
        self._sf = sf
        self.Account = Account(sf)

    def get_by_id(self, contractId=None):
        """
                    Get SF contract
                    :param contractId: contract ID
                    :return: Contract/False if contract was queried
                    """
        if contractId is not None:
            try:
                contract = self._sf.Contract.get(contractId)
                return Parser.parse(contract)
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
                        'errorCode'], id=contractId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contract ID is missing!")
            return False

    def get_account_contracts(self, accountId=None):
        contacts = self._sf.query(
            f"SELECT Id,ContractNumber,ContractTerm,CreatedById,CreatedDate,Description,OwnerId,AccountId FROM Contract WHERE AccountId='{accountId}'")
        return Parser.parse(contacts)

    def get_count(self):
        """
        Number of contracts in database
        :return: Integer
        """
        return (self._sf.query("SELECT Count() from Contract"))['totalSize']

    def create(self, json={}):
        """
        Create new contract, 'LastName' field is required!
        :param json: JSON Formatted contact data
        :return: Created account ID
        """
        try:
            status = self._sf.Contract.create(json)
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

    def update(self, contractId=None, json={}):
        """
        Update SF contact
        :param contractId:
        :param json: JSON attributes object to be updated
        :return: True/False if contract was updated/!updated
        """
        if contractId is not None:
            try:
                status = self._sf.Contract.update(contractId,
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
                print("[UPDATE]{errorCode}: Malformed request {url}. {message} ID: {contractId}".format(
                    message=e.content[0]['message'],
                    url=e.url,
                    errorCode=e.content[0][
                        'errorCode'], contractId=contractId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contract ID is missing!")
            return False

    def delete(self, contractId=None):
        """
        Delete SF contract
        :param contractId: contract ID to be deleted
        :return: True/False
        """
        if contractId is not None:
            try:
                status = self._sf.Contract.delete(contractId)
                if status == 204:
                    print("Deleted contract ID:{0}".format(contractId))
                    return True
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message},contact ID: {contractId}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'],
                    contractId=contractId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contact ID is missing!")
            return False
