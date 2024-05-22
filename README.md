
# Address Book

This project an address book application where API users can create, update and delete
addresses.
The address should:
- contain the coordinates of the address.
- be saved to an SQLite database.
- be validated
API Users should also be able to retrieve the addresses that are within a given distance and
location coordinates.


## Deployment

### Python Version
- python 3.11

#### Run server
- Create virtual environment
```bash
python -m venv env
```
- Activate virtual environment
  - for windows ``` env/Scripts/activate ``` 
  - for Linux ``` source env/bin/activate```
- Install requirements
```bash 
pip install -r requirements.txt 
```
- Run local server
```bash
python main.py
```