

cd C:\Users\%USERNAME%\Documents\websiteOnline\unlockTest-main

python -m venv .venv

call %CD%\.venv\Scripts\Activate.bat

pip install -r requirements.txt

python main.py
