import os
import sys

os.system(f'streamlit run "{os.path.join(os.path.dirname(sys.argv[0]), "streamlit_dashboard/dashboard.py")}"')
