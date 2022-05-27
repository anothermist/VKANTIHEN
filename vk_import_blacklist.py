import time
import vk_api

from config import token
from blacklist import blacklist

# group_id = 0
group_id = 205750647
# group_id = 210486377

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

blacklist_items = blacklist['items']

i = 0
while i < blacklist['count']:
    print('BLOCKING: ' + str(i + 1) + ' ' + str(blacklist_items[i]))
    try:
        if group_id > 0:
            vk.groups.ban(group_id=group_id, owner_id=blacklist_items[i])
            print('USER BANNED! \n')
        else:
            vk.account.ban(owner_id=blacklist_items[i])
            print('USER BANNED! \n')
    except Exception as e:
        print(str(e) + '\n')

    time.sleep(2)
    i += 1

print('BLACKLIST IS IMPORTED !')
