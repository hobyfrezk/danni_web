#### Appointments API

##### Data models attributes:
- _user_ (ForeignKey)
- _appointment_time_ 
- _duration_
- _services_ (ManyToManyField)
- _staff_ (ForeignKey)
- _is_canceled_
- _created_at_
- _updated_at_

##### APIs
- `/api/appointments/`
    - `GET` method
        - Permission: `IsStaff`
        - List all appointments (_pagination enabled_)
    - `POST` method
        - Permission  `IsAuthenticated`
        - Create new appointment
        

- `/api/appointments/{appointment_id}/`
    - `GET` method
        - Permission: `IsObjectOwnerOrIsStaff`
        - Retrieve appointment
        
        
- `/api/appointments/{}/cancel`
    - `POST` method
        - Permission: `IsObjectOwnerOrIsStaff`
        - Cancel an appointment