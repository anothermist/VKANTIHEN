import time
import vk_api

from config import token

group_id = 0
# group_id = 205750647

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


if group_id > 0:
    blacklist = vk.groups.getBanned(group_id=group_id, count='200')
else:
    blacklist = vk.account.getBanned(count='200')

blacklist_count = blacklist['count']
blacklist_items = blacklist['items']

if int(blacklist_count) > 200:
    iterations = int(blacklist_count) / 10
    if int(blacklist_count) % 200 != 0:
        iterations += 1
    i = 1
    while i < iterations:
        time.sleep(1)
        if group_id == 0:
            buff = vk.account.getBanned(count='200', offset=(200 * i))
            blacklist_items = blacklist_items + buff['items']
        i += 1
buff = []
if group_id > 0:
    i = blacklist_count
    while i > 0:
        buff.append(blacklist['items'][i - 1]['profile']['id'])
        i -= 1
    blacklist_items = buff

print(str(blacklist_items))

blacklist = 'blacklist = {\'count\': ' + str(blacklist_count) + ', \'items\': ' + str(blacklist_items) + '}'
f = open('blacklist.py', 'w+')
f.seek(0)
f.write(blacklist)
f.close()

print('BLACKLIST IS EXPORTED TO FILE ! ' + str(blacklist_count) + ' IDS')
