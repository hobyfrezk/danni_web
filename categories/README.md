#### Category API

##### Data models attributes:
- *primary_key*
- *name*
- *products_set*

---
##### APIs:
- *<ins> localhost/category/ </ins>*
    - `GET` method  
    - return list of all categories' name
    - Permission: `AllowAny`
  
    
- *<ins> localhost/category/{pk}/ </ins>*
    - `GET` method
    - Retrieve Category for details
    - Permission: `AllowAny`
    - Returns
        - Success 200 
            - ``{
                "success": true,
                "data": {
                    "id": 1,
                    "name": "Manicure",
                    "products": [
                        {
                            "name": "Spa Polish Manicure",
                            "price": "25.00",
                            "created_at": "2021-06-24T22:24:44.088853Z"
                        },
                        {
                            "name": "Spa Shellac Manicure",
                            "price": "35.00",
                            "created_at": "2021-06-24T22:25:20.535654Z"
                        }
                    ],
                    "created_at": "2021-06-23T19:05:40.426794Z"
                }
            }``
        - Failure 404
            - ``{
                    "detail": "Not found."
                }``


-  *<ins> localhost/category/ </ins>*
    -  `POST` method
    - Create new category
    - Permission: `IsAdminUser`
    - Returns:
        - Success 201:
            - ``{
                    "success": true,
                    "data": {
                        "name": "Pedicure",
                        "created_at": "2021-XX-XXTXX:XX:XX.XXXXXXZ"
                    }
                }``
        - Error 1: **category existed**, 400.
            - ``{
                "message": "Please check input",
                "errors": {
                    "message": [
                        "category: Manicure already exists"
                    ]
                }
            }``
    
    
-  *<ins> localhost/category/ </ins>*
    - `PUT` method
    - Update existed category
    - Permission: `IsAdminUser`
    - Returns:
        - Success 200:
            - ``{
                    "success": true,
                    "data": {
                        "id": 1,
                        "name": "XXXXXX",
                        "created_at": "2021-06-23T19:05:40.426794Z"
                    }
                }``
    
    
- *<ins> localhost/category/delete/{pk}/ </ins>*
    - `POST` method
    - Delete existed category #TODO soft deletion
    - Permission: `IsAdminUser`
    
    