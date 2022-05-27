import time
import vk_api

from config import token
from friendlist_deep_1 import friendlist

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

delay_sec = 10

count_api_asks = 0

array_elements_count = len(friendlist['items'])
while array_elements_count > 0:
    count_api_asks += 1
    print('API ASKS: ' + str(count_api_asks) + ' | ' + str(array_elements_count) + ' | LOOKING USER ID: ' + str(
        friendlist['items'][array_elements_count - 1]) + '\n')
    try:
        userinfo = vk.users.get(fields='blacklisted', user_id=friendlist['items'][array_elements_count - 1])[0][
            'blacklisted']
        if userinfo == 1:
            print('BLACKLISTER DETECTED! ID: ' + str(friendlist['items'][array_elements_count - 1]) + ' LOG UPDATED \n')

            f = open('vk_find_blacklisters.log', 'a')
            f.write('BLACKLISTER DETECTED! ID: ' + str(friendlist['items'][array_elements_count - 1]) + '\n')
            f.close()

    except Exception as e:
        print(str(e) + '\n')

    time.sleep(delay_sec)
    array_elements_count -= 1
