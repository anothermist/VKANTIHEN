import time
import vk_api

from config import token
# from friendlist_deep_1 import friendlist

delay_sec = 10
deep_level = 0

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

friendlist = vk.friends.get()

count_api_asks = 1

f = open('friendlist.py', 'w')
f.write('friendlist = ' + str(friendlist))
f.close()
print(
    'DEEP LEVEL: 0' + ' EXTRACTED: ' + str(len(friendlist['items'])) + ' IDS IS EXPORTED TO FILE ! \n')


def delete_duplicates(list_with_duplicates):
    new_list = []
    for element in list_with_duplicates:
        if not element in new_list:
            new_list.append(element)
    return new_list


items_get = []
extracted_ids = []

while deep_level > 0:

    array_elements_count = len(friendlist['items'])
    while array_elements_count > 0:
        count_api_asks += 1
        print(str(array_elements_count) + ' EXTRACTING FRIENDLIST FROM: ' + str(friendlist['items'][array_elements_count - 1]))
        try:
            items_get = (vk.friends.get(user_id=friendlist['items'][array_elements_count - 1]))['items']
        except Exception as e:
            print(str(e) + '\n')
        extracted_ids = extracted_ids + items_get
        print('API ASKS: ' + str(count_api_asks) + ' | EXTRACTED WITH DUPLICATES: ' + str(len(extracted_ids)) + ' | USER\'S FRIENDLIST: ' + str(
            len(items_get)) + '\n')
        time.sleep(delay_sec)
        array_elements_count -= 1

    print('DELETING DUPLICATES IN PROGRESS, PLEASE WAIT SOME TIME!')
    extracted_ids = delete_duplicates(extracted_ids)
    friendlist = str('friendlist = {\'count\': ' + str(len(extracted_ids)) + ', \'items\': ' + str(extracted_ids) + '}')
    filename = 'friendlist_deep_' + str(deep_level) + '.py'
    f = open(filename, 'w')
    f.write('friendlist = {\'count\': ' + str(len(extracted_ids)) + ', \'items\': ' + str(extracted_ids) + '}')
    f.close()

    print('DEEP LEVEL: ' + str(deep_level) + ' EXTRACTED: ' + str(len(extracted_ids)) + ' IDS IS EXPORTED TO FILE !')
    deep_level -= 1
