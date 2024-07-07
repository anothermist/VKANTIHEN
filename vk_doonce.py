import time
import vk_api

from config import token
from blacklist import blacklist

# group_id = 0
group_id = 205750647
# group_id = 210486377

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


try:
    if group_id > 0:
        vk.groups.ban(group_id=group_id, owner_id=54248567)
        print('USER BANNED! \n')
    else:
        vk.account.ban(owner_id=54248567)
        print('USER BANNED! \n')
except Exception as e:
    print(str(e) + '\n')



print('BLACKLIST IS IMPORTED !')
