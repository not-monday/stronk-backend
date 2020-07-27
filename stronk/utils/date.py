from datetime import datetime

def date_str_to_date(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%d')

def date_time_str_to_date(date: str) -> datetime:
    return datetime.fromisoformat(date)