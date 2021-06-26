#### Product API

#### Data models attributes:
- _primary_key_
- _name_
- _price_
- _category_
- _created_at_
- *employee_set*  #TODO


#### APIs:
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
