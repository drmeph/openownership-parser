# -*- coding: utf-8 -*-
import sys


class OwnershipOrControlStatement:
    def __init__(self, jsonObj):
        self.statementID = getattr(jsonObj, "statementID", "")
        self.statementType = getattr(jsonObj, "statementType", "")
        self.statementDate = getattr(jsonObj, "statementDate", "")

        if hasattr(jsonObj, "subject"):
            self.subjectDescribedByEntityStatement = jsonObj.subject.describedByEntityStatement
        else:
            self.subjectDescribedByEntityStatement = ""

        # Will only set this attribute if the interested party is an Entity, not a person. (cause: PII)
        if hasattr(jsonObj, "interestedParty"):
            interestedParty = jsonObj.interestedParty
            if hasattr(interestedParty, "describedByEntityStatement"):
                self.interestedPartyDescribedByEntityStatement = jsonObj.interestedParty.describedByEntityStatement
            else:
                self.interestedPartyDescribedByEntityStatement = ""

        # TODO replacesStatements

    def getInsertRequest(self):
        attrs = filter(lambda attr: not attr.startswith('__') and not attr.startswith('get'), dir(self))
        attr_list = []
        val_list = []

        for attr in attrs:
            attr_list.append(attr)
            val_list.append(getattr(self, attr))

        req = f"INSERT INTO OwnershipOrControlStatement ({','.join(attr_list)}) VALUES ({','.join(val_list)})"
        print(req)

        return req


class EntityStatement:
    def __init__(self, jsonObj):
        self.statementID = getattr(jsonObj, "statementID", "")

    def getInsertRequest(self):
        return ""


class Address:
    def __init__(self, jsonObj):
        self.type = getattr(jsonObj, "type", "")

    def getInsertRequest(self):
        return ""

def getInsert(jsonObj):
    if not hasattr(jsonObj, "statementType"):
        sys.exit("Every statement must contain a statement type")

    if jsonObj.statementType == "entityStatement":
        formattedObj = EntityStatement(jsonObj)
        formattedObj.getInsertRequest()
    elif jsonObj.statementType == "ownershipOrControlStatement":
        formattedObj = OwnershipOrControlStatement(jsonObj)
        formattedObj.getInsertRequest()
    else:
        print(f"Skipping non-supported statement: {jsonObj.statementType}")
