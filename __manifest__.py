{
    'name': 'Inventory Management',
    'version': '1.0',
    'summary': 'Manage inventory items, locations, and movements',
    'category': 'Inventory Customize',
    'author': 'hieu',
    'depends': ['base'],
    'data': [

        'security/inventory_management_groups.xml',
        'security/ir.model.access.csv',
        'security/inventory_management_security.xml',

        'data/inventory_management_data.xml',

        'views/inventory_item_views.xml',
        'views/inventory_location_views.xml',
        'views/inventory_movement_views.xml',

        'views/inventory_management_menus.xml',
        # 'views/inventory_item_template.xml',
        # 'views/inventory_location_template.xml',
        # 'views/inventory_movement_template.xml',

    ],
}
