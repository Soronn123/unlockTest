

cd C:\Users\%USERNAME%\Documents\websiteOnline

python -m venv .venv

call %CD%\.venv\Scripts\Activate.bat

pip install -r requirements.txt

python main.py
