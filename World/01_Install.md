# Install for Larch
 
An easy way for anyone to perform XAFS analysis!! <br>(oxide and valence determination)

If you haven't set up the Larch environment, please check **https://xraypy.github.io/xraylarch/installation.html**

## Windows

1. Open https://xraypy.github.io/xraylarch/installation.html

2. Refer to **1.1. Installing from a Binary installers**, click on **Larch for Windows**, and download the Larch Binary Installers. 
<br>Then, install Larch individually.
<br>It will be installed in **C:/Users/YourName/AppData/Local/xraylarch**.

At this point, the Larch package should be automatically installed on your terminal.

> [!NOTE]
>If the download and installation were unsuccessful, please follow these steps:
>
>2-1. Click on the **GetLarch.bat script** under 1.1.1. Windows Notes and download it.
>
>2-2. Open Command Prompt and enter the following commands:
>```
>cd C:\Users\<YOURNAME>\Downloads
>GetLarch
>```

3. Open Command Prompt and type ```conda activate```. If **(base)** is displayed, it's correct.

4. Type ```conda update -y conda python pip```.
<br>Wait until the process finishes (All packages will be updated to the latest versions).

5. Type ```conda install -yc conda-forge xraylarch```.

6. Check if the environment is set up correctly by typing ```larch -m```.

7. Type ```pip install notebook``` to synchronize the virtual environment with the Jupyter notebook environment.

8. Enter ```from larch import Interpreter``` into Jupyter Notebook to verify if it can be imported correctly.

## Mac
1. Open https://xraypy.github.io/xraylarch/installation.html

2. Refer to **1.1. Installing from a Binary installers**, click on **Larch for MacOSX**, and download the Larch Binary Installers. 
<br>Then, install Larch individually.

> [!NOTE]
>If the following errors occur, please follow the instructions:
>
>*MacOS will not install non-signed 3rd party packages by default.*
><br>→ Allow the installation of this package in the "General" settings of "Security & Privacy" in System Preferences
><br> (administrator password required).
>
>*During installation, you may need to click "Install only for me".*
><br>→ If prompted for an administrator password, go back and select "Install only for me" again.

> [!NOTE]
>If the download and installation were unsuccessful, please follow these steps:
>
>2-1. Download the **GetLarch.sh script**.
> 
>If you are unable to download, copy & paste the script from the GetLarch.sh script into Notepad, and create a file named GetLarch.sh in your Downloads folder.
>
>2-2. Open Terminal and enter the following commands:
>```
>cd Downloads
>sh GetLarch.sh
>```

3. Open Command Prompt and type ```conda activate```. If **(base)** is displayed, it's correct.

4. Type ```conda update -y conda python pip```.
<br>Wait until the process finishes (All packages will be updated to the latest versions).

5. Type ```conda install -yc conda-forge xraylarch```.

6. Check if the environment is set up correctly by typing ```larch -m```.

7. Type ```pip install notebook``` to synchronize the virtual environment with the Jupyter notebook environment.

8. Enter ```from larch import Interpreter``` into Jupyter Notebook to verify if it can be imported correctly.


## Linux
1. Open https://xraypy.github.io/xraylarch/installation.html

2. Download the **GetLarch.sh script**.
<br>If you are unable to download, copy & paste the script from the GetLarch.sh script into Notepad, and create a file named GetLarch.sh in your Downloads folder.

3. Open Terminal and enter the following commands:
```
cd Downloads
sh GetLarch.sh
```

4. Open Command Prompt and type ```conda activate```. If **(base)** is displayed, it's correct.

5. Type ```conda update -y conda python pip```.
<br>Wait until the process finishes (All packages will be updated to the latest versions).

6. Type ```conda install -yc conda-forge xraylarch```.

7. Check if the environment is set up correctly by typing ```larch -m```.

8. Type ```pip install notebook``` to synchronize the virtual environment with the Jupyter notebook environment.

9. Enter ```from larch import Interpreter``` into Jupyter Notebook to verify if it can be imported correctly.
