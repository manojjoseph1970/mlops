import traceback
import sys
class CustomException(Exception):
    def __init__(self, message, message_detail: sys) -> None:
        super().__init__(message)
        self.message = message
        self.error_message=self.get_detailed_error_message(message, message_detail)
        self.trace = traceback.format_exc()
    @staticmethod
    def get_detailed_error_message(error_message, message_detail: sys) -> str:
        _, _, exc_tb = traceback.sys.exc_info()
        line_number = exc_tb.tb_lineno
        file_name = exc_tb.tb_frame.f_code.co_filename
        detailed_message = f"Error occurred in script: {file_name} at line number: {line_number} with message: {error_message}"
        return detailed_message
    def __str__(self):
        return f"CustomException: {self.message}\nTraceback:\n{self.trace}"