SET currentdir=%CD%
mkdir env
cd /d %currentdir%"\env"
py -3.8-32 -m venv %currentdir%"\env"
cd /d %currentdir%"\env\Scripts"
activate
cd /d %currentdir%
pip install -r requirments.txt
cmd /k "ECHO Program has finished running"