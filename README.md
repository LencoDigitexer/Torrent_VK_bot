# Torrent_VK_bot

:negative_squared_cross_mark: Этот проект умер за ненадобностью<br>
Решение - не париться и настроить vpn для торрента <br>
:black_square_button: делать или не делать, вот в чем вопрос?   

Сервис скачивания торрентов через браузер на основе vk_api

Как работает?
1. Написать группе https://vk.com/club182306529
2. Напишет, что создает папку. Она создается в папке users
3. Команда "загрузки" отобразит торренты через api
4. Постоянно требует отправить torrent - файл (отправьте ему этот файл для загрузки)
5. Этот файл скачается в torrent_user

Как настроить?
1. скачать qbittorrent
2. "Загрузки должны выглядеть так"  (копировать торрент файлы в torrent_user)

<p align="center">
  <img src="img/1.png"/>
</p>

3. Веб-интерфейс должен быть таким (в файле конфигурации config.py можно поменять настройки под свои пароль adminadmin)

<p align="center">
  <img src="img/2.png"/>
</p>

4. В файле конфига укажите полный путь до папки users в этом репозитории
5. Нужен пайтов и установленные зависимости
> Запускаем:

    $ pip install -r requirements.txt

6. Пишем команды боту

## Дальнейшее техническое задание

Суть: в настройках торрента можно запустить программу по завершению закачки. <br>
Написать дополнительный py скрипт для получения ключей из программы-клиента и манипулировать ими.

<br>

Как: В настройках "загрузки" клиента указать настройку запуска внешней программы

<p align="center">
  <img src="img/3.png"/>
</p>

Программа будет принимать ключи торрента и принимать их как аргументы (см. https://jenyay.net/Programming/Argparse )

Далее она должна создать zip-архив и залить на send.firefox.com (см. https://github.com/timvisee/ffsend ) и как то получить ссылку из консоли (см. https://python-scripts.com/subprocess ). пример реализации выхвата текста из командной строки ( https://github.com/LencoDigitexer/RAPy/blob/1110a52b35ebb452474798c6ce2ca7bd3f2b8f12/adobe.py#L229 )

<br>

В идеале, программа должна оповестить пользователя об окончании загрузки, но это нужно сделать функцию добавления меток в vk_bot.py на 80 строке. Тогда будет легче брать id пользователя вк для отправки функцией self.send_msg() (35 строка vk_bot.py) и по окончании загрузки на vshare отправлять ссылку на скачивание. Но можно пока сделать сохранение в txt. Потом разберусь в этой вакханалии. Главное, чтобы был скелет, с чем работать.
