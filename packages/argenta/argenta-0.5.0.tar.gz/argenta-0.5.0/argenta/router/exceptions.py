class RepeatedFlagNameException(Exception):
    def __str__(self):
        return "Repeated registered_flag name in register command"


class TooManyTransferredArgsException(Exception):
    def __str__(self):
        return "Too many transferred arguments"


class RequiredArgumentNotPassedException(Exception):
    def __str__(self):
        return "Required argument not passed"


class IncorrectNumberOfHandlerArgsException(Exception):
    def __str__(self):
        return "Handler has incorrect number of arguments"


class TriggerCannotContainSpacesException(Exception):
    def __str__(self):
        return "Command trigger cannot contain spaces"
