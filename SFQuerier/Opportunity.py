##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : Opportunity.py

from simple_salesforce import SalesforceResourceNotFound, SalesforceMalformedRequest

from SFQuerier import Parser

__author__ = "Adam Mahameed"
__created__ = "01/04/2021"
__version__ = "1.0"

class Opportunity:
    def __init__(self, sf):
        self._sf = sf

    def get_opportunities(self, accountId=None):
        cases = self._sf.query(
            f"SELECT Id,Amount,IsClosed,IsWon,Type FROM Opportunity "
            f"WHERE AccountId='{accountId}'")
        return Parser.parse(cases)

    def delete(self, opportunityId=None):
        """
        Delete an account opportunity
        :param id: Opportunity ID to be deleted
        :return: True/False if deleted
        """
        if opportunityId is not None:
            try:
                status = self._sf.Opportunity.delete(opportunityId)
                if status == 204:
                    print("Deleted Opportunity ID:{0}".format(opportunityId))
                    return True
            except SalesforceResourceNotFound as e:  # Account doesn't exist
                print(
                    "[DELETE]{errorCode}: Resource {name} not found. {message}".format(message=e.content[0]['message'],
                                                                                       name=e.resource_name,
                                                                                       errorCode=e.content[0][
                                                                                           'errorCode']))
                return False
            except SalesforceMalformedRequest as e:  # Deletion failed (could be due account being associated to existing cases)
                print("[DELETE]{errorCode}: Malformed request {url}. {message},Opportunity ID: {opportunityId}".format(
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'], opportunityId=opportunityId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Opportunity ID is missing!")
            return False