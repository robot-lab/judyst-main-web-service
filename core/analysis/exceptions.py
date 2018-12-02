class CommonAnalysisException(Exception):
    def __init__(self, *args, **kwargs):
        if args.count > 0:
            self.message = args[0]
        if 'message' in kwargs:
            self.message = kwargs['message']
        if self.message is None:
            self.message = 'Error'

    def __str__(self):
        return self.message
