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
    - `GET` *<ins> localhost/category/1 </ins>*
    

- Create Category `POST`
    - create new category
    - Permission: `IsStaff`
    - `POST` *<ins> localhost/category/ </ins>*
    
- Update Category `PUT`
    - update existed category
    - Permission: `IsStaff`
    - `PUT` *<ins> localhost/category/ </ins>*
    
- Delete Category `POST` and `detail=True`
    - soft deletion existed category
    - Permission: `IsStaff`
    - `POST` *<ins> localhost/category/delete/1 </ins>*