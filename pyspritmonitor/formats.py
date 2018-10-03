import pkg_resources
import json


def load_formats():
    """Read costs and fuelings formats defined in JSON"""

    resource_package = __name__
    resource_path = '/'.join(('resources', 'formats.json'))
    formats = json.load(pkg_resources.resource_stream(resource_package, resource_path))
    return formats


formats = load_formats()
