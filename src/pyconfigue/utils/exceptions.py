class SetupError(Exception):
    def __init__(self, *args: tuple) -> None:
        super().__init__(*args)
