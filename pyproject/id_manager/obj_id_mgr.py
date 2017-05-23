# -*- coding: utf-8 -*-
# @Author  : jh.feng

import bson.objectid as objectid
import uuid

class IdManagerInterface(object):
    @staticmethod
    def GenID():
        raise NotImplementedError

    @staticmethod
    def Str2ID(string):
        raise NotImplementedError

    @staticmethod
    def ID2Str(uid):
        raise NotImplementedError

    @staticmethod
    def Bytes2ID(bytes):
        raise NotImplementedError

    @staticmethod
    def ID2Bytes(uid):
        raise NotImplementedError

    @staticmethod
    def GetIDType():
        raise NotImplementedError

    @staticmethod
    def IsIDType(obj):
        raise NotImplementedError


class IdManagerImpl_UUID(IdManagerInterface):
    """
    IdManager负责给Entity产生一个唯一的id
    """

    @staticmethod
    def GenID():
        return uuid.uuid1()

    @staticmethod
    def Str2ID(string):
        return uuid.UUID(string)

    @staticmethod
    def ID2Str(uid):
        return str(uid)

    @staticmethod
    def Bytes2ID(bytes):
        return uuid.UUID(bytes=bytes)

    @staticmethod
    def ID2Bytes(uid):
        return uid.bytes

    @staticmethod
    def GetIDType():
        return uuid.UUID

    @staticmethod
    def IsIDType(obj):
        return isinstance(obj, uuid.UUID)


class IdManagerImpl_ObjectId(IdManagerInterface):
    """
    IdManager负责给Entity产生一个唯一的id
    """

    @staticmethod
    def GenID():
        return objectid.ObjectId()

    @staticmethod
    def Str2ID(string):
        return objectid.ObjectId(string)

    @staticmethod
    def ID2Str(uid):
        return str(uid)

    @staticmethod
    def Bytes2ID(bytes):
        return objectid.ObjectId(bytes)

    @staticmethod
    def ID2Bytes(uid):
        return uid.binary

    @staticmethod
    def GetIDType():
        return objectid.ObjectId

    @staticmethod
    def IsIDType(obj):
        return isinstance(obj, objectid.ObjectId)


IdManager = IdManagerImpl_ObjectId
