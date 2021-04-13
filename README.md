# openownership-parser
Parser to import Open Ownership data in to SAP database

Need to create the following tables


## Pre-requisite
* install ijson
```bash
pip install ijson
```

* Create the following tables:
    * EntityStatement
      
        |Name|Type|Description|Required|
        |---|---|---|---|
        |statementID|string|A persistent globally unique identifier for this statement.||
        |statementType|string|This should always be ‘entityStatement.|Yes|
        |statementDate|string|The date on which this statement was made.||
        |entityType|string|What kind of entity is this? The ‘registeredEntity’ code covers any legal entity created through an act of official registration, usually resulting in an identifier being assigned to the entity.|Yes|
        |missingInfoReason|string|For EntityStatements with the type ‘anonymousEntity’ or ‘unknownEntity’ this field should contain an explanation of the reason that detailed information on the entity is not provided.||
        |name|string|The declared name of this entity.||
        |alternateNames|array[string]|An array of other names this entity is known by.||
        |incorporatedInJurisdictionCode|string|The ISO_3166-2 2-Digit country code, or ISO_3166-2 sub-division code of the jurisdiction||
        |incorporatedInJurisdictionName|string|The name of the jurisdiction||
        |foundingDate|string|When was this entity founded, created or registered. Please provide as precise a date as possible in ISO 8601 format. When only the year or year and month is known, these can be given as YYYY or YYYY-MM.||
        |dissolutionDate|string|If this entity is no longer active, provide the date on which it was disolved or ceased. Please provide as precise a date as possible in ISO 8601 format. When only the year or year and month is known, these can be given as YYYY or YYYY-MM.||
        |replacesStatements|array[string]|If this statement replaces a previous statement or statements, provide the identifier(s) for the previous statement(s) here. Consuming applications are advised to mark the identified statements as no longer active.||
      
    * Address

        |Name|Type|Description|Required|
        |---|---|---|---|
        |addressId|int|address identifier|Yes|
        |type|string|What type of address is this? placeOfBirth, home, residence, registered, service, alternative||
        |address|string|The address, with each line or component of the address separated by a line-break or comma. This field may also include the postal code.||
        |postCode|string|The postal code for this address.||
        |country|string|The ISO 2-Digit county code for this address.||
        |statementId|string|Entity Statement located at this address|Yes|
        
    * OwnershipOrControlStatement

        |Name|Type|Description|Required|
        |---|---|---|---|
        |statementID|string|A persistent globally unique identifier for this statement.|Yes|
        |statementType|string|This should always be set to ownershipOrControlStatement.|Yes|
        |statementDate|date|The date on which this statement was made.||
        |subjectDescribedByEntityStatement|string|Provide the identifier of the statement which describes the entity that the subject of an ownership or control interest.|Yes|
        |interestedPartyDescribedByEntityStatement|string|A reference to a statement describing a registered entity, trust or arrangement that has an ownership or control interest in the subject of this statement. An entityStatement should be used when the direct interests to be described represents known control or ownership by anyone other than a natural person.||
        |replacesStatements|array[string]|If this statement replaces a previous statement or statements, provide the identifier(s) for the previous statement(s) here. Consuming applications are advised to mark the identified statements as no longer active.||
        
