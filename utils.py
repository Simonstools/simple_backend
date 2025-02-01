def delete_item(id: int, lst: list):
    for idx, item in enumerate(lst):
        if item['id'] == id:
            del lst[idx]

def update_item(id: int, data: dict, lst: list):
    for idx, item in enumerate(lst):
        if item['id'] == id:
            lst[idx] = data
