import datetime
import time
import sys
import vk_api

from config import token

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

# i = 30283
# while i > 0:
#     try:
#         vk.wall.delete(post_id=i)
#         i -= 1
#         print(str(i))
#     except Exception as e:
#         print(str(e))
#     time.sleep(2)

auto_accept = 2  # 0 = ask, 1 = keep as followers,		2 = add to friendlist
auto_delete = 2  # 0 = ask, 1 = del me from followers, 	2 = ban unfriendler

friends_now = vk.friends.get()

vk.status.set(text=str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + ' | add=' + str(auto_accept) + ', del=' + str(auto_delete) + ' | ' + str(friends_now['count']))
