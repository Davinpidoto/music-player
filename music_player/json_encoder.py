from json import JSONEncoder


class DynamicJSONEncoder(JSONEncoder):

    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()

        return super(DynamicJSONEncoder, self).default(o)


try:
    from sqlalchemy import inspect
    from sqlalchemy.orm.state import InstanceState
except ImportError as e:
    def __nomodule(*args, **kwargs): raise e
    inspect = __nomodule
    InstanceState = __nomodule


def get_entity_propnames(entity):
    ins = entity if isinstance(entity, InstanceState) else inspect(entity)
    return set(
        ins.mapper.column_attrs.keys() +  # Columns
        ins.mapper.relationships.keys()  # Relationships
    )


def get_entity_loaded_propnames(entity):
    ins = inspect(entity)
    keynames = get_entity_propnames(ins)

    if not ins.transient:
        keynames -= ins.unloaded

    if ins.expired:
        keynames |= ins.expired_attributes

    return keynames


class JsonSerializableBase(object):

    def __json__(self, exluded_keys=set()):
        return {name: getattr(self, name)
                for name in get_entity_loaded_propnames(self) - exluded_keys}