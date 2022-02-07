import json
import os
from typing import Union
import marshmallow_dataclass
from game.equipment import EquipmentData

base_dir: str = os.path.abspath(os.path.dirname(__file__))
equipment_path: str = os.path.join(base_dir, "data", "equipment.json")


def read_file(file_path: str, encoding: str = "utf-8") -> Union[dict, list]:
    try:
        with open(file_path, encoding=encoding) as f:
            return json.load(f)
    except Exception:
        raise


def load_equipment() -> EquipmentData:
    try:
        return marshmallow_dataclass.class_schema(EquipmentData)().load(data=read_file(equipment_path))
    except Exception:
        raise



