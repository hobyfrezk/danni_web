#### Employees API

##### Data models attributes:
- _user_ (OneToOneField)
- _services_ (ManyToManyField)
- _nickname_
- _created_at_
- _updated_at_

##### APIs
- `'/api/employees/'`
    - `GET` method
        - Return all employees
        - Permission `AllowAny`
        - Returns ``
        {
        "success": true,
        "employees": [
            {
                "id": 2,
                "user_id": 1,
                "services": [
                    {
                        "id": 1,
                        "name": "Spa Polish Manicure",
                        "price": "25.00",
                        "category": {
                            "id": 1,
                            "name": "Manicure",
                            "created_at": "2021-06-23T19:05:40.426794Z"
                        },
                        "created_at": "2021-06-24T22:24:44.088853Z"
                    },
                    {
                        "id": 2,
                        "name": "Spa Shellac Manicure",
                        "price": "35.00",
                        "category": {
                            "id": 1,
                            "name": "Manicure",
                            "created_at": "2021-06-23T19:05:40.426794Z"
                        },
                        "created_at": "2021-06-24T22:25:20.535654Z"
                    },
                    {
                        "id": 3,
                        "name": "Toe cure nail polish",
                        "price": "35.00",
                        "category": {
                            "id": 5,
                            "name": "Pedicure",
                            "created_at": "2021-06-24T14:30:25.585314Z"
                        },
                        "created_at": "2021-06-25T02:07:32.321066Z"
                    }
                ],
                "nickname": "admin",
                "created_at": "2021-06-29T16:15:50.985052Z"
            }
        ]
    }
    ``
    - `POST` method
        - Create a mew employee     
        - Permission `IsAdmin`
        - Return ``{'id': 3, 'user': OrderedDict([('username', 'client_account'), ('email', 'client_test@minenails.com'), ('is_staff', True), ('is_superuser', False)]), 'services': [OrderedDict([('id', 1), ('name', 'Spa Polish Manicure'), ('price', '25.00'), ('category', OrderedDict([('id', 1), ('name', 'Manicure'), ('created_at', '2021-06-30T21:42:29.512660Z')])), ('created_at', '2021-06-30T21:42:29.513680Z')])], 'nickname': 'ergou', 'created_at': '2021-06-30T21:42:29.527023Z'}
``

- `'/api/employees/{employee_id}/'`
    - `GET` method
        - Retrieve An Employee
        - Permission `AllowAny`
        - Return ``{
    "id": 2,
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@minenails.com",
        "is_staff": true,
        "is_superuser": true
    },
    "services": [
        {
            "id": 1,
            "name": "Spa Polish Manicure",
            "price": "25.00",
            "category": {
                "id": 1,
                "name": "Manicure",
                "created_at": "2021-06-23T19:05:40.426794Z"
            },
            "created_at": "2021-06-24T22:24:44.088853Z"
        },
        {
            "id": 2,
            "name": "Spa Shellac Manicure",
            "price": "35.00",
            "category": {
                "id": 1,
                "name": "Manicure",
                "created_at": "2021-06-23T19:05:40.426794Z"
            },
            "created_at": "2021-06-24T22:25:20.535654Z"
        },
        {
            "id": 3,
            "name": "Toe cure nail polish",
            "price": "35.00",
            "category": {
                "id": 5,
                "name": "Pedicure",
                "created_at": "2021-06-24T14:30:25.585314Z"
            },
            "created_at": "2021-06-25T02:07:32.321066Z"
        }
    ],
    "nickname": "admin",
    "created_at": "2021-06-29T16:15:50.985052Z"
}``
    - `DELETE` method
        - Remove employee status from a user
        - Permission `IsAdmin`
        - Return ``{'success': True}``
        

- `'/api/employees/{employee_id}/add-services/'`
    - `POST` method
        - Add Products to An Employee
        - Permission `IsAdmin`
        - `Request.data = {
            'services': [product.id, ...]
        }`
        - Return ``{'success': True, 'employee': {'id': 11, 'user': OrderedDict([('id', 10), ('username', 'client_account'), ('email', 'client_test@minenails.com'), ('is_staff', True), ('is_superuser', False)]), 'services': [OrderedDict([('id', 7), ('name', 'Spa Polish Manicure'), ('price', '25.00'), ('category', OrderedDict([('id', 10), ('name', 'Manicure'), ('created_at', '2021-07-01T01:30:54.576792Z')])), ('created_at', '2021-07-01T01:30:54.577770Z')]), OrderedDict([('id', 8), ('name', 'Spa Shellac Manicure'), ('price', '35.00'), ('category', OrderedDict([('id', 10), ('name', 'Manicure'), ('created_at', '2021-07-01T01:30:54.576792Z')])), ('created_at', '2021-07-01T01:30:54.578140Z')])], 'nickname': 'ergou', 'created_at': '2021-07-01T01:30:54.586121Z'}}``


- `'/api/employees/{employee_id}/remove-services/'`
    - `POST` method
        - Remove products from an employee
        - Permission `IsAdmin`
        - `Request.data = {'services': [product.id, ...]}`
        - Return ``{'success': True, 'employee': {'id': 11, 'user': OrderedDict([('id', 10), ('username', 'client_account'), ('email', 'client_test@minenails.com'), ('is_staff', True), ('is_superuser', False)]), 'services': [OrderedDict([('id', 7), ('name', 'Spa Polish Manicure'), ('price', '25.00'), ('category', OrderedDict([('id', 10), ('name', 'Manicure'), ('created_at', '2021-07-01T01:30:54.576792Z')])), ('created_at', '2021-07-01T01:30:54.577770Z')]), OrderedDict([('id', 8), ('name', 'Spa Shellac Manicure'), ('price', '35.00'), ('category', OrderedDict([('id', 10), ('name', 'Manicure'), ('created_at', '2021-07-01T01:30:54.576792Z')])), ('created_at', '2021-07-01T01:30:54.578140Z')])], 'nickname': 'ergou', 'created_at': '2021-07-01T01:30:54.586121Z'}}
    ``

- `'/api/employees/{employee_id}/appointments/'` 
    - `GET` method
        - Get appointments for an employee (_pagination enabled_)
        - Permission `IsStaff`

- `'/api/employees/{employee_id}/checkouts/'` 
    - `GET` method
        - Get checkouts served by an employee (_pagination enabled_)
        - Permission `IsStaff`
