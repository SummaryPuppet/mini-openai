from datetime import datetime


class Time:
    def __init__(self):
        pass

    def get():
        current_time = datetime.now()

        return {
            "Hour": current_time.hour,
            "Minute": current_time.minute,
            "Day": current_time.day,
            "Month": current_time.month,
        }
