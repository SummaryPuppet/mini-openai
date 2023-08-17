from weather import Weather
from pc_program import PcProgram
from tts import TTS


class Command:
    def __init__(self):
        self.options = {
            "get_weather": {"instance": Weather(), "arg": "ubicacion"},
            "open_edge": {"instance": PcProgram(), "arg": "website"},
        }

    def execute(self, command: str, args):
        option = self.options.get(command)

        arg = option["arg"]
        instance = option["instance"].get(arg)
        print(instance)
        tts_file = TTS().process(args[arg])

        return tts_file
