# Danni Web
A Django + React web application for Nails salon.

## Data models
Data models for Django backend.

### Client Related Models
Models and its property for client related information.

#### Member
  > This model will be used to reprensent a client in the database.
  > It contains name, balance, membership tier, transaction history of a customer. 
  
  | __`Member`__        | Usage                  | DataType                                  |
  |---------------------|------------------------|-------------------------------------------|
  | id                  | Primary key            | *`AutoField`*                             |
  | first_name          | Customer first name    | *`CharField`*                             |
  | last_name           | Customer last name     | *`CharField`*                             |
  | phone               | Customer phone number  | *`CharField`*                             |
  | balance             | Balance of the account | *`DecimalField`*                          |
  | tier                | Membership tier        | *`ForeignKey`* of __`Tier`__ data type    |
  | created_at          | Membership start time  | *`DateTimeField`*                         |
  | modified_at         | Membership updated time| *`DateTimeField`*                         |
  | transactions        | Transaction history    | `Queryset` of __`Transaction`__ data type |
  | appointments_past   | Past appointments      | `Queryset` of __`Appointment`__ data type |
  | appointments_active | Active appointments    | `Queryset` of __`Appointment`__ data type |

### Staff side
Models and its property for staff related information.

#### Staff
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

#### Tier
  > Membership tier that can be set for each customer with membership.
  
  | __`Tier`__ | Usage                                  | DataType         |
  |------------|----------------------------------------|------------------|
  | id         | Primary key                            | *`AutoField`*    |
  | name       | Tier name                              | *`CharField`*    |
  | discount   | Discount given by this membership tier | *`DecimalField`* |
  
#### Service Category
  > Category of provided service
  
  | __`Category`__  | Usage                            | DataType                              |
  |-----------------|----------------------------------|---------------------------------------|
  | id              | Primary key                      | *`AutoField`*                         |
  | name            | Category name                    | *`CharField`*                         |
  | services        | Services belong to this category | `Queryset` of __`Service`__ data type |
  
#### Service
  > Model of services that can be provided by the salon. Each service must belong to a category (many to one relationship -> ForeignKey) and can be provided by multiple staffs (many to many relationships -> ManyToManyField)
  
  | __`Service`__  | Usage                                    | DataType                                     |
  |----------------|------------------------------------------|----------------------------------------------|
  | id             | Primary key                              | *`AutoField`*                                |
  | name           | Service name                             | *`CharField`*                                |
  | price          | Service price                            | *`DecimalField`*                             |
  | category       | Category that this service belongs to    | *`ForeignKey`* of __`Category`__ data type   |
  | staffs         | Staffs that able to provide this service | *`ManyToManyField`* of __`Staff`__ data type |
  
#### Appointment
  > Appointment can be made online by customer and it contains the infomation about the customer who made it, the staff it related to and the reserved time of it, also it could optionally contains the services required by the customer.
 
  | __`Appointment`__ | Usage                                       | DataType                                             |
  |-------------------|---------------------------------------------|------------------------------------------------------|
  | id                | Primary key                                 | *`AutoField`*                                        |
  | member            | Client who made the appointment             | *`ForeignKey`* of __`Member`__ data type             |
  | time_start        | Appointment start time                      | *`DateTimeField`*                                    |
  | time_end          | Appointment end time                        | *`DateTimeField`*                                    |
  | work_shift        | Devoted shift time for this appointment     | *`ForeignKey`* of __`ShiftTime`__ data type          |
  | staff             | Optional, Required staff                    | *`ForeignKey`* of __`Staff`__ data type              |
  | services          | Optional, required service made by customer | *`ManyToManyField`* of __`Service`__ data type       |

#### Transaction
  > Transaction contains infomation such as: ① customer who made this transaction, ② provided services and ③ who provide these services, how the payments was made: how much of the ④ balance deduction and ⑤ non-balance pay, for the non-balance pay, should also specify ⑥ the transaction method (option: cash, credit card, ETM, Alipay, Wechat), ⑦ tax, ⑧ tips and ⑨ transaction date.
  
  | __`Transaction`__  | Usage                                 | DataType                                                                             |
  |--------------------|---------------------------------------|--------------------------------------------------------------------------------------|
  | id                 | Primary key                           | *`AutoField`*                                                                        |
  | create_time        | Datetime                              | *`DateField.auto_now_add`*                                                           |
  | member             | Customer                              | *`ForeignKey`* of __`Member`__ data type                                             |
  | services           | Service provided for this transaction | *`List`* of __`Service`__ data type                                                  |
  | staff              | Staff who take this customer          | *`ForeignKey`* of __`Staff`__ data type                                              |
  | balanace_before    | Balance before this transaction       | *`DecimalField`*                                                                     |
  | balanace_before    | Balance after this transaction        | *`DecimalField`*                                                                     |
  | non_balance_pay    | Amount payed except balance           | *`DecimalField`*                                                                     |
  | recharge           | Amount recharge                       | *`DecimalField`*                                                                     |
  | method             | Transaction method                    | *`CharField`* with choices ["Cash", "Credit card", "ETM", "Alipay", "WeChat"]        |
  | tax                | Amount of tax                         | *`dict`* {"pst": *`DecimalField`*, "gst": *`DecimalField`*}                          |
  | tips               | Amount of tips                        | *`DecimalField`*                                                                     |
  | time               | Datetime of this transaction          | *`DateTimeField`*                                                                    |

#### WorkShift
  > WorkShift model is used to orgnize staff shift priod. It contains start time of the shift, duration of the shift for a staff.
  
  | __`WorkShift`__ | Usage                         | DataType                                |
  |-----------------|-------------------------------|-----------------------------------------|
  | id              | Primary key                   | *`AutoField`*                           |
  | staff           | Staff of this work shift      | *`ForeignKey`* of __`Staff`__ data type |
  | start_time      | start time of this work shift | *`DateTimeField`*                       |
  | end_time        | end time of this work shift   | *`DateTimeField`*                       |
  | duration        | duration of this work shift   | end_time - start_time                   |
  
