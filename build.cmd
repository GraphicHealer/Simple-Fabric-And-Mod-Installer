pip install -r requirements.txt
cd src
python -m pymakeself %cd% "FabricInstaller" FabricSetup.py
cd ..
move .\src\FabricInstaller.py .\
python -m PyInstaller  --hidden-import=pysimplegui --hidden-import=json -F --distpath %cd% %cd%\FabricInstaller.py
