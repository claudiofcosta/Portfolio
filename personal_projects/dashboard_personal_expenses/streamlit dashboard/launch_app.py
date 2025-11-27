import os
import sys

# Launches your Streamlit app inside the .exe
app_path = os.path.join(os.path.dirname(sys.argv[0]), "streamlit dashboard\dashboard.py")
os.system(f'streamlit run "{app_path}"')
