import logging

import boto3



def add_domain(domain,sdb = None):
    '''Add domain (database) to sdb if it does not exist
    Paramater: domain string, sdb client
    ParamValidationError, DNSSErverError'''
    if not sdb:
        sdb = boto3.client('sdb')

    return sdb.create_domain(DomainName = domain)


def delete_domain(domain,sdb = None):
    '''Delete an existing domain (database) in sdb if it exists
    Paramater: domain
    ParamValidationError, DNSSErverError'''

    if not sdb:
        sdb = boto3.client('sdb')
    return sdb.delete_domain(DomainName = domain)



def add_attribute(domain,item,attributes,sdb = None, replace = True):
    '''Add/remove attributes (columns) to a domain
    Paramaters: domain, item (Row), Attributes:Value list of dictionary
        eg. ('attribute','value')
    Exceptions: TypeError,IndexError,DNSServerError'''
    if not sdb:
        sdb = boto3.client('sdb')
    return sdb.put_attributes(
        DomainName=domain,
        ItemName=item,
        Attributes=[{'Name': attributes[0], 'Value': attributes[1],'Replace': replace}]

    )


def delete_attributes(domain,item,attributes,sdb = None):
    '''Remove attributes (columns) from a domain (database)
    Paramaters: domain, item (Row), Attributes:Value dictionary (column)
    eg. [{'Name': 'column', 'Value': 'data', 'Replace': True}]
    Exceptions: TypeError,IndexError,DNSServerError'''

    if not sdb:
        sdb = boto3.client('sdb')
    return sdb.delete_attributes(
        DomainName=domain,
        ItemName=item,
        Attributes=[ attributes ]
    )
    
    
def get_attributes(domain,item,sdb = None):
    '''Get attributes (columns) for an item (row)
    Paramaters: domain, item
    Exceptions: TypeError,IndexError,DNSServerError'''

    if not sdb:
        sdb = boto3.client('sdb')
    return sdb.get_attributes(
        DomainName=domain,
        ItemName=item,
   
    )

def delete_item(domain,item,sdb = None):
    '''Remove item (row) from a domain (database)
    Paramaters: domain, item (Row), Attributes:Value dictionary (column)
    eg. [{'Name': 'column', 'Value': 'data', 'Replace': True}]
    Exceptions: TypeError,IndexError,DNSServerError'''

    if not sdb:
        sdb = boto3.client('sdb')

    return sdb.delete_attributes(
        DomainName=domain,
        ItemName=item,
        Attributes=[]
    )

def select_all(domain,sdb = None):
    '''Get list of records for a zone
    Paramater: domain (database) name string
    Return: resource records list'''
    if not sdb:
        sdb = boto3.client('sdb')

    return sdb.select(SelectExpression = 'select * from '+domain)

def select_all_where(domain,query,order_by=None,sdb = None):
    '''Get list of records for a zone
    Paramater: domain (database) name string, query string eg. attribute = 'string'
    Return: resource records list'''
    if not sdb:
        sdb = boto3.client('sdb')
    query_string = 'select * from '+domain+' where '+query
    if order_by:
        query_string += ' order by '+ order_by

    return sdb.select(SelectExpression = query_string)

def select_id(domain,id, sdb=None):
    '''Get list of records for a domain (database)
    Paramater: domain name string, query string eg. attribute = 'string'
    Return: resource records list'''
    if not sdb:
        sdb = boto3.client('sdb')

    return sdb.select(SelectExpression = 'select * from '+domain+ " where itemName() = '"+ id +"'")

def select_attribute_where(domain,attribute,query,order_by=None,sdb = None):
    '''Get list of record for a domain (database)
    Paramater: domain name string, query string eg. attribute = 'string'
    Return: resource records list'''
    if not sdb:
        sdb = boto3.client('sdb')
    query_string = 'select '+attribute+' from '+domain+' where '+query
    if order_by:
        query_string += ' order by '+ order_by

    data = items_to_tuple(sdb.select(SelectExpression = query_string)['Items'])

    return data

def items_to_tuple(items):
    '''Take a sdb dictionary and convert it into
        [(item,{attribute:value}),....]'''
    i = []

    for item in items:
        a = {}
        for attribute in item['Attributes']:

            if attribute['Name'] == 'shipping' or attribute['Name'] == 'total':
                attribute['Value'] = float(attribute['Value'])

            a[attribute['Name']] = attribute['Value']
        i.append((item['Name'],a))

    return i

def items_to_csv(items):
    '''Take a sdb dictionary and convert it into list of strings
        deliminated by , ['item,attribute:value,.....', '....']'''
    i = []

    for item in items:
        line = item['Name']

        for attribute in item['Attributes']:

            if attribute['Name'] == 'shipping' or attribute['Name'] == 'total':
                attribute['Value'] = float(attribute['Value'])

            line += ','+attribute['Name']+':'+str(attribute['Value'])

        i.append(line)

    return i


def backup_db(domain,sdb=None):
    return items_to_csv(select_all(domain,sdb)['Items'])
