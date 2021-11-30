from typing import Any, Dict
from ruamel import yaml
from ruamel.yaml import YAML


def load_yaml(filename: str):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def convert(v1_yaml_obj: Dict[Any, Any], filename: str) -> bool:

    triggers = []
    for trigger in v1_yaml_obj.get('triggers', {}):
        if trigger.get('type') == 'meya.dialogflow':
            triggers.append({"expect": "dialogflow", "intent": trigger['properties']['intent'], "language": trigger['properties']['language'], "integration": "integration.google.dialogflow.dialogflow"})


    steps = []
    states = v1_yaml_obj.get("states", {})
    for state_key in states.keys():
        component = states[state_key].get('component')
        properties = states[state_key].get('properties')
        delay = states[state_key].get('delay')
        if not component:
            break

        if component == 'meya.text':
            steps.append({"say": properties.get('text')})
            if delay:
                steps.append({'delay': delay.get('relative', 1)})

        if component == "meya.text_buttons":
            steps.append({"ask": properties.get('text'), "quick_replies": [{"text": button["text"], "action": {"flow": f"flow.{button['flow']}"}} for button in properties["buttons"]]})

    if not steps:
        return False

    save_v2_yaml({"triggers": triggers, "steps": steps}, filename)
    return True


def save_v2_yaml(v2_yaml_format: Dict[Any, Any], filename: str):
    round_trip_yaml = YAML(typ="rt")
    round_trip_yaml.indent = 2
    round_trip_yaml.sequence_indent = 4
    round_trip_yaml.sequence_dash_offset = 2
    with open(filename, 'w') as file:
        round_trip_yaml.dump(data=v2_yaml_format, stream=file)

    return True

