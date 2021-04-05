##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : Adam Mahameed
# @File    : CaseComment.py

"""
TODO:Case.Comment.add
TODO:Case.Comment.get
TODO:Case.Comment.delete
TODO:Case.Comment.update
"""
import collections

from simple_salesforce import SalesforceResourceNotFound, SalesforceMalformedRequest


class CaseComment:
    def __init__(self, sf):
        self._sf = sf

    def add(self, caseId=None, comment=None, isPublished=False):
        try:
            comment = self._sf.CaseComment.create(
                {'ParentId': caseId, 'CommentBody': comment, 'IsPublished': isPublished})
            if isinstance(comment, collections.OrderedDict):
                if comment['success'] == True:
                    return comment['id']
                else:
                    print(comment['errors'])
                    raise Exception("Case creation failed")
            else:
                raise Exception("Case creation failed")

        except SalesforceResourceNotFound as e:
            print(
                "[COMMENT CREATE]{errorCode}: Resource {name} not found. {message}".format(
                    message=e.content[0]['message'],
                    name=e.resource_name,
                    errorCode=e.content[0][
                        'errorCode']))
            return False
        except SalesforceMalformedRequest as e:  # Field doesn't exist / Required fields are missing
            print("[COMMENT CREATE]{errorCode}: Malformed request {url}. {message}".format(
                message=e.content[0]['message'],
                url=e.url,
                errorCode=e.content[0][
                    'errorCode']))
            return False
        except Exception as e:
            print("Something went wrong!")
            print(e)
        return False

    def update(self, commentId=None, comment=None, isPublished=None):
        """
        Update SF comment
        :param isPublished: boolean if comment is public
        :param commentId: comment ID
        :param comment: New comment value
        :return: True/False if comment was updated/!updated
        """
        if commentId is not None:
            try:
                if isPublished is None:
                    status = self._sf.CaseComment.update(commentId, {
                        "CommentBody": comment})  # Status code 204 is returned if info was updated succesfully
                else:
                    status = self._sf.CaseComment.update(commentId, {
                        "CommentBody": comment,
                        "IsPublished": isPublished})  # Status code 204 is returned if info was updated succesfully
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
                        'errorCode'], id=commentId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Comment ID is missing!")
            return False

    def delete(self, commentId=None):
        """
        Delete SF Comment
        :param commentId: comment ID to be deleted
        :return: bool if deleted
        """
        if commentId is not None:
            try:
                status = self._sf.CaseComment.delete(commentId)
                if status == 204:
                    print("Deleted comment ID:{0}".format(commentId))
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
                    message=e.content[0]['message'], url=e.url, errorCode=e.content[0]['errorCode'], id=commentId))
                return False
            except Exception as e:
                print("Something went wrong!")
                print(e)

            return False
        else:
            print("Contact ID is missing!")
            return False
