import datetime
import time
import vk_api

from config import token
from friendlist import friendlist

delay_sec = 55
auto_accept = 2  # 0 = ask, 1 = keep as followers,		2 = add to friendlist
auto_delete = 2  # 0 = ask, 1 = del me from followers, 	2 = ban unfriendler

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

while True:
    try:
        vk_status_was = vk.status.get()
        print(str(vk_status_was['text']))
        f = open('vk_antihen.log', 'a')
        f.write(str(vk_status_was['text']) + '\n')
        f.close()

        friends_now = vk.friends.get()
        friends_was = friendlist

        if friends_now != friends_was:
            print('IN FRIENDLIST WAS: ' + str(friends_was['count']))
            f = open('vk_antihen.log', 'a')
            f.write('IN FRIENDLIST WAS: ' + str(friends_was['count']) + '\n')
            f.close()
            print('IN FRIENDLIST NOW: ' + str(friends_now['count']))
            f = open('vk_antihen.log', 'a')
            f.write('IN FRIENDLIST NOW: ' + str(friends_now['count']) + '\n')
            f.close()

        if int(friends_was['count']) < int(friends_now['count']):
            f = open('friendlist.py', 'w')
            f.write('friendlist = ' + str(friends_now))
            f.close()

            f = open('vk_antihen.log', 'a')
            f.write('\n' + 'FRIENDLIST DATABASE UPDATED !!!' + '\n')
            f.close()
            print('FRIENDLIST DATABASE UPDATED !!!')
            exit()

        else:
            if int(friends_was['count']) > int(friends_now['count']):

                count = 0
                while count < friends_was['count']:
                    if friends_was['items'][count] != friends_now['items'][count]:
                        userinfo = vk.users.get(fields='blacklisted', user_id=friends_was['items'][count])[0]
                        print('LEFT ME: ' + str(userinfo['id']) + ' | Closed: ' + str(
                            userinfo['is_closed']) + ' | Access: ' + str(userinfo['can_access_closed']) + ' | ' + str(
                            userinfo['first_name']) + ' ' + str(userinfo['last_name']))
                        f = open('vk_antihen.log', 'a')
                        f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                        f.write('LEFT ME: ' + str(userinfo['id']) + ' | Closed: ' + str(
                            userinfo['is_closed']) + ' | Access: ' + str(userinfo['can_access_closed']) + ' | ' + str(
                            userinfo['first_name']) + ' ' + str(userinfo['last_name']) + '\n')
                        f.close()

                        friend_protection = int(
                            vk.users.get(fields='is_friend', user_id=friends_was['items'][count])[0]['is_friend'])

                        if friend_protection == 1:
                            print('ERROR: PROTECTION PREVENT TO DELETION A FRIENDS!!!')
                            f = open('vk_antihen.log', 'a')
                            f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                            f.write('ERROR: PROTECTION PREVENT TO DELETION A FRIENDS!!! ' + '\n')
                            f.close()

                        else:
                            how_to_del = 0

                            if auto_delete == 0:
                                how_to_del = int(input('0 = DON\'T UNFOLLOW, 1 = UNFOLLOW, 2 = ADD TO BLACKLIST '))

                            if auto_delete == 1 or how_to_del == 1:
                                vk.friends.delete(user_id=friends_was['items'][count])
                                print('REMOVED: ' + str(userinfo['id']) + ' | Closed: ' + str(
                                    userinfo['is_closed']) + ' | Access: ' + str(
                                    userinfo['can_access_closed']) + ' | ' + str(userinfo['first_name']) + ' ' + str(
                                    userinfo['last_name']))
                                f = open('vk_antihen_removed.log', 'a')
                                f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                                f.write('REMOVED: ' + str(userinfo['id']) + ' | Closed: ' + str(
                                    userinfo['is_closed']) + ' | Access: ' + str(
                                    userinfo['can_access_closed']) + ' | ' + str(userinfo['first_name']) + ' ' + str(
                                    userinfo['last_name']) + '\n\n')
                                f.close()

                            if auto_delete == 2 or how_to_del == 2:
                                vk.account.ban(owner_id=friends_was['items'][count])
                                print('BLOCKED: ' + str(userinfo['id']) + ' | Closed: ' + str(
                                    userinfo['is_closed']) + ' | Access: ' + str(
                                    userinfo['can_access_closed']) + ' | ' + str(userinfo['first_name']) + ' ' + str(
                                    userinfo['last_name']))
                                f = open('vk_antihen_blocked.log', 'a')
                                f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                                f.write('BLOCKED: ' + str(userinfo['id']) + ' | Closed: ' + str(
                                    userinfo['is_closed']) + ' | Access: ' + str(
                                    userinfo['can_access_closed']) + ' | ' + str(userinfo['first_name']) + ' ' + str(
                                    userinfo['last_name']) + '\n\n')
                                f.close()

                            if count == 0:
                                deletefromDB = str(str(friends_was['items'][count]))
                            else:
                                deletefromDB = str(', ' + str(friends_was['items'][count]))

                            f = open('friendlist.py', 'w')
                            items = str(friends_was['items'])
                            friendlist_newest = items.replace(deletefromDB, '')
                            f.write('friendlist = {\'count\': ' + str(
                                friends_was['count'] - 1) + ', \'items\': ' + friendlist_newest + '}')
                            f.close()

                            exit()

                    count += 1

        followers = vk.friends.getRequests()

        if int(followers['count']) > 0:
            print('NEW REQUEST: ' + str(followers))
            follower_user_data = vk.users.get(user_id=followers['items'])[-1]
            print(str(follower_user_data['id']) + ' | Closed: ' + str(
                follower_user_data['is_closed']) + ' | Access: ' + str(
                follower_user_data['can_access_closed']) + ' | ' + str(follower_user_data['first_name']) + ' ' + str(
                follower_user_data['last_name']))

            f = open('vk_antihen.log', 'a')
            f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
            f.write('NEW REQUEST: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                follower_user_data['is_closed']) + ' | Access: ' + str(
                follower_user_data['can_access_closed']) + ' | ' + str(follower_user_data['first_name']) + ' ' + str(
                follower_user_data['last_name']) + '\n')
            f.close()

            how_to_add = 0

            if auto_accept == 0:
                how_to_add = int(input('1 = KEEP AS FOLLOWER, 2 = ADD TO FRIENDLIST '))

            if auto_accept == 1 or how_to_add == 1:
                vk.friends.delete(user_id=followers['items'])
                print('REQUEST DELETED: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                    follower_user_data['is_closed']) + ' | Access: ' + str(
                    follower_user_data['can_access_closed']) + ' | ' + str(
                    follower_user_data['first_name']) + ' ' + str(follower_user_data['last_name']) + '\n')

                f = open('vk_antihen.log', 'a')
                f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                f.write('REQUEST DELETED: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                    follower_user_data['is_closed']) + ' | Access: ' + str(
                    follower_user_data['can_access_closed']) + ' | ' + str(
                    follower_user_data['first_name']) + ' ' + str(follower_user_data['last_name']) + '\n')
                f.close()

                f = open('vk_antihen_ignored.log', 'a')
                f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                f.write('REQUEST DELETED: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                    follower_user_data['is_closed']) + ' | Access: ' + str(
                    follower_user_data['can_access_closed']) + ' | ' + str(
                    follower_user_data['first_name']) + ' ' + str(follower_user_data['last_name']) + '\n')
                f.close()

            if auto_accept == 2 or how_to_add == 2:
                vk.friends.add(user_id=followers['items'])
                print('ADDED TO FRIENDLIST: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                    follower_user_data['is_closed']) + ' | Access: ' + str(
                    follower_user_data['can_access_closed']) + ' | ' + str(
                    follower_user_data['first_name']) + ' ' + str(follower_user_data['last_name']) + '\n')

                f = open('vk_antihen.log', 'a')
                f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                f.write('ADDED TO FRIENDLIST: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                    follower_user_data['is_closed']) + ' | Access: ' + str(
                    follower_user_data['can_access_closed']) + ' | ' + str(
                    follower_user_data['first_name']) + ' ' + str(follower_user_data['last_name']) + '\n\n')
                f.close()

                f = open('vk_antihen_added.log', 'a')
                f.write('\n' + str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + '\n')
                f.write('ADDED TO FRIENDLIST: ' + 'ID: ' + str(follower_user_data['id']) + ' | Closed: ' + str(
                    follower_user_data['is_closed']) + ' | Access: ' + str(
                    follower_user_data['can_access_closed']) + ' | ' + str(
                    follower_user_data['first_name']) + ' ' + str(follower_user_data['last_name']) + '\n\n')
                f.close()

                exit()

        vk.status.set(text=str(datetime.datetime.now().strftime('%d.%m.%y - %H:%M:%S')) + ' | add=' + str(auto_accept) + ', del=' + str(auto_delete) + ' | ' + str(friends_now['count']))

        time.sleep(delay_sec)
    except Exception as e:
        print(str(e))
        time.sleep(delay_sec)
        exit()
