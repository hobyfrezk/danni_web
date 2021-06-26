# Danni Web
A Django + React web application for Nails salon.

## Data models
Data models for Django backend.

#### Category API

##### Data models attributes:
- *primary_key*
- *name*
- *products_set*  #TODO

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
    
 ---
 #### Product API

##### Data models attributes:
- _primary_key_
- _name_
- _price_
- _category_
- _created_at_
- *employee_set*  #TODO


##### APIs:
- List All Products `GET` `'api/products/'`
    - Return all products  
    - Permission: `AllowAny`
    - Return 
        ``{
            "success": true,
            "products": [
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
                },
                {
                    "id": 4,
                    "name": "Discount",
                    "price": "-3.00",
                    "category": null,
                    "created_at": "2021-06-26T05:51:01.579460Z"
                }
            ]
        }``
        
        
- List Products under Specific Category `GET` `'api/products/?category={category_name}'`
    - Return products under a specific category
    - Permission: `AllowAny`
    - Return ``{
                "success": true,
                "products": [
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
                    }
                ]
            }``
            
            
- List Products under Specific Employee #TODO


- Create Products `POST` `'/api/products/'`
    - Create a new product by `Request.data`
    - `Request.data = {
            "name": "product_name",
            "price": "XX",
            "category_id"(optional): category.id
        }`
    - `category_id is Int or None`
    - `unique_together = (('category', 'name'), )`
    - Permission: `IsAdminUser`
    - Return ``{
                "id": 10,
                "name": "Product_name",
                "price": "XX.XX",
                "category_id": X,
                "created_at": "2021-06-26T06:19:04.689476Z"
                }``
                
                
- Update Products `PUT` `'/api/products/{product_id}/'`
    - Permission `IsAdminUser`
    - `Request.data = {
            "name": "product_name",
            "price": "XX",
            "category_id"(optional): category.id, 
        }`
    - Return ``{
    "id": 10,
    "name": "Product_name_new",
    "price": "XX.XX",
    "category_id": category.id/null,
    "created_at": "2021-06-26T06:19:04.689476Z"
}``


- Delete Products `DELETE` `'/api/products/{product_id}/'`
    - Delete an existed product
    - Permission `IsAdminUser`
    - Return ``{
                "success": true
                }``


---