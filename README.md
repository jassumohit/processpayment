# ProcessPayment  

## How to run the project  
### Pre-requisites -  
1. Pipenv  
2. Python 3.x  

### Steps to run on command line 
1. Clone repo  
2. CD to root directory of repo  
3. For installing dependencies and modules, Run  
`pip install -r requirements.txt`
4. For application, Run  
`python app.py`  
5. To exit, press *ctrl+c*  

### Steps to Test application  
1. Open command line or terminal
2. cd to root directory of cloned repo  
3. Run  
`pytest`  
This will run all the test cases and show the report on terminal  

### Assumptions  
1. Only 16 digits creditcard validation of VISA and MasterCard(starting with 4 or 5[1-5])  
2. ExpirationDate format is %d/%m/%Y i.e. 16/10/2022  
3. CardHolder name can be alphanumeric, only none is validated  
4. External Gateways will always return True when data fields are available and validated
