# DanniWeb
A Django + React web application for Nails salon.

## Data models
Data models for Django backend.

### Client Related Models
Models and its property for client related information.

- Member
  > This model will be used to reprensent a client in the database.
  > It contains name, balance, membership tier, transaction history of a customer. 
  
  | __`Member`__ | Usage                  | DataType                                  |
  |--------------|------------------------|-------------------------------------------|
  | id           | Primary key            | *`AutoField`*                             |
  | name         | Customer name          | *`CharField`*                             |
  | balance      | Balance of the account | *`DecimalField`*                          |
  | tier         | Membership tier        | *`ForeignKey`* of __`Tier`__ data type    |
  | transactions | Transaction history    | `Queryset` of __`Transaction`__ data type |

### Staff side
Models and its property for staff related information.

- Staff
  > This model will be used to reprensent a client in the database. 
  > It contains name, balance, membership tier, transaction history of a customer. 
  
  | __`Staff`__      | Usage                                  | DataType                                  |
  |------------------|----------------------------------------|-------------------------------------------|
  | id               | Primary key                            | *`AutoField`*                             |
  | name             | Staff name                             | *`CharField`*                             |
  | work_shifts      | Working time history                   | `Queryset` of __`WorkShift`__ data type   |
  | capable_services | Services can be provided by this staff | `Queryset` of __`Service`__ data type     |
  | transactions     | Transactions made by this staff        | `Queryset` of __`Transaction`__ data type |
  | paychecks        | Paychecks paid to this staff           | `Queryset` of __`Paycheck`__ data type    |
  
### Management side

- Tier
  > Membership tier that can be set for each customer with membership.
  
  | __`Tier`__ | Usage                                  | DataType         |
  |------------|----------------------------------------|------------------|
  | id         | Primary key                            | *`AutoField`*    |
  | name       | Tier name                              | *`CharField`*    |
  | discount   | Discount given by this membership tier | *`DecimalField`* |
  
- Service Category
  > Category of provided service
  
  | __`Category`__  | Usage                            | DataType                              |
  |-----------------|----------------------------------|---------------------------------------|
  | id              | Primary key                      | *`AutoField`*                         |
  | name            | Category name                    | *`CharField`*                         |
  | services        | Services belong to this category | `Queryset` of __`Service`__ data type |
  
- Service
  > Model of services that can be provided by the salon. Each service must belong to a category (many to one relationship -> ForeignKey) and can be provided by multiple staffs (many to many relationships -> ManyToManyField)
  
  | __`Service`__  | Usage                                    | DataType                                     |
  |----------------|------------------------------------------|----------------------------------------------|
  | id             | Primary key                              | *`AutoField`*                                |
  | name           | Service name                             | *`CharField`*                                |
  | price          | Service price                            | *`DecimalField`*                             |
  | category       | Category that this service belongs to    | *`ForeignKey`* of __`Category`__ data type   |
  | staffs         | Staffs that able to provide this service | *`ManyToManyField`* of __`Staff`__ data type |
  
- Appointment
- Transaction
- WorkShift

