# **TXD - by benzoXdev**

This project is a **Remote Administration Tool (RAT)** based on **Discord**, which allows commands to be executed remotely on a victim machine via a Discord bot. The bot connects to a user-specified Discord server, and commands are executed via a text channel within the Discord server, making it easy to manage remotely in a controlled environment.

The bot is capable of executing custom commands prefixed with `!`, providing full access to the victim machine and facilitating real-time interaction. The project includes several tools to automate the creation and compilation of an **executable file (EXE)** that can be executed on the victim machine without raising suspicion.

---

## **Project Characteristics**

The project includes the following scripts and functionalities:

### 1. **botConnect.py**

- **Main Function**: This script generates the connection of the Discord bot that connects to a specific server.
- **Commands**:
    - `!myhelp`: Shows a list of available commands.
    - `!geolocate`: Shows the public IP address of the victim machine, plus other information about the location of said IP.
    - **Additional commands**: Custom commands that you can define to interact with the victim machine.

## !myhelp (List)

### 📜 Available Commands

### General Commands:

- `!message` = Show message box with your text  
  Syntax: `!message example`

- `!shell` = Execute shell command  
  Syntax: `!shell whoami`

- `!voice` = Text-to-speech  
  Syntax: `!voice test`

- `!admincheck` = Check if program has admin privileges

- `!cd` = Change directory

- `!dir` = List directory contents

- `!download` = Download file from target machine

- `!upload` = Upload file to target machine  
  Syntax: `!upload file.png` (with attachment)

- `!delete` = Delete a file  
  Syntax: `!delete /path/to/file.txt`

- `!write` = Write text to a file

- `!clipboard` = Get clipboard content from target machine

- `!idletime` = Get user idle time

- `!datetime` = Show current date and time

- `!currentdir` = Show current directory

---

### Privilege Escalation & System Control:

- `!getadmin` = Request admin privileges via UAC

- `!block` = Block keyboard and mouse (Admin required)

- `!unblock` = Unblock keyboard and mouse (Admin required)

- `!screenshot` = Take screenshot

- `!exit` = Exit program

- `!kill` = Kill session or process  
  Syntax: `!kill session-3` or `!kill all`

- `!uacbypass` = Attempt UAC bypass for admin privileges

- `!shutdown` = Shutdown computer

- `!restart` = Restart computer

- `!logoff` = Log off current user

- `!bluescreen` = Trigger blue screen (Admin required)

- `!migrateprocess <process_name>` = Migrate process to new instance  
  Syntax: `!migrateprocess example.exe`

---

### Security & System Modifications:

- `!prockill` = Kill process by name  
  Syntax: `!prockill process`

- `!disabledefender` = Disable Windows Defender (Admin required)

- `!disablefirewall` = Disable Windows Firewall (Admin required)

- `!critproc` = Make program a critical process (Admin required)

- `!uncritproc` = Remove critical process status (Admin required)

- `!website` = Open website on target  
  Syntax: `!website www.google.com`

- `!disabletaskmgr` = Disable Task Manager (Admin required)

- `!enabletaskmgr` = Enable Task Manager (Admin required)

- `!startup` = Add program to startup

---

### Geolocation & Other:

- `!geolocate` = Geolocate using IP lat/long

- `!listprocess` = List all processes

- `!infocounts` = Get system account info

- `!rootkit` = Launch rootkit (Admin required) [Not available]

- `!unrootkit` = Remove rootkit (Admin required) [Not available]

- `!getcams` = List camera names

- `!selectcam` = Select camera for photo  
  Syntax: `!selectcam 1`

- `!webcampic` = Take photo with selected webcam

- `!myhelp` = This help menu

### 2. **CompilerPYtoEXE.py**

- **Main Function**: Automates the bot configuration and compilation process into an executable **.exe** file.
- **Process**:
    - Requests the user for the **Bot Token** and the **Server ID** (the Discord server ID).
    - Compiles the Python file (`botConnect.py`) to an EXE file that can be executed on the victim machine.

### 3. **guiaAutoextraibleEXE.py**

- **Main Function**: Detailed instructions on how to package the `.exe` file with a `fake_error.vbs` file (which simulates a Windows error), the guide is in the script called `guiaAutoextraibleEXE.py`.
- **Goal**: Make the `.exe` file go unnoticed by packaging it in a **self-extracting** file that simulates a Windows error.

### 4. **ScriptSmartScreen**

- **Main Function**: Scripts that allow you to disable the Windows **SmartScreen** to prevent the executable file from blocking.
- Includes:
    - **DuckyScript**: To disable SmartScreen.
    - **PowerShell script**: To disable SmartScreen automatically on the victim machine.

> NOTE:

For these 2 previous scripts ``social engineering`` would be needed so that somehow the victim user executes at least the ``.ps1`` script and thus deactivates the ``SmartScreen``.
### 5. **ExclusionWindowsDefender (Windows 11)**

- **Main Function**: Tool to prevent **Windows Defender** from detecting the executable file as a threat.
- **Instructions**: Run the script `ExclusionWindowsDefender/carpetaExcluidaWindowsDefender.ps1` to create a folder excluded from Windows Defender scans, ensuring that the executable file is not detected.

> NOTE:

For this script here, in the same way as before, some type of ``social engineering`` would have to be done so that the victim user executes said script and thus generates a folder that avoids ``Windows Defender`` where our ``Trojan`` is deposited. (In Windows 10 it is not usually detected as "Malware")

