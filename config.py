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

@dataclass
class Config:
    user: User
    slot: Slot
    schedule: Schedule
    notifier: Notifier

def write_config(config: Config):
    config_dict = {
        'user': vars(config.user),
        'slot': vars(config.slot),
        'schedule': {
            'date': config.schedule.date.strftime("%Y/%m/%d"),
            'start_time': config.schedule.start_time.strftime("%H:%M:%S"),
            'end_time': config.schedule.end_time.strftime("%H:%M:%S")
        },
        'notifier': vars(config.notifier)
    }
    with open('config.yaml', 'w') as file:
        yaml.dump(config_dict, file, sort_keys=False)

def read_config() -> Config | None:
    if not Path('config.yaml').is_file():
        return None
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)
        return Config(
            user=User(**data['user']),
            slot=Slot(**data['slot']),
            schedule=Schedule(
                date=datetime.strptime(data['schedule']['date'], "%Y/%m/%d"),
                start_time=datetime.strptime(data['schedule']['start_time'], "%H:%M:%S"),
                end_time=datetime.strptime(data['schedule']['end_time'], "%H:%M:%S")
            ),
            notifier=Notifier(**data['notifier'])
        )