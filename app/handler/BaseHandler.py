from configs import config, Config

class BaseHandler:
    def __init__(self, config: Config) -> None:
        self.config = config