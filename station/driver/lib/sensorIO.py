class SensorIO:
    def read(self) -> dict:
        raise NotImplementedError

    def activate(self) -> bool:
        raise NotImplementedError
