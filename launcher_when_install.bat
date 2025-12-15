

cd C:\Users\%USERNAME%\Documents\websiteOnline\unlockTest-main

if not EXIST .venv\ echo python -m venv .venv

call %CD%\.venv\Scripts\Activate.bat

pip install -r requirements.txt

python main.py

pause