import pandas as pd
import sys
from src.logger import logging
from src.exception import CustomException

def parse_whatsapp(file_path):
    try:
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if ' - ' in line:
                    parts = line.split(' - ', 1)
                    rest = parts[1]
                    if ': ' in rest:
                        sender, message = rest.split(': ', 1)
                        data.append({'sender': sender.strip(), 'message': message.strip()})
        
        messages = pd.DataFrame(data)
        logging.info('WhatsApp chat parsed successfully')
        return messages
    
    except Exception as e:
        raise CustomException(e, sys)