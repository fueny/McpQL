from dotenv import load_dotenv
import os

load_dotenv()
zhipu_key = os.environ.get('zhipu')
print(zhipu_key)