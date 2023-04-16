class TranslationException(Exception):
    
    def __init__(self, message, emailaddress):
        super().__init__(message)
        self.emailaddress = emailaddress

class BatchBuilderException(TranslationException):
    pass

class EpaddModsHandlingException(TranslationException):
    pass