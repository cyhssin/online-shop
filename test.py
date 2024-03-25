import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("EMAIL_PASSWORD"))