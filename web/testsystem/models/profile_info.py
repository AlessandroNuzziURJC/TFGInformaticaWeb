from django.conf import settings
import os

class ProfileInfo:
    file_path = os.path.join(settings.BASE_DIR, 'testsystem/files/user_data.txt')

    def get_data(self):
        output = {}

        self.user_data_extract(output)
        return output
    
    def user_extract_data(self, output):
        if not os.path.exists(self.path):
            return None
        
        with open(self.file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split(': ')
                output[key.strip()] = value.strip()

        return output
    
    def instance_types_data(self, output):
        pass