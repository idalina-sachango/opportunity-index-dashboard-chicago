PLATFORM=$(python3 -c 'import platform; print(platform.system())')

echo -e "1. Creating new virtual environment..."

python3 -m venv env 

echo -e "2. Installing Requirements..."

source env/bin/activate
pip install -r requirements.txt

echo -e "3. Loading in API data for show..."
for FILE in api_code/*
do

   python3 -m $FILE
   echo -e "data from $FILE loaded into tools4schools/data"
done

deactivate 
echo -e "Install is complete."