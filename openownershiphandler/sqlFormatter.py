# -*- coding: utf-8 -*-
import sys


class Statement:
    def __init__(self):
        pass

    def getInsertRequest(self):
        tableName = self.__class__.__name__
        attrs = filter(lambda attr: not attr.startswith('__') and not attr.startswith('get'), dir(self))
        attr_list = []
        val_list = []
        addr_list = []

        for attr in attrs:
            val = getattr(self, attr)

            if type(val) is list:
                addr_list = val
            else:
                attr_list.append(attr)
                val_list.append("'"+val+"'")

        #print("Attrs:", attr_list)
        #print("Vals:", val_list)
        req = f"INSERT INTO {tableName} ({','.join(attr_list)}) VALUES ({','.join(val_list)});"

        if addr_list:
            for addr in addr_list:
                req += "\n" + addr.getInsertRequest()

        if not isinstance(self, Address):
            print(req)

        return req


class OwnershipOrControlStatement(Statement):
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


class EntityStatement(Statement):
    def __init__(self, jsonObj):
        self.statementID = getattr(jsonObj, "statementID", "")
        self.statementType = getattr(jsonObj, "statementType", "")
        self.statementDate = getattr(jsonObj, "statementDate", "")
        self.entityType = getattr(jsonObj, "entityType", "")
        self.missingInfoReason = getattr(jsonObj, "missingInfoReason", "")
        self.foundingDate = getattr(jsonObj, "foundingDate", "")
        self.dissolutionDate = getattr(jsonObj, "dissolutionDate", "")
        self.name = getattr(jsonObj, "name", "")
        # TODO alternateNames

        if hasattr(jsonObj, "incorporatedInJurisdiction"):
            self.incorporatedInJurisdictionCode = jsonObj.incorporatedInJurisdiction.code
            self.incorporatedInJurisdictionName = jsonObj.incorporatedInJurisdiction.name
        else:
            self.incorporatedInJurisdictionCode = ""
            self.incorporatedInJurisdictionName = ""

        if hasattr(jsonObj, "addresses"):
            self.addresses = []

            for address in jsonObj.addresses:
                addrObj = Address(address, self.statementID)
                self.addresses.append(addrObj)

        #TODO replacesStatements


class Address(Statement):
    def __init__(self, jsonObj, statementId):
        self.type = getattr(jsonObj, "type", "")
        self.address = getattr(jsonObj, "address", "")
        self.postCode = getattr(jsonObj, "postCode", "")
        self.country = getattr(jsonObj, "country", "")
        self.statementId = statementId


def getInsert(jsonObj):
    if not hasattr(jsonObj, "statementType"):
        sys.exit("Every statement must contain a statement type")

    if jsonObj.statementType == "entityStatement":
        formattedObj = EntityStatement(jsonObj)
        return formattedObj.getInsertRequest()
    elif jsonObj.statementType == "ownershipOrControlStatement":
        formattedObj = OwnershipOrControlStatement(jsonObj)
        return formattedObj.getInsertRequest()
    else:
        print(f"Skipping non-supported statement: {jsonObj.statementType}")
        return ""
