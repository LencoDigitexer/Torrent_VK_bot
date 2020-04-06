import vk_api
import random
import urllib.request, json 
import wget
import os
from vk_api.bot_longpoll import VkBotLongPoll
import qbittorrentapi
from config import *


class Server:

            def __init__(self, api_token, group_id, server_name: str="Empty"):
                print("Инициализация вк")
                self.server_name = server_name
                self.vk = vk_api.VkApi(token=api_token)
                self.upload = vk_api.VkUpload(self.vk)
                self.long_poll = VkBotLongPoll(self.vk, group_id)
                self.vk_api = self.vk.get_api()
                print("Готово")
                print("Инициализация торрента")
                self.qbt_client = qbittorrentapi.Client(host=url_web_api_torrent, username=torrent_login_api, password=torrent_password_api)
                try:
                    self.qbt_client.auth_log_in()
                except qbittorrentapi.LoginFailed as e:
                    print(e)
                print("Готово")
            def send_img(self, send_id, attachments, text):

                self.vk_api.messages.send(peer_id=send_id,
                                          message=text,
                                          attachment = attachments,
                                          random_id=123456 + random.randint(1,27))

            def send_msg(self, send_id, message):

                self.vk_api.messages.send(peer_id=send_id,
                                          message=message,
                                          random_id=123456 + random.randint(1,27))
                                          
            def start(self):
                for event in self.long_poll.listen():
                    if event.object.message is not None: # исключение инфы о начале написания

                        print(event.object.message["text"].lower())
                        user_id = event.object.message["from_id"]

                        # проверка папки пользователя
                        lst = os.listdir(path="./users")
                        if (str(user_id) in lst) == False:
                            self.send_msg( user_id , "У тебя нет папки - создаем" )
                            path = os.path.dirname(os.path.abspath(__file__)) + "/users/" + str(user_id)
                            os.mkdir(path)
                        ###############################

                        #проверка состояния торрентов
                        if event.object.message["text"].lower() == "загрузки".lower():
                            send_text = "Скачанные торренты\n\n"
                            torrent_list = self.qbt_client.torrents.info()

                            for i in range(0, len(torrent_list)):
                                if torrent_list[i]["save_path"] == savepath_torrent_file + "\\" + str(user_id) + "\\":
                                    send_text = send_text + str(i+1) + ' "' + torrent_list[i]["name"] + '" ====> ' + torrent_list[i]["state"] + '\n'

                            self.send_msg( user_id, send_text)
                        #####

                        '''
                        # напоминалка
                        if not event.object.message["attachments"]:
                            self.send_msg( event.object.message["from_id"], "Пожалуйста, отправь мне torrent - файл для загрузки")
                        #####'''
                        
                        # сохранение торрентов в папку 
                        if event.object.message["attachments"]:
                            download_url = event.object.message["attachments"][0]["doc"]["url"]
                            self.send_msg( user_id, "Ваш торрент добавлен в очередь" )
                            wget.download(download_url, "torrent_user\\" + str(user_id) + ".torrent")
                        # добавляем закачку
                            self.qbt_client.torrents_add(torrent_files="torrent_user\\" + str(user_id) + ".torrent", savepath=savepath_torrent_file + "\\" + str(user_id))
                        #####
                        else:
                            lst = event.object.message["text"].split()
                            print(lst)
                            print(len(lst))
                            if len(lst)==2:
                                if lst[0].lower() == 'скачать'.lower():
                                    self.send_msg(user_id, "Вы скачиваете " + str(lst[1]))


'''             

                        wget.download(download_url, "users\\" + str(user_id) + ".torrent")
                        if event.object.message["text"].lower == "как дела":
                            self.send_msg( str(event.object.message["from_id"]), "всё хорошо" )'''
                    



if __name__ ==  "__main__":
    server1 = Server("7d4011c118beec2a124712ed3c53609f3bc940c3eb9154b0356f2f21eafb414ff365eada4cd404550becd", 182306529, "server1")
    server1.start() 
