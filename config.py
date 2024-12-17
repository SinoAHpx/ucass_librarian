from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
import yaml

@dataclass
class User:
    username: str
    password: str

@dataclass
class Slot:
    room: str
    seat: str

@dataclass
class Schedule:
    date: datetime
    start_time: datetime
    end_time: datetime

@dataclass
class Notifier:
    gmail: str | None
    password: str | None
    recipient: str | None

@dataclass
class Config:
    user: User
    slot: Slot
    schedule: Schedule
    notifier: Notifier

def write_default_config():
    config_dict = {
        'user': {
            'username': 'your student card number',
            'password': 'your password'
        },
        'slot': {
            'room': 'the room, example: A201',
            'seat': 'the seat, example: 001'
        },
        'schedule': {
            'date': datetime.now().strftime("%Y/%m/%d"),
            'start_time': '08:00:00',
            'end_time': '22:00:00'
        },
        'notifier': {
            'gmail': None,
            'password': None, 
            'recipient': None
        }
    }
    with open('config.yaml', 'w') as file:
        yaml.dump(config_dict, file, sort_keys=False)

_config_cache = None

def read_config() -> Config | None:
    global _config_cache
    if _config_cache is not None:
        return _config_cache
    
    if not Path('config.yaml').is_file():
        return None
        
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        _config_cache = Config(
            user=User(**data['user']),
            slot=Slot(**data['slot']),
            schedule=Schedule(
                date=datetime.strptime(data['schedule']['date'], "%Y/%m/%d"),
                start_time=datetime.strptime(data['schedule']['start_time'], "%H:%M:%S"),
                end_time=datetime.strptime(data['schedule']['end_time'], "%H:%M:%S")
            ),
            notifier=Notifier(**data['notifier'])
        )
        return _config_cache