---

## **Prerequisites**

Before running this project, make sure you have the following requirements configured:

1. **Python 3.x**: This project is written in ``Python3``. You can install it from the following link:
    
    - [Download Python3 from the Microsoft Store](https://apps.microsoft.com/detail/9NRWMJP3717K?hl=neutral&gl=ES&ocid=pdpshare)
    
1. **Dependencies**:
    
    - This project requires several ``Python`` libraries that will be installed automatically via the `requirements.txt` file.
    
    To install the necessary dependencies, simply run the following command in your terminal:
	
	```
	pip install -r requirements.txt
	```
    
    This will install all the necessary libraries for the project to work correctly.
    

---

## **Project Use**

### 1. **Compiling the Bot with `CompilerPYtoEXE.py`**

The ``CompilerPYtoEXE.py`` script automates the process of configuring the ``bot`` and compiling the **.exe** file.

#### Steps to run **CompilerPYtoEXE.py**:

1. **Execute the `main.py`** script by double-clicking on it.
    
    - **Important**: **Never directly run the `CompilerPYtoEXE.py`** script, as doing so will cause the compilation process to fail. The `main.py` script is responsible for correctly executing **CompilerPYtoEXE.py**.
    
2. **Provide bot data**:  

    The script will open a configuration window where you must enter the **Bot Token** and the **Server ID**:
    
    - **Bot Token**: You can obtain this token from the ``Discord Developer`` Portal.
    - **Server ID**: This is the ``ID`` of the ``Discord`` server that the bot will connect to. To obtain it, activate developer mode in ``Discord`` and right click on the server to copy its ``ID``.
    
3. **Select the `botConnect.py` file** (in the `ScriptDiscordShell` folder):

    Once your bot is configured, select the `ScriptDiscordShell/botConnect.py` file you want to use to build.
    
4. **Specifies the location of the compiled file**:  

    After selecting the file, you will be asked to choose the location where you want to save the compiled **.exe** file.
    
5. **Wait for the build to complete**:  

    The script will generate the **.exe** file that you can run on the victim machine for the bot to connect to the specified ``Discord`` server.
    
### Practical video:

https://github.com/user-attachments/assets/d5e40b83-6d99-4d84-95ef-77d46511ccb9

---

### 2. **Bypass SmartScreen Lock**

#### 1. **DuckyScript**:

- **Function**: Disable ``SmartScreen`` so that the ``.exe`` file does not crash when executed.
- **Usage**: Simply run ``DuckyScript`` in the victim's environment to disable ``SmartScreen`` with a ``BadUSB``. (Although this requires having the victim's PC at a physical level)

#### 2. **PowerShell script** (`ScriptSmartScreen/PowerShellScript/disableSmartScreen.ps1`):

- A ``PowerShell`` script is included that disables the ``SmartScreen`` automatically.
- **Run the PowerShell script** to prevent ``SmartScreen`` from blocking the execution of the generated ``.exe`` file. (This technique would require ``social engineering`` for this)

---

### 3. **Bypass Windows Defender Detection (Windows 11)**

In some cases, **Windows Defender** might detect the executable file as a threat in ``Windows 11``. To prevent this, tools are included to exclude the executable file from ``Windows Defender`` scans.

#### Steps to avoid Windows Defender detection:

1. **Execute the script `carpetaExcluidaWindowsDefender.ps1`** (in the `ExclusionWindowsDefender` folder):
    
    - This script will create a folder that will be excluded from ``Windows Defender`` scans.
    - **Run the script with PowerShell** to ensure that the folder where you will store the ``EXE`` file is not scanned by ``Windows Defender``.
    
2. **Move the .exe file to the excluded folder**:
    
    - After running the script, move the generated **.exe** file to the folder that was excluded from ``Windows Defender`` scans.

---

### 4. **Make the `.exe` File More Realistic**

To make the **.exe** file go unnoticed, the `guiaAutoextraibleEXE.py` file is included, which explains how to create a **self-extractable** archive with **WinRAR**.

#### Steps to package the `.exe` file as self-extracting:

1. **Prepare the generated `.exe`** file and the `fake_error.vbs` file (in the `buildEXE` folder, simulates a Windows error).
2. Use **WinRAR** to package both files into a **self-extracting** archive.
3. The self-extracting file will run and simulate a ``Windows`` error, making the bot go unnoticed.

### Practical video:

https://github.com/user-attachments/assets/1f287107-ead9-4403-a1e7-63d565a0eddb

---

### 5. **Discord Bot Settings**

To configure the Discord bot:

1. Run the `DiscordBotPage.bat` file to be redirected to the bot configuration page in the **Discord Developer Portal**.
2. Follow the steps on the page to configure the **Bot Token** and obtain the necessary permissions for the bot on your server.

---

## **Warning and Responsible Use**

This project is intended for educational purposes and for penetration testing in controlled environments. **Do not use this project without the explicit consent of the owner of the system you are controlling.** Unauthorized use of these types of tools is illegal and against Discord's terms of service, as well as local laws and regulations. international.

This project should not be used for malicious activities or to compromise systems without the consent of the parties involved.

---

## **Contributions**

**TXD** - Created by **benzoXdev**

If you would like to contribute to the project, please open a **pull request** or report any issues in the **issues** section of this repository.
