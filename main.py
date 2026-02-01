# TXD - by benzoXdev
import os
import subprocess

def run_script_in_terminal():
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        script_to_run = os.path.join(script_directory, "CompilerPYtoEXE.py")

        os.chdir(script_directory)
        if os.name == "nt":  # Windows
            # Use PowerShell to run the script
            command = f'Powershell -NoExit -Command "python3 {script_to_run}"'
            subprocess.run(command, shell=True)
        elif os.name == "posix":  # Linux/Mac
            # Use default terminal
            command = f'x-terminal-emulator -e "python3 {script_to_run}"'
            subprocess.run(command, shell=True)
        else:
            print("Could not determine operating system.")

    except PermissionError as e:
        print(f"Permission error: {e}. Make sure you have access to the file or directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_script_in_terminal()
