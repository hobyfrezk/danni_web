#### Appointments API

##### Data models attributes:


##### APIs
- `/api/appointments/`
    - `GET` method
        - Permission: `IsStaff`
        - List all appointments
    - `POST` method
        - Permission  
      

- `/api/appointments/{appointment_id}/`
    - `GET` method
        - Permission: `IsObjectOwnerOrIsStaff`
        - Retrieve appointment
        
- `/api/appointments/{}/cancel`
    - `POST` method
        - Permission: `IsObjectOwnerOrIsStaff`
        - Cancel an appointment