import json
from randomizer.Enums.Items import Items
from randomizer.Lists.Item import Item
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Types import Types
from randomizer.Enums.Events import Events
from randomizer.Enums.Collectibles import Collectibles
from randomizer.LogicClasses import Event
import sys
import os
import re
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(parent_dir)


def split_camel_case(name):
    return ' '.join([x for x in re.split('([A-Z][a-z]+)', name) if x])


def strip_name(name):
    return name.replace(" ", "").replace(":", "").replace("-", "").replace("'", "").lower()


class RegionNode:
    """A node representing a region in the logic graph."""

    def __init__(self,
                 id: Regions | str,
                 Name,
                 Class="Region",
                 Type="Region"):

        prefix = Class[0].lower() + Type[0].lower() + "-"

        _id = id if isinstance(id, str) else strip_name(id.name.lower())

        # self.id = prefix+_id
        self.id = _id
        self.Name = Name
        self.Class = Class
        self.Type = Type

    def to_dict(self):
        """Convert the RegionNode to a dictionary."""
        return {
            "id": self.id,
            "Name": self.Name,
            "Class": self.Class,
            "Type": self.Type
        }

    def to_json(self):
        """Convert the RegionNode to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)


class RegionEdge:
    """An edge representing a region in the logic graph."""

    def __init__(self,
                 id,
                 source: RegionNode | str,
                 target: RegionNode | str,
                 Name: str,
                 Logic: object | bool = True,
                 Class: str = "Transition",
                 type: str = "Neighbourhood",
                 ):

        if id is None:
            id = f"edge_{os.urandom(4).hex()}"

        _name = Name if Name else source.Name + " to " + target.Name

        self.id = id
        self.Name = _name
        self.source = source.id if isinstance(source, RegionNode) else source
        self.target = target.id if isinstance(target, RegionNode) else target
        self.sourceType = "Region"
        self.targetType = "Location"
        self.Class = Class
        self.type = type
        self.Requires = Logic

    def to_dict(self):
        """Convert the RegionEdge to a dictionary."""
        return {
            "id": self.id,
            "Name": self.Name,
            "source": self.source,
            "target": self.target,
            "sourceType": self.sourceType,
            "targetType": self.targetType,
            "Class": self.Class,
            "type": self.type,
            "Requires": self.Requires
        }

    def to_json(self):
        """Convert the RegionEdge to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)


class QueryLogic:
    def __init__(self, combinator: str, rules: list):
        if combinator not in ['or', 'and']:
            raise ValueError("Combinator must be 'or' or 'and'")
        self.combinator = combinator
        self.rules = rules

    def to_dict(self):
        return {
            "combinator": self.combinator,
            "rules": self.rules
        }
    
    def to_json(self):
        """Convert the QueryLogic to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)


class CheckEdge:
    """A node representing a region in the logic graph."""

    def __init__(self, id, Name: str, source: RegionNode | str, target: Items | Collectibles | str, Types, Class, Logic: object | bool = True, Persona='any'):
        self.id = id
        self.Name = Name
        self.source = source.id if isinstance(source, RegionNode) else source
        self.target = target.name.lower() if isinstance(
            target, (Items, Collectibles)) else target
        self.sourceType = "Region"
        self.type = "Location"
        self.targetType = "Item"
        self.Types = Types
        self.Class = Class
        self.Persona = Persona
        self.Requires = Logic
        self.Rewards = QueryLogic('and', [{"Name": self.target, "Amount": 1}])

    def set_reward_amount(self, reward: str = None, amount: int = 1):
        if reward:
            self.Rewards["Name"] = reward
        self.Rewards["Amount"] = amount

    def set_multiple_rewards(self, rewards: QueryLogic):
        self.Rewards = rewards

    def to_dict(self):
        """Convert the RegionNode to a dictionary."""
        rewards = self.Rewards.to_dict() if isinstance(self.Rewards, QueryLogic) else self.Rewards
        return {
            "id": self.id,
            "Name": self.Name,
            "source": self.source,
            "target": self.target,
            "type": self.type,
            "sourceType": self.sourceType,
            "targetType": self.targetType,
            "Types": self.Types,
            "Class": self.Class,
            "Requires": self.Requires,
            "Persona": self.Persona,
            "Rewards": rewards
        }

    def to_json(self):
        """Convert the RegionNode to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)


class ItemNode:
    """A node representing an item in the logic graph."""

    def __init__(self, id: Items, item: Item):
        itemType = item.type.name

        if (item.type == Types.Shop):
            itemType = "Move"

        prefix = ""

        _id = id if isinstance(id, str) else id.name.lower()

        self.id = (prefix+_id).lower()
        self.Name = item.name
        self.Class = "Item"
        self.Type = itemType

    def to_dict(self):
        """Convert the ItemNode to a dictionary."""
        return {
            "id": self.id,
            "Name": self.Name,
            "Class": self.Class,
            "Type": self.Type
        }

    def to_json(self):
        """Convert the ItemNode to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)


class EventNode:
    """A node representing an item in the logic graph."""

    def __init__(self, event: Events):
        prefix = ""

        _id = event if isinstance(event, str) else event.name.lower()

        self.id = (prefix+_id).lower()
        self.Name = split_camel_case(event.name)
        self.Class = "Item"
        self.Type = "Event"

    def to_dict(self):
        """Convert the ItemNode to a dictionary."""
        return {
            "id": self.id,
            "Name": self.Name,
            "Class": self.Class,
            "Type": self.Type
        }

    def to_json(self):
        """Convert the ItemNode to a JSON string."""
        return json.dumps(self.to_dict(), indent=4)
