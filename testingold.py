from src.logger import get_logger
from src.custom_exception import CustomException
import sys
logger=get_logger(__name__)
def dev_number_division(num1: float, num2: float) -> float:
    try:
        logger.info("Starting division operation")
        result = num1 / num2
        logger.info(f"Division successful: {num1} / {num2} = {result}")
        return result
    except Exception as e:
        logger.error("Error occurred during division operation")
        raise CustomException("Division by zero is not allowed", sys) 

if __name__ == "__main__":
    try:
        num1 = 10
        num2 = 0  # This will cause a division by zero error
        dev_number_division(num1, num2)
    except CustomException as ce:
        logger.error(f"Caught a CustomException: {ce}")