class ProxyRequestException(Exception):
    def __init__(self, errors: list[Exception]) -> None:
        self.errors = errors
        self.message = "The request failed with the following errors:\n".join(
            [str(error) for error in errors]
        )
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"
