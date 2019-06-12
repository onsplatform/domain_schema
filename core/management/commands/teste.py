import yaml, io, os


with open('D:/platform/domain_schema/core/management/commands/e_ageoper.yaml', 'r', encoding='utf-8') as stream:
    yamlDict = yaml.load(stream,Loader=yaml.FullLoader)
    #print(yamlDict)
    #print(yamlDict.items())
    #myEntity = Entity()
    #myFields = Field()

    #myEntity.name = '1st key of dict'
    
    #myFields.entity = '1st key of dict'
    #myFields.name = 'id_age'
    #myFields.field_type = 'string'
    
    #myEntity.save()

    entitity = ''
    fields = {}

    for d in yamlDict.items():
        entitity = d[0]
        fields = d[1]

    #print(entitity)
    #print(fields)

    for k,v in fields.items():
        print(k, v)

"""
    for k in yamlDict.items():
        print(k[1])
"""