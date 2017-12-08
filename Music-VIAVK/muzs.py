# -*- coding: utf-8 -*-

import tkinter
from tkinter import messagebox
from collections import OrderedDict
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication,QMenu,QSystemTrayIcon,QAction
from subprocess import Popen, PIPE
from chromote import Chromote
import telebot, psutil,sys,time,os, types,requests,json
from bs4 import BeautifulSoup

App_name='Vk-Music-Tg'

tok=''
white_list=[]
chrome_path='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
icon_link='https://raw.githubusercontent.com/Sergeydigl3/telegram-vk-music/master/music.png'
cache_path=QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.ConfigLocation)
if cache_path.endswith('/python'):cache_path=cache_path[:len(cache_path)-7]
cache_path=cache_path+os.path.sep+App_name
if not os.path.isdir(cache_path): os.mkdir(cache_path)

if not os.path.isfile(cache_path+os.path.sep+'config.ini'):
    root = tkinter.Tk()
    root.withdraw()
    result=messagebox.showerror("Error", 'Config file not found. You can make this with "Config Generator"')
    sys.exit()
else:
    try:
        data=json.loads(open(cache_path+os.path.sep+'config.ini', 'r').read())
        tok=data['Token']
        white_list=data['ids']
        chrome_path=data['ch_path']
    except:
        root = tkinter.Tk()
        root.withdraw()
        result = messagebox.showerror("Error", 'Problem with Config file. Try to delete it and recreate it')
        sys.exit()


if os.path.isdir(cache_path) and not os.path.isfile(cache_path+os.path.sep+'muz-trey.png'):
    with open(cache_path+os.path.sep+'muz-trey.png', "wb") as code:
        code.write(requests.get(icon_link).content)
bot=telebot.TeleBot(token=tok)

def chrome_cheker():
    for i in psutil.process_iter():
        if i.name() == "chrome.exe":
            return False
    return True

def checker(m):
    if m.chat.id in white_list: return False
    else: return True

def do_somt(func, m):
    try:
        ch = Chromote()
        for i in ch.tabs:
            if i.url.startswith('https://vk.com/'):
                if func=='play':
                    soup = BeautifulSoup(str(i.html), 'lxml')
                    soup=soup.find(class_='head_nav_item_player')
                    soup=soup.find(id="top_audio_player")
                    if len(soup.get('class'))==2:
                        i.evaluate('getAudioPlayer().play()')
                        send(m, 'Музыка играет')
                    else:
                        i.evaluate('getAudioPlayer().pause()')
                        send(m, 'Музыка приостановлена')
                else:
                    i.evaluate(func)
                return True
        return False
    except BaseException as e: print(str(e))

def do_somth(func, m=white_list[0]):
    temp=do_somt(func, m)
    if not temp: send(m,'Вкладка https://vk.com/... не найдена')
def send(m, t):
    try:
        bot.send_message(m, t)
    except:pass

@bot.message_handler(commands=['start'])
def hi(m):
    send(m.chat.id, 'Привет, если ты не Сергей - уходи!')
@bot.message_handler(commands=['ping'])
def ping(m):
    send(m.chat.id, 'Pong!')
@bot.message_handler(func=lambda m: checker(m))
def check(m):
    send(m.chat.id,'Ты не Сергей...')
@bot.message_handler(commands=['play'])
def pause(m):
    do_somth("play", m.chat.id)
@bot.message_handler(commands=['next'])
def next(m):
    do_somth('getAudioPlayer().playNext()')
    send(m.chat.id, 'Включён следующий трек')
@bot.message_handler(commands=['prev'])
def prev(m):
    do_somth('getAudioPlayer().playPrev()')
    send(m.chat.id, 'Включён преведующий трек')
@bot.message_handler(commands=['off'])
def off(m):
    send(m.chat.id, 'Если вы хотите выключить бота напишите /destroy')
@bot.message_handler(commands=['pcoff'])
def bot_off(m):
    send(m.chat.id, 'Если вы хотите выключить компьютер напишите /poweroff')
@bot.message_handler(commands=['destroy'])
def destroy(m):
    QApplication.quit()
@bot.message_handler(commands=['poweroff'])
def poweroff(m):
    bot.send_message(m.chat.id, 'Отключаюсь')
    os.system('poweroff')

@bot.message_handler(content_types=['text'])
def other_text(m):
    if m.text.isdigit() and int(m.text)>=0 and int(m.text)<=100:
        vol=int(m.text)/100
        func='getAudioPlayer().setVolume({})'.format(str(vol))
        do_somth(func)
        send(m.chat.id, 'Громкость установлена на '+str(int(vol*100))+'%')
    else: send(m.chat.id, 'Я тебя не понимаю')

class ProgramTray(QtCore.QThread):
    def __init__(self, icon):
        QtCore.QThread.__init__(self)
        self.menu = QMenu()
        self.icon = QSystemTrayIcon(QtGui.QIcon(icon))
        self.flag_exit = True
        self.first=True

    def run(self):
        if chrome_cheker():
            p1 = Popen('"{}" --remote-debugging-port=9222 & exit'.format(chrome_path), shell=True, stdout=PIPE)
            time.sleep(2)
            p1.kill()
            try:
                bot.delete_webhook()
                bot.polling(none_stop=True)
            except:
                bot.send_message(white_list[0], 'Программа выключенна. Сбой')
        else:
            if self.first:
                self.first = False
                bot.send_message(white_list[0], 'Полностью закройте Chrome и запустите программу')
        print('Кажется я умираю')
        QApplication.quit()

    def stop(self):
        QApplication.quit()

    def setMenu(self, menu=None):
        if not menu:
            menu = []
        collection = OrderedDict(menu)
        items = collection.keys()
        functions = collection.values()

        for i, item in enumerate(items):
            function = functions[i]

            if isinstance(function, types.MethodType) \
                or isinstance(function, types.FunctionType):
                self.menu.addAction(QAction(item, self,
                                    triggered=function))

        self.quitAction = QAction("Exit", self, triggered=self.stop)
        self.menu.addAction(self.quitAction)

        self.icon.setContextMenu(self.menu)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    program = ProgramTray(cache_path+os.path.sep+'muz-trey.png')
    program.setMenu()
    program.icon.show()
    program.start()
    print(app.exec_())