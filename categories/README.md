#### Category API

##### Data models attributes:
- *primary_key*
- *name*
- *products_set*

---
##### APIs:
- List Categories  `GET`  
    - return list of all categories' name
    - Permission: `AllowAny`
    - `GET` *<ins> localhost/category/ </ins>*
    
    
- Retrieve Category for details `GET` and `detail=True`
    - include products belong to this specific category
    - Permission: `AllowAny`
    - `GET` *<ins> localhost/category/{pk}/ </ins>*
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


- Create Category `POST`
    - create new category
    - Permission: `IsAdminUser`
    - `POST` *<ins> localhost/category/ </ins>*
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
    
    
- Update Category `PUT`
    - update existed category
    - Permission: `IsAdminUser`
    - `PUT` *<ins> localhost/category/ </ins>*
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
    
    
- Delete Category `POST` and `detail=True`
    - soft deletion existed category
    - Permission: `IsAdminUser`
    - `POST` *<ins> localhost/category/delete/{pk}/ </ins>*
    
    