"""Fix protobuf relative imports."""

import os
import re

for filename in os.listdir("randomizer/proto_gen"):
    if filename.endswith(".py") and filename != "__init__.py":
        with open(os.path.join("randomizer/proto_gen", filename), "r") as f:
            content = f.read()
        content = re.sub(r"^from common import ", "from .common import ", content, flags=re.M)
        content = re.sub(r"^import (\w+_pb2) as ", r"from . import \1 as ", content, flags=re.M)
        with open(os.path.join("randomizer/proto_gen", filename), "w") as f:
            f.write(content)
