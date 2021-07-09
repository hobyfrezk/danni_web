#### Checkouts API

##### Data models attributes:
- _user_ (ForeignKey)
- _appointment_ (ForeignKey)
- _served_by_ (ForeignKey)
- _checked_by_ (ForeignKey)
- _products_ (ManyToManyField)
- _type_ (Choice: Spending, Recharge, Recharge and Spending)
- _amount_
- _pst_
- _gst_
- _checkout_snapshot_ 
- _notes_
- _created_at_
- _updated_at_

##### APIs
- `/api/checkouts/`
    - `GET` method
        - List all checkouts
        - Permission: `IsStaff`
    - `POST` method
        - Create new checkout
        - Permission `IsStaff`
        

- `/api/checkouts/{checkout_id}/`
    - `DESTORY` method
        - Delete a checkout
        - Permission: `IsStaff`
    - `PUT` method
        - Update a checkout
        - Permission `IsStaff`
