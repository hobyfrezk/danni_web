## Category API

#### Data models attributes:
- *primary_key*
- *name*

---
#### APIs json:
- List Categories  `GET`  
    - return list of all categories' name
    - Permission: `AllowAny`
    - `GET` *<ins> localhost/category/ </ins>*
    

- Retrieve Category with details `GET` and `detail=True`
    - include products belong to this specific category
    - Permission: `AllowAny`
    - `GET` *<ins> localhost/category/{pk}/ </ins>*
    

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
                        "created_at": "2021-06-24T14:30:25.585314Z"
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
    
- Delete Category `POST` and `detail=True`
    - soft deletion existed category
    - Permission: `IsAdminUser`
    - `POST` *<ins> localhost/category/delete/{pk}/ </ins>*