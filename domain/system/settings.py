defaultUser = {
    'username': 'olamide',
    'firstname': 'Olamide',
    'middlename': '',
    'lastname': 'Okunola',
    'password': 'allow',
    'phonenumber': '08023719137',
    'email': 'olamide@favychos.com',
    'authorizations': [
        {
                "description": "User Authorizations",
                "model": "User",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "authorization_auth",
                "model": "Authorization",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "customer_auth",
                "model": "Customer",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "group_auth",
                "model": "Group",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "price_auth",
                "model": "Price",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "product_auth",
                "model": "Product",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "production_auth",
                "model": "Production",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            },
            {
                "description": "sale_auth",
                "model": "Sale",
                "create": True,
                "edit": True,
                "view": True,
                "delete": True
            }
    ],
    'groups': [
        {
            'description': 'manager_group',
            'details': 'Group of Managers',
            'authorizations': [],
        }
    ]
}