# DanniWeb
A Django + React web application for Nails salon.

## Data models
Data models for Django backend.

### Client Related Models
Models and its property for client related information.

- Member
  > This model will be used to reprensent a client in the database.
  > It contains name, balance, membership tier, transaction history of a customer. 
  
  | Member       | Usage                  | DataType                            |
  |--------------|------------------------|-------------------------------------|
  | id           | Primary key            | *`AutoField`*                       |
  | name         | Customer name          | *`CharField`*                       |
  | balance      | Balance of the account | *`DecimalField`*                    |
  | tier         | Membership tier        | __`Tier`__ data type                |
  | transactions | Transaction history    | List of __`Transaction`__ data type |

### Staff side
Models and its property for staff related information.

- Staff
  > This model will be used to reprensent a client in the database. 
  > It contains name, balance, membership tier, transaction history of a customer. 
  
  | Staff            | Usage                                  | DataType                            |
  |------------------|----------------------------------------|-------------------------------------|
  | id               | Primary key                            | *`AutoField`*                       |
  | name             | Staff name                             | *`CharField`*                       |
  | work_shifts      | Working time history                   | List of __`WorkShift`__ data type   |
  | capable_services | Services can be provided by this staff | List of __`Service`__ data type     |
  | transactions     | Transactions made by this staff        | List of __`Transaction`__ data type |
  | paychecks        | Paychecks paid to this staff           | List of __`Paycheck`__ data type    |
  
### Management side

- Tier
  > Membership tier that can be set for each customer with membership.
  
  | Tier     | Usage                                  | DataType         |
  |----------|----------------------------------------|------------------|
  | id       | Primary key                            | *`AutoField`*    |
  | name     | Tier name                              | *`CharField`*    |
  | discount | Discount given by this membership tier | *`DecimalField`* |
  
- Service Category
  > Category of provided service
  
- Service
  > 
- Appointment
- Transaction
- WorkShift

