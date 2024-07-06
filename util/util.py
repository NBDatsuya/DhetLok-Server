import json


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_dict(self):
    return {to_camel_case(column.name): getattr(self, column.name) for column in self.__table__.columns}
