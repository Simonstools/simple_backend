import logging

def delete_item(id: int, lst: list):
    for idx, item in enumerate(lst):
        if item['id'] == id:
            del lst[idx]

def update_item(id: int, data: dict, lst: list):
    for idx, item in enumerate(lst):
        if item['id'] == id:
            lst[idx] = data

def check_route(route: str) -> str:
    result = [word for word in route.split('/') if word != '']
    result.insert(0, '')
    handled_route = '/'.join(result)
    if route != handled_route:
        logging.warning(f"Route has been modified from {route} to {handled_route}")
    return handled_route
