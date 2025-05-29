class ProcessorResponse:
    def __init__(self, task_id: str, message: str):
        self.task_id = task_id
        self.message = message

class UrlProcessorResponse(ProcessorResponse):
    def __init__(self, task_id: str, url: str, message: str):
        super().__init__(task_id, message)
        self.url = url

class CsvProcessorResponse(ProcessorResponse):
    def __init__(self, task_id: str, file_url: str, message: str):
        super().__init__(task_id, message)
        self.file_url = file_url