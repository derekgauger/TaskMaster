import PyInstaller.__main__

PyInstaller.__main__.run([
   'task_master.py',
   '--onefile',
   '--windowed',
   "--icon=task_master_icon.ico"
])