# Endpoints
ID = 1
PREFIX = '/api/v1/'
ENDPOINT_MENU = f'{PREFIX}menus'
ENDPOINT_FULL_LIST = f'{ENDPOINT_MENU}-full-list'
ENDPOINT_SUBMENU = f'{ENDPOINT_MENU}/{ID}/submenus'
ENDPOINT_DISH = f'{ENDPOINT_SUBMENU}/{ID}/dishes'

# Messages
MENU_NOT_FOUND_MSG = 'menu not found'
MENU_ALREADY_EXISTS_MSG = 'Меню с таким заголовком уже существует.'
MENU_MSG_PACK = (MENU_ALREADY_EXISTS_MSG, MENU_NOT_FOUND_MSG)

SUBMENU_NOT_FOUND_MSG = 'submenu not found'
SUBMENU_ALREADY_EXISTS_MSG = 'Подменю с таким заголовком уже существует.'
SUBMENU_MSG_PACK = (SUBMENU_ALREADY_EXISTS_MSG, SUBMENU_NOT_FOUND_MSG)

DISH_NOT_FOUND_MSG = 'dish not found'
DISH_ALREADY_EXISTS_MSG = 'Блюдо с таким заголовком уже существует.'
DISH_MSG_PACK = (DISH_ALREADY_EXISTS_MSG, DISH_NOT_FOUND_MSG)

# MENU Data
MENU_POST_PAYLOAD = {'title': 'My menu 1',
                     'description': 'My menu description 1'}
MENU_PATCH_PAYLOAD = {'title': 'My updated menu 1',
                      'description': 'My updated menu description 1'}
CREATED_MENU = {'id': '1',
                'title': 'My menu 1',
                'description': 'My menu description 1',
                'submenus_count': 0,
                'dishes_count': 0}
EXPECTED_MENU = {'id': '1',
                 'title': 'My menu 1',
                 'description': 'My menu description 1',
                 'submenus_count': 1,
                 'dishes_count': 1}
UPDATED_MENU = {'id': '1',
                'title': 'My updated menu 1',
                'description': 'My updated menu description 1',
                'submenus_count': 1,
                'dishes_count': 1}
DELETED_MENU = {'status': True, 'message': 'The menu has been deleted'}

# SUBMENU Data
SUBMENU_POST_PAYLOAD = {'title': 'My submenu 1',
                        'description': 'My submenu description 1'}
SUBMENU_PATCH_PAYLOAD = {'title': 'My updated submenu 1',
                         'description': 'My updated submenu description 1'}
CREATED_SUBMENU = {'id': '1',
                   'title': 'My submenu 1',
                   'description': 'My submenu description 1',
                   'dishes_count': 0}
EXPECTED_SUBMENU = {'id': '1',
                    'title': 'My submenu 1',
                    'description': 'My submenu description 1',
                    'dishes_count': 1}
UPDATED_SUBMENU = {'id': '1',
                   'title': 'My updated submenu 1',
                   'description': 'My updated submenu description 1',
                   'dishes_count': 1}
DELETED_SUBMENU = {'status': True, 'message': 'The submenu has been deleted'}

# DISH Data
DISH_POST_PAYLOAD = {'title': 'My dish 1',
                     'description': 'My dish description 1',
                     'price': '12.50'}
DISH_PATCH_PAYLOAD = {'title': 'My updated dish 1',
                      'description': 'My updated dish description 1',
                      'price': '14.5'}
CREATED_DISH = {'id': '1',
                'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '12.5'}
UPDATED_DISH = {'id': '1',
                'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '14.5'}
DELETED_DISH = {'status': True, 'message': 'The dish has been deleted'}

EXPECTED_FULL_LIST = [
    {'title': 'My menu 1', 'id': 1, 'description': 'My menu description 1',
     'submenus': [
         {'menu_id': 1, 'description': 'My submenu description 1', 'title': 'My submenu 1', 'id': 1,
          'dishes': [
              {'price': 12.5, 'title': 'My dish 1', 'submenu_id': 1, 'id': 1, 'description': 'My dish description 1'}]}]}]

EXPECTED_MENU_FILE_CONTENT = [{'title': 'Меню', 'description': 'Основное меню', 'submenus': [{'title': 'Холодные закуски', 'description': 'К пиву', 'dishes': [{'title': 'Сельдь Бисмарк', 'description': 'Традиционное немецкое блюдо из маринованной сельди', 'price': 182.99}, {'title': 'Мясная тарелка', 'description': 'Нарезка из ветчины, колбасных колечек, нескольких сортов сыра и фруктов', 'price': 215.36}, {'title': 'Рыбная тарелка', 'description': 'Нарезка из креветок, кальмаров, раковых шеек, гребешков, лосося, скумбрии и красной икры', 'price': 265.57}]}, {'title': 'Рамен', 'description': 'Горячий рамен', 'dishes': [{'title': 'Дайзу рамен', 'description': 'Рамен на курином бульоне с куриными подушками и яйцом аджитама, яично-пшеничной лапшой, ростки зелени, грибами муэр и зеленым луком', 'price': 166.47}, {'title': 'Унаги рамен', 'description': 'Рамен на нежном сливочном рыбном бульоне, с добавлением маринованного угря, грибов муэр, кунжута, зеленого лука', 'price': 168.25}, {'title': 'Чиизу Рамен', 'description': 'Рамен на насыщенном сырном бульоне на основе кокосового молока, с добавлением куриной грудинки, яично - пшеничной лапши, мисо-матадоре, ростков зелени, листьев вакамэ',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  'price': 132.88}]}]}, {'title': 'Алкогольное меню', 'description': 'Алкогольные напитки', 'submenus': [{'title': 'Красные вина', 'description': 'Для романтичного вечера', 'dishes': [{'title': 'Шемен де Пап ля Ноблесс', 'description': 'Вино красное — фруктовое, среднетелое, выдержанное в дубе', 'price': 2700.79}, {'title': 'Рипароссо Монтепульчано', 'description': 'Вино красное, сухое', 'price': 3100.33}, {'title': 'Кьянти, Серристори', 'description': 'Вино красное — элегантное, комплексное, не выдержанное в дубе', 'price': 1850.42}]}, {'title': 'Виски', 'description': 'Для интересных бесед', 'dishes': [{'title': 'Джемисон', 'description': 'Классический купажированный виски, проходящий 4-хлетнюю выдержку в дубовых бочках', 'price': 420.78}, {'title': 'Джек Дэниелс', 'description': 'Характерен мягкий вкус, сочетает в себе карамельно-ванильные и древесные нотки. Легкий привкус дыма.', 'price': 440.11}, {'title': 'Чивас Ригал', 'description': 'Это купаж высококачественных солодовых и зерновых виски, выдержанных как минимум в течение 12 лет, что придает напитку роскошные нотки меда, ванили и спелых яблок.', 'price': 520.08}]}]}]
