class AmsdalGlueConnectionsError(Exception):
    message: str

    def __str__(self) -> str:
        return self.message


class BinaryValuesNotSupportedError(AmsdalGlueConnectionsError):
    message = 'Binary values are not supported within IN.'


class DistinctOnNotSupportedError(AmsdalGlueConnectionsError):
    message = 'DISTINCT ON is not supported in this context'
