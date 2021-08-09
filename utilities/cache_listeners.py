def user_changed(sender, instance, **kwargs):
    # import inside function to avoid cyclic dependency
    from accounts.services import UserService

    UserService.invalidate_user(instance.id)


def customer_changed(sender, instance, **kwargs):
    # import inside function to avoid cyclic dependency
    from customers.services import CustomerService

    CustomerService.invalidate_customer(instance.user_id)