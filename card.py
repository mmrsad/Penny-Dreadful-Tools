import types

def properties():
    return {
        'layout': 'TEXT',
        'name': 'TEXT',
        'mana_cost': 'TEXT',
        'cmc': 'REAL',
        'type': 'TEXT',
        'text': 'TEXT',
        'power': 'TEXT',
        'toughness': 'TEXT',
        'loyalty': 'TEXT',
        'image_name': 'TEXT',
        'hand': 'INTEGER',
        'life': 'INTEGER',
        'starter': 'INTEGER',
    }

def set_properties():
    return {
        'name': 'TEXT',
        'code': 'TEXT',
        'gatherer_code': 'TEXT',
        'old_code': 'TEXT',
        'magiccardsinfo_code': 'TEXT',
        'release_date': 'INT',
        'border': 'TEXT',
        'type': 'TEXT',
        'online_only': 'INT'
    }

def printing_properties():
    return {
        'system_id': 'TEXT',
        'rarity': 'TEXT',
        'flavor': 'TEXT',
        'artist': 'TEXT',
        'number': 'TEXT',
        'multiverseid': 'TEXT',
        'watermark': 'TEXT',
        'border': 'TEXT',
        'timeshifted': 'INTEGER',
        'reserved': 'INTEGER',
        'mci_number': 'TEXT'
    }

class Card(types.SimpleNamespace):
    def __init__(self, params):
        super().__init__()
        for k in params.keys():
            setattr(self, k, params[k])

class Printing(types.SimpleNamespace):
    def __init__(self, params):
        super().__init__()
        for k in params.keys():
            setattr(self, k, params[k])
