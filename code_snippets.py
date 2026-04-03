# TO PREVIEW ON JUPYTER
import subprocess
from IPython.display import display, Markdown
result = subprocess.run(
    [r"C:\Users\slate\B_MY PROJECTS\.venv\Scripts\python.exe", "1a_Day_1_playwright.py"],
    capture_output=True,
    text=True,
    cwd=r"C:\Users\slate\B_MY PROJECTS\notebooks"
)
print("OUTPUT:", result.stdout)
print("ERROR:", result.stderr)

# 