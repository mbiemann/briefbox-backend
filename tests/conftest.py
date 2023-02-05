from importlib.util import spec_from_file_location, module_from_spec
import sys

from pytest import fixture


common_spec = spec_from_file_location("common", "scripts/layers/common/common.py")
common_module = module_from_spec(common_spec)
sys.modules["common"] = common_module
common_spec.loader.exec_module(common_module)

auth_spec = spec_from_file_location("auth", "scripts/layers/auth/auth.py")
auth_module = module_from_spec(auth_spec)
sys.modules["auth"] = auth_module
auth_spec.loader.exec_module(auth_module)


@fixture
def module(request):
    path = request._pyfuncitem.location[0]
    path_parts = path.split("/")
    path_parts[0] = "scripts"
    file = str(path_parts[-1])
    mod_name = file[:-3]
    file_parts = file.split("_")
    file_parts.pop(0)
    file = "_".join(file_parts)
    path_parts[-1] = file
    path = "/".join(path_parts)
    method = request._pyfuncitem.location[2]
    method_parts = str(method).split("_")
    method_parts.pop(0)
    method = "_".join(method_parts)
    spec = spec_from_file_location(mod_name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
