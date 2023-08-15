from jinja2 import Template
import yaml
import os


def get_config():
    with open(f"src/config/{os.environ.get('ENV')}.yaml", "r") as f:
        template = Template(f.read())
        rendered_yaml = template.render(DB_PASSWORD=os.environ.get("DB_PASSWORD"))
    return yaml.safe_load(rendered_yaml)
