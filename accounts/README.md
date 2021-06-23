### Account Documentation
User Django pre-defined `auth.user` module to manage all account register login logout action.
We will create another `UserProfile` app to manage user profile data later.
---

#### Data models attributes:
- *primary_key*
- *username*
- *password*
- *email*
```
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
```
---
#### APIs json:
- Signup Api
- Login Api
- Logout APi
