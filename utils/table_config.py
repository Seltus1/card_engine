
import json

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LayoutSection:
    name: str
    type: str
    function: str
    text: Optional[str] = None
    spacing: Optional[int] = None
    uneven: Optional[bool] = None
    players: Optional[List[str]] = None
    middle_text: Optional[str] = None
    data_type: Optional[str] = None


@dataclass
class PaddingRule:
    range_start: int
    range_end: Optional[int]
    change: int



@dataclass
class TableConfig:
    layout_sections: List[LayoutSection]
    padding_rules: List[PaddingRule]
    
    @classmethod
    def from_json(cls, json_path: str) -> 'TableConfig':
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Parse layout sections
        sections = []
        for section_data in data['layout_sections']:
            section = LayoutSection(**section_data)
            sections.append(section)
        
        # Parse padding rules
        rules = []
        for rule_data in data['padding_progression']:
            rule = PaddingRule(
                range_start=rule_data['range'][0],
                range_end=rule_data['range'][1],
                change=rule_data['change']
            )
            rules.append(rule)
        
        return cls(layout_sections=sections, padding_rules=rules)


class TableConfigManager:
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = None
    


    @property
    def config(self) -> TableConfig:
        if self._config is None:
            self._config = TableConfig.from_json(self.config_path)
        return self._config
    


    def get_section(self, name: str) -> Optional[LayoutSection]:
        for section in self.config.layout_sections:
            if section.name == name:
                return section
        return None
    


    def get_padding_change(self, index: int) -> int:
        for rule in self.config.padding_rules:
            if rule.range_end is None:
                if index >= rule.range_start:
                    return rule.change
            else:
                if rule.range_start <= index < rule.range_end:
                    return rule.change
        return 0
