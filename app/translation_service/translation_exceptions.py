class TranslationException(Exception):
    
    def __init__(self, message, emailaddress):
        super().__init__(message)
        self.emailaddress = emailaddress

class BatchBuilderException(TranslationException):
    def __init__(self, message, emailaddress=None):
        super().__init__(message, emailaddress)


class EpaddModsHandlingException(TranslationException):
    def __init__(self, message, emailaddress=None):
        super().__init__(message, emailaddress)
        
class MissingEmbargoBasisException(EpaddModsHandlingException):
    def __init__(self, message, emailaddress=None):
        super().__init__(message, emailaddress)