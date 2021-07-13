# A Nail Solon Website
A Django + React web application for Salon Store. 
This is just Django/backend part.

APIs
- Account Related
    - Signup
        - POST `api/accounts/signup/`  
    - Login
        - POST `api/accounts/login/` 
    - Logout
        - POST `api/accounts/logout/` 
    - Login Status
        - GET `api/accounts/login_status/` 
        
    
- Customer Related
    - Get my profile
        - GET `api/customers/{id}/`
    - Update my profile
        - POST `api/customers/{id}/`
    - Check available slots #TODO
    - Make an appointment
        - POST `api/appointments/`
    - Check my appointments _pagination_
        - GET `api/customers/{id}/appointments/`
    - Cancel an appointment
        - POST `api/appointments/{id}/cancel/`
    - Check my checkouts history _pagination_ #TODO        
    

- Staff
    - List all customers profiles _pagination_
        - GET `api/customers/` 
    - Get a customer profile
        - GET `api/customers/{id}/`
    - List all appointments _pagination_
        - GET `api/appointments/`
    - Check reserved appointments _pagination_
        - GET `api/employees/{id}/appointments/`
    - Update a reserved appointment #TODO
    - Cancel a reserved appointment
        - POST `api/appointments/{id}/cancel/`
    - Make an appointment for customer
        - POST `api/appointments/staff-create`
    - List all checkouts _pagination_
        - GET `api/checkouts/`
    - Make a checkout (make recharges or/and spendings)
        - POST `api/checkouts/`
    - Update a checkout
        - POST `api/checkouts/{id}/`
    - Retrieve a checkout
        - GET `api/checkouts/{id}/`
    - Delete a checkout
        - DESTROY `api/checkouts/{id}/`
        
        
- Admin
    - Inherit all apis from staff
    - List all staffs
        - GET `api/employees/`
    - Create a staff
        - POST `api/employees/`
    - Remove a staff
        - POST `api/employees/{id}/`
    - Add/remove service from staff
        - POST `api/employees/{id}/add-services/`
        - POST `api/employees/{id}/remove-services/`
    
    
More Detail for APIs can be found in following links.
- [Accounts API](https://github.com/hobyfrezk/danni_web/blob/main/accounts/README.md)
- [Category API](https://github.com/hobyfrezk/danni_web/blob/main/categories/README.md)
- [Product API](https://github.com/hobyfrezk/danni_web/blob/main/products/README.md)
- [Employee API](https://github.com/hobyfrezk/danni_web/blob/main/employees/README.md)
- [Customer API](https://github.com/hobyfrezk/danni_web/blob/main/customers/README.md)
- [Appointments API](https://github.com/hobyfrezk/danni_web/blob/main/appointments/README.md)
- [Checkouts API](https://github.com/hobyfrezk/danni_web/blob/main/checouts/README.md)