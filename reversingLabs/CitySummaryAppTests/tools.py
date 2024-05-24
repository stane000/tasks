import os
import re
import subprocess

class ApplicationTestRunner:
 

    def run_app(self, city: str) -> str:
        """
        Runs city_summary_app and returns execution result
        """
        try:
            dir = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(dir, '..', 'CitySummaryApp\\city_summary_app.py')
            result = subprocess.run(['python', app_path, city], capture_output=True, text=True)
        except Exception as ex:
            print(f"Error occurred: {ex}")
        else:
            return result.stdout
        
class FileChecker:
    """
    The class responsible for checking the created file
    """
    def __init__(self, file_path: str) -> None:
        
        self.file_path = file_path
        self.context = ""
        with open(file_path, "r") as f:
            self.context = self.context.join(f.readlines())

    def check_if_word_in_file(self, word: str) -> None:
        assert word.lower() in self.context.lower(), f"Error: {word} not found in file, file_path: {self.file_path}"

    def check_file_length(self, expected_length: int = 100) -> None:
        assert len(self.context) > expected_length, f"Error: file does not contain more that {expected_length}" \
                                                       f"character, file_path: {self.file_path}"

    def check_if_expected_temperature_in_file(self) -> None:
        """
        Check if phrase '-100 < number < 100 degrees Celsius' in file
        """
   
        pattern = r'is (-?(100(\.0+)?|[1-9]?\d(\.\d+)?) degrees Celsius)'
        matches = re.findall(pattern, self.context)

        assert [match[0] for match in matches], f"Expected phrase not found in file, file_path: {self.file_path}"