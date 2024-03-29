#### Customer API

##### Data models attributes:
- _user_ (OneToOneField)
- _first_name_ 
- _last_name_
- _gender_
- _phone_
- _balance_
- _created_at_
- _updated_at_

##### APIs
-  *<ins> /api/accounts/signup/ </ins>*
    - `POST` Method 
    - Create new account and new customer profile
    - Permission: `AllowAny`
    
    
-  *<ins> /api/customers/ </ins>*
    - `GET` Method
    - List all customers (_pagination enabled_)
    - Permission: `IsStaff`
    
- *<ins>/api/customers/{customer_id}/</ins>*
    - `GET` Method
    - Retrieve a customer
    - Permission: `IsObjectOwnerOrIsStaff`


- *<ins>/api/customers/{customer_id}/update-info/</ins>*
    - `POST` Method
    - Update info (first_name, last_name, gender, phone)
    - Permission: `IsObjectOwnerOrIsStaff`
    
    
- *<ins>/api/customers/{customer_id}/update-balance/</ins>*
    - `POST` Method
    - Update balance
    - Permission: `IsStaff`


- *<ins>/api/customers/{customer_id}/appointments/</ins>* 
    - `GET` Method
    - List appointments for a customer (_pagination enabled_)
    - Permission: `IsObjectOwnerOrIsStaff`
   
   
- *<ins>/api/customers/{customer_id}/checkouts/</ins>* 
    - `GET` Method
    - List checkouts for a customer (_pagination enabled_)
    - Permission: `IsObjectOwnerOrIsStaff`