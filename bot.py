import os
import subprocess

if __name__ == "__main__":
    # Run the Streamlit app
    # Start the Uvicorn app
    os.chdir("api")
    uvicorn_process = subprocess.Popen(["uvicorn", "main:app", "--port", "3100"])
    os.chdir("..")
    # Start the Streamlit app
    streamlit_process = subprocess.Popen(["streamlit", "run", "app/auth.py"])
    # Wait for both processes to complete
    streamlit_process.wait()
    uvicorn_process.wait()
    