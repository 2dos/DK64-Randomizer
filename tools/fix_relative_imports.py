import os

for filename in os.listdir('randomizer/proto_gen'):
    if filename.endswith('.py') and filename != '__init__.py':
        with open(os.path.join('randomizer/proto_gen', filename), 'r') as f:
            content = f.read()
        content = content.replace('from common', 'from .common')
        with open(os.path.join('randomizer/proto_gen', filename), 'w') as f:
            f.write(content)