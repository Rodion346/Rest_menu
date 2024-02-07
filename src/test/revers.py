def reverse_operation(route_name: str, **kwargs) -> str:
    routes = {
        'read_menus': '/api/v1/menus',
        'create_menu': '/api/v1/menus',
        'read_menu': f'/api/v1/menus/{kwargs.get('menu_id', '')}',
        'update_menu': f'/api/v1/menus/{kwargs.get('menu_id', '')}',
        'delete_menu': f'/api/v1/menus/{kwargs.get('menu_id', '')}',
        'read_submenus': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus',
        'create_submenu': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus',
        'read_submenu': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/{kwargs.get('submenu_id', '')}',
        'update_submenu': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/{kwargs.get('submenu_id', '')}',
        'delete_submenu': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/{kwargs.get('submenu_id', '')}',
        'read_dishes': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/{kwargs.get('submenu_id', '')}/dishes',
        'create_dish': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/{kwargs.get('submenu_id', '')}/dishes',
        'read_dish': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/'
        f'{kwargs.get('submenu_id', '')}/dishes/{kwargs.get('dish_id', '')}',
        'update_dish': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/'
        f'{kwargs.get('submenu_id', '')}/dishes/{kwargs.get('dish_id', '')}',
        'delete_dish': f'/api/v1/menus/{kwargs.get('menu_id', '')}/submenus/'
        f'{kwargs.get('submenu_id', '')}/dishes/{kwargs.get('dish_id', '')}',
    }

    return str(routes.get(route_name))
