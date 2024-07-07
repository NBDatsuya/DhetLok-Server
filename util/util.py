from external_utils import inspect, swag_from


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_dict(self):
    return {to_camel_case(column.name): getattr(self, column.name) for column in self.__table__.columns}


def auto_swag_blueprint(app, blueprint):
    """自动生成蓝图的 Swagger 文档"""
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(blueprint.name + '.'):
            endpoint = app.view_functions[rule.endpoint]
            if endpoint and not hasattr(endpoint, 'spec'):
                endpoint_spec = {
                    "summary": endpoint.__name__,
                    "description": inspect.getdoc(endpoint) or "",
                    "responses": {
                        200: {
                            "description": "Success"
                        }
                    }
                }
                endpoint.__dict__['__apidoc__'] = endpoint_spec
                swag_from(endpoint_spec, methods=[rule.methods])
