from kivy.lang import Builder
from kivymd.app import MDApp
import os
from tkinter import *
from plyer import filechooser
import pyttsx3
import PyPDF2
import threading
import cv2
import numpy as np
from kivy.clock import Clock
from word2number import w2n
from playsound import playsound
from kivymd.uix.snackbar import Snackbar
import pytesseract as pyt
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
import time
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screen import Screen
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip
Window.size = (350, 600)


Builder.load_string('''

<ItemConfirm>
    IconLeftWidget:
        icon: "microphone" 


<SplashScreen>:
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
    Image:
        source: "images/logo.jpg"
        size_hint: .40, .40
        pos_hint: {"center_x": .5, "center_y": .55}
    MDLabel:
        text: "Virtual Eye"
        pos_hint: {"center_x": .5, "center_y": .2}
        halign: "center"
        theme_text_color: "Custom"
        text_color: 75/255,0/255,130/255,1
        font_size: "35sp"
        font_name: "font/Poppins-SemiBold.ttf"
    MDLabel:
        text: "Vision Assistance"
        pos_hint: {"center_x": .5, "center_y": .15}
        halign: "center"
        theme_text_color: "Custom"
        text_color: 75/255,0/255,130/255,1
        font_size: "13sp"
        font_name: "font/Poppins-Regular.ttf"

   
<VirtualEye>:
    BoxLayout:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation:"vertical"

                        MDTopAppBar:
                            title:"Virtual Eye"
                            elevation: 0
                            font_name: "font/Poppins-SemiBold.ttf"
                            md_bg_color: 75/255,0/255,130/255,1
                            right_action_items: [["microphone-settings", lambda x: root.commands()]]
                        Widget:

                    MDGridLayout:
                        size_hint_y:.85
                        cols:2
                        padding:dp(15)
                        spacing:dp(15)
                        ElementCard:
                            image:"images/text to speech.png"
                            text:"Text To Speech"
                            font_name: "font/Poppins-Regular.ttf"
                            on_press: root.text_to_speech()
                        ElementCard:
                            image:"images/image to audio.png"
                            text:"Image To Audio"
                            font_name: "font/Poppins-Regular.ttf"
                            on_press: root.manager.current='screen_two'
                        ElementCard:
                            image:"images/speech to text.png"
                            text:"Speech To Text"
                            font_name: "font/Poppins-Regular.ttf"
                            on_press: root.speech_to_text()
                        ElementCard:
                            image:"images/pdf to audio.png"
                            text:"PDF To Audio"
                            font_name: "font/Poppins-Regular.ttf"
                            on_press: root.pdf_to_audio_button()
                        Widget:

                    MDLabel:
                        id: pdf_label
                        pos_hint: {'center_x':.5,'center_y':.225}
                        size_hint: .8, .4
                        halign: "center"

                    BoxLayout:
                        Widget:
                        MDFloatingActionButton:
                            icon: "microphone"
                            md_bg_color: 75/255,0/255,130/255,1
                            elevation: 0
                            pos_hint: {"center_x": .5, "center_y": .1}
                            on_press: root.onclick()
                        Widget:


<Content>:
    orientation:"vertical"
    spacing:"12dp"
    size_hint_y:None
    size_hint_x:.5
    height:"50dp"
    MDTextField:
        id: pgno
        hint_text: "Enter Page No"
        text_color_focus: 75/255,0/255,130/255,1
        hint_text_color_focus: 75/255,0/255,130/255,1
        line_color_focus: 75/255,0/255,130/255,1
        pos_hint: {'center_x':.5,'center_y':.5}
        width:250

<Content2>:
    orientation:"vertical"
    spacing:"12dp"
    size_hint_y:None
    size_hint_x:.5
    height:"155dp"
        
<ElementCard@MDCard>:
    md_bg_color:255/255,255/255,255/255,1
    padding:dp(15)
    radius:dp(25)
    elevation: 3
    image:''
    text:""
    ripple_behavior: True
    orientation:'vertical'
    Image:
        source:root.image
    MDBoxLayout:
        oriental:'vertical'
        MDLabel:
            halign:"center"
            text:root.text


<TextToSpeech>:

    Camera:
        id: camera2
        resolution: (640, 480)
        play: True
        index: 2
        size_hint_x: 0.9
        pos_hint: {'center_x':.5,'center_y':.7}
        allow_stretch: True

    MDLabel:
        id: name_label2
        pos_hint: {'center_x':.5,'center_y':.315}
        size_hint: .8, .4
        halign: "center"
        background_color: .5, .5, .5, .3
        canvas.before:
            Color:
                rgba: self.background_color
            RoundedRectangle:
                pos: 18,97
                size: 315,200
                radius: [25]

    MDFillRoundFlatIconButton:
        text: "Capture"
        icon: "camera"
        md_bg_color: 75/255,0/255,130/255,1
        elevation: 0
        size_hint: .3,.1
        pos_hint: {'center_x':.8,'center_y':.1}
        on_press: root.capture_image2()

    MDFillRoundFlatIconButton:
        text: "Back"
        icon: "undo"
        size_hint: .3,.1
        md_bg_color: 75/255,0/255,130/255,1
        elevation: 0
        pos_hint: {'center_x':.2,'center_y':.1}
        on_press: root.back_button()

    BoxLayout:
        Widget:
        MDFloatingActionButton:
            icon: "microphone"
            md_bg_color: 75/255,0/255,130/255,1
            elevation: 0
            pos_hint: {"center_x": .5, "center_y": .1}
            on_press: root.onclick()
        Widget:

   
<ImageToAudio>:

    Image:
        id: my_img
        source: ""
        size_hint_x: 0.8
        pos_hint: {'center_x':.5,'center_y':.33}
        allow_stretch: True

    Camera:
        id: camera
        resolution: (640, 480)
        play: True
        index: 2
        size_hint_x: 0.8
        pos_hint: {'center_x':.5,'center_y':.685}
        allow_stretch: True

    MDLabel:
        id: name_label
        pos_hint: {'center_x':.5,'center_y':.915}
        halign: "center"
        background_color: .5, .5, .5, .3
        canvas.before:
            Color:
                rgba: self.background_color
            RoundedRectangle:
                pos: 25,525
                size: 300,50
                radius: [25]



    MDIconButton:
        icon: "folder"
        pos_hint: {"center_x": .85, "center_y": .91}
        on_press: root.file_choose()



    MDFillRoundFlatIconButton:
        text: "Capture"
        icon: "camera"
        md_bg_color: 75/255,0/255,130/255,1
        elevation: 0
        size_hint: .3,.1
        pos_hint: {'center_x':.8,'center_y':.1}
        on_press: root.capture_image()

    MDFillRoundFlatIconButton:
        text: "Back"
        icon: "undo"
        size_hint: .3,.1
        md_bg_color: 75/255,0/255,130/255,1
        elevation: 0
        pos_hint: {'center_x':.2,'center_y':.1}
        on_press: root.back_button()

    BoxLayout:
        Widget:
        MDFloatingActionButton:
            icon: "microphone"
            md_bg_color: 75/255,0/255,130/255,1
            elevation: 0
            pos_hint: {"center_x": .5, "center_y": .1}
            on_press: root.onclick()
        Widget:


<SpeechToText>:

    MDLabel:
        id: name_label3
        pos_hint: {'center_x':.5,'center_y':.87}
        size_hint: .8, .9
        halign: "center"
        background_color: .5, .5, .5, .3
        canvas.before:
            Color:
                rgba: self.background_color
            RoundedRectangle:
                pos: 18,100
                size: 315,470
                radius: [25]

    MDFillRoundFlatIconButton:
        text: "Back"
        icon: "undo"
        size_hint: .3,.1
        md_bg_color: 75/255,0/255,130/255,1
        elevation: 0
        pos_hint: {'center_x':.2,'center_y':.1}
        on_press: root.back_button()

    MDFillRoundFlatIconButton:
        text: "Send"
        icon: "whatsapp"
        md_bg_color: 75/255,0/255,130/255,1
        elevation: 0
        size_hint: .3,.1
        pos_hint: {'center_x':.8,'center_y':.1}
        on_press: root.whatsapp_button()

    BoxLayout:
        Widget:
        MDFloatingActionButton:
            icon: "microphone"
            md_bg_color: 75/255,0/255,130/255,1
            elevation: 0
            pos_hint: {"center_x": .5, "center_y": .1}
            on_press: root.onclick()
        Widget:

''')


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None


class SplashScreen(Screen):
    pass


class Content(BoxLayout):
    pass


class Content2(BoxLayout):
    pass


class VirtualEye(Screen):

    dialog = None
    commands_dialog = None
    recognizer = sr.Recognizer()

    def Back_Button(self, audio):
        st = threading.Thread(
            target=self._Back_Button, args=(audio,))
        st.start()

    def _Back_Button(self, audio):
        print("button pressed")
        playsound(audio)

    #### Speak ####

    def Speak(self, audio):

        speech_thread = threading.Thread(
            target=self._Speak, args=(audio,))
        speech_thread.start()

    def _Speak(self, audio):

        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 185)
        engine.say(audio)
        engine.runAndWait()

    #### mic button ####

    def onclick(self):

        print("button pressed")
        self.cmd()

    #### Microphone funtioning ####

    def mic(self):

        global text

        with sr.Microphone() as source:
            print("Listening....")
            playsound(
                'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\mic.mp3')
            self.recognizer.adjust_for_ambient_noise(source, duration=0)
            recordedaudio = self.recognizer.listen(source)

            try:
                print('Recognizing....')
                text = self.recognizer.recognize_google(
                    recordedaudio, language='en-US')
                text = text.capitalize()
                print('You said:', format(text))
                self._Speak(text)

            except Exception:
                self.Speak('Please Say Again')
                self.cmd()

            return text

    #### functions of command ####

    def cmd(self):

        text = self.mic()

        if 'Open pdf to audio' in text:
            self.pdf_to_audio()

        elif 'Open image to audio' in text:
            self.image_to_audio()

        elif 'Open speech to text' in text:
            self.speech_to_text()

        elif 'Open text to speech' in text:
            self.text_to_speech()

        elif 'Go to homepage' in text:
            self.manager.current = 'screen_one'

        elif 'Mic off' or 'Microphone off' in text:
            pass

        else:
            self.Speak('Please Say Again')
            print('Please Say Again')
            self.cmd()

    #### PDF To Audio (Audio Access) ####

    def pdf_to_audio(self):

        print('Button Clicked')
        self._Speak('Say The File Name')
        text = self.mic()

        rootDir = "C:\\Users\\"
        fileToSearch = f'{text}.pdf'

        try:
            for relPath, dir, files in os.walk(rootDir):
                if (fileToSearch in files):
                    self.ids.pdf_label.text = f'{fileToSearch}'
                    self.fullPath = os.path.join(
                        rootDir, relPath, fileToSearch)
                    self.fullPath = self.openpdf()
                    self.Speak("pages")
                    self.Speak(self.pages)
                    self._Speak("Say The Page Number")
                    self.pagenumber()
                    break
            else:
                self.Speak('File Not Found')
                self.pdf_to_audio()

        except Exception:
            self.Speak('File Not Found')
            self.pdf_to_audio()

    #### open file for pdf to audio ####

    def openpdf(self):

        print(self.fullPath)
        self.book = open(self.fullPath, 'rb')
        self.pdfReader = PyPDF2.PdfFileReader(self.book)
        self.pages = self.pdfReader.numPages
        print('Total pages:', self.pages)

    #### Page Number ####

    def pagenumber(self):

        text = self.mic()
        num = w2n.word_to_num(text)
        if num > self.pages:
            self.Speak('Page Number Exceeds The Total Pages')
            self.pagenumber()
        elif num <= self.pages:
            page = self.pdfReader.getPage(num-1)
            read = page.extractText()
            self.Speak(read)
        else:
            self.Speak('Check Page Number')
            self.pagenumber()

    #### PDF To Audio (Manual Access) ####

    def pdf_to_audio_button(self):

        global pdfname
        print('Button Clicked')
        self.my_file = filechooser.open_file()
        label = Label(text=self.my_file).pack()
        print(self.my_file)
        r = "".join(self.my_file)
        r = r[::-1]
        s = r.find("\\")
        pdfname = r[0:s]
        pdfname = pdfname[::-1]
        if self.my_file == []:
            print("pdf not selected")
        else:
            if not self.dialog:
                self.dialog = MDDialog(
                    type="custom",
                    radius=[20, 7, 20, 7],
                    auto_dismiss=False,
                    content_cls=Content(),
                    pos_hint={"center_x": .5, "center_y": .5},
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            on_press=self.cancel),
                        MDRaisedButton(text="OK", md_bg_color=(75/255, 0/255, 130/255, 1),
                                       on_press=self.ok_dialog),

                    ],
                )
            self.dialog.open()

    #### pdf to audio page no dialog box ok button ####

    def ok_dialog(self, obj):

        self.dialog.dismiss()
        print('Enter Page No:', self.dialog.content_cls.ids.pgno.text)
        try:
            for file in self.my_file:
                self.fullPath = file
                self.fullPath = self.openpdf()
                if int(self.dialog.content_cls.ids.pgno.text) > self.pages:
                    Snackbar(text='Page Number Exceeds The Total Pages', bg_color=(
                        75/255, 0/255, 130/255, 1)).open()
                else:
                    self.ids.pdf_label.text = f'{pdfname}'
                    page = self.pdfReader.getPage(
                        int(self.dialog.content_cls.ids.pgno.text)-1)
                    read = page.extractText()
                    self.Speak(read)
                    self.dialog.content_cls.ids.pgno.text = ''
                    break
        except:
            self.dialog.content_cls.ids.pgno.text = ''
            Snackbar(text='Invalid File Name', bg_color=(
                75/255, 0/255, 130/255, 1)).open()

    #### pdf to audio page no dialog box cancel button ####

    def cancel(self, obj):

        self.dialog.content_cls.ids.pgno.text = ''
        self.dialog.dismiss()

    def cancel2(self, obj):

        self.commands_dialog.dismiss()

    #### Image To Audio (Audio and Manual Access) ####

    def image_to_audio(self):

        print('Button Clicked')
        self.manager.current = 'screen_two'

    #### Text To Speech ####

    def text_to_speech(self):

        print('Button Clicked')
        self.manager.current = 'screen_three'

    #### Speech To Text ####

    def speech_to_text(self):

        print('Button Clicked')
        self.manager.current = 'screen_four'

    def TTS(self, obj):
        self._Speak("Open Text To Speech")

    def ITA(self, obj):
        self._Speak("Open Image To Audio")

    def STT(self, obj):
        self._Speak("Open Speech To Text")

    def PTA(self, obj):
        self._Speak("Open PDF To Audio")

    def commands(self):

        if not self.commands_dialog:
            self.commands_dialog = MDDialog(
                title="Commands",
                radius=[20, 7, 20, 7],
                auto_dismiss=False,
                content_cls=Content2(),
                pos_hint={"center_x": .5, "center_y": .5},
                type="confirmation",
                items=[
                    ItemConfirm(text="Open Text to Speech", on_press=self.TTS),
                    ItemConfirm(text="Open Image to Audio", on_press=self.ITA),
                    ItemConfirm(text="Open Speech to Text", on_press=self.STT),
                    ItemConfirm(text="Open PDF to Audio", on_press=self.PTA),
                ],
                buttons=[
                    MDFlatButton(
                        text="OK",
                        font_size=12,
                        on_press=self.cancel2),
                ],
            )
        self.commands_dialog.open()


class ImageToAudio(Screen):

    #### back button in image to audio ####

    def back_button(self):

        self.ids.name_label.text = ""
        self.ids.my_img.source = ""
        self.manager.current = 'screen_one'
        VirtualEye().Back_Button(
            'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\back-button.mp3')

    def onclick(self):
        t = VirtualEye().mic()
        if 'Go to homepage' in t:
            self.back_button()

        elif 'Mic off' in t:
            pass

        elif 'Capture' in t:
            self.capture_image()

        else:
            pass

    #### To capture the image (Audio Access) ####

    def capture_image(self):
        print("captured")
        playsound(
            'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\camera-shutter.mp3')
        self.ids.camera.export_to_png("captured_image.png")
        self.detect_image("captured_image.png")

    #### detect the object in the image ####

    def detect_image(self, img_name):
        # Load Yolo

        net = cv2.dnn.readNet("C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\yolov3.weights",
                              "C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\yolov3.cfg")
        classes = []
        with open("C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1]
                         for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # Loading image
        img = cv2.imread(img_name)
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(
            img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        l = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                l += [label]
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

        dict1 = {i: l.count(i) for i in l}
        dict2 = {}
        for i in dict1:
            dict2.setdefault(dict1[i], []).append(i)

        output_str = ""
        for k, v in dict1.items():
            output_str += f"{k}: {v}, "
        output_str = output_str.rstrip(", ")
        print(output_str)

        try:
            if l == []:
                print("Capture Again")
                VirtualEye()._Speak("Capture Again")
            else:
                self.ids.name_label.text = f'{output_str}'
                VirtualEye().Speak(dict2)

        except Exception:
            print("Capture Again!")
            VirtualEye().Speak("Capture Again")

    #### image to audio file manager ####

    def file_choose(self):
        choosen_file = filechooser.open_file()
        try:
            if choosen_file == []:
                print("file not selected")
            else:
                file_name = str(choosen_file).replace(
                    '[', '').replace(']', '').replace('\'', '').replace('\"', '')
                print(file_name)
                self.ids.my_img.source = file_name
                self.detect_image(file_name)
        except Exception:
            self.ids.name_label.text = f'File Not Found'


class TextToSpeech(Screen):

    def back_button(self):
        self.ids.name_label2.text = ''
        self.manager.current = 'screen_one'
        VirtualEye().Back_Button(
            'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\back-button.mp3')

    def onclick(self):
        t = VirtualEye().mic()
        if 'Go to homepage' in t:
            self.back_button()

        elif 'Mic off' in t:
            pass

        elif 'Capture' in t:
            self.capture_image2()

        else:
            pass

    def capture_image2(self):

        print("captured")
        playsound(
            'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\camera-shutter.mp3')
        self.ids.camera2.export_to_png("text_image.png")
        pyt.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        img = cv2.imread("text_image.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        text = pyt.image_to_string(img)
        if text == '':
            print("Capture Again")
            VirtualEye().Speak("Capture Again")
        else:
            self.ids.name_label2.text = f'{text}'
            VirtualEye().Speak(text)
            print(text)


class SpeechToText(Screen):

    def back_button(self):
        self.ids.name_label3.text = ''
        self.manager.current = 'screen_one'
        VirtualEye().Back_Button(
            'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\back-button.mp3')

    def onclick(self):

        global msg
        global username

        t = VirtualEye().mic()
        if 'Go to homepage' in t:
            self.back_button()

        elif 'Mic off' in t:
            pass

        elif 'send this message to' in t:
            self.ids.name_label3.text = f'{t}'
            list_t = t.split()
            print(list_t)

            index2 = list_t.index("send", -7, -1)
            msg = " ".join(list_t[0:index2])
            print(msg)

            index = list_t.index("to", -5, -1)
            username = " ".join(list_t[index+1:])
            username = username.title()
            print(username)

            self.confirm()

        else:
            self.ids.name_label3.text = f'{t}'
            pass

    def confirm(self):
        VirtualEye()._Speak("Say yes for confirmation")
        text = VirtualEye().mic()
        try:
            if 'Yes' in text:

                options = webdriver.ChromeOptions()
                options.add_argument(
                    "user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Wtsp")
                options.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])

                chrome_executable = Service('chromedriver.exe')
                browser = webdriver.Chrome(
                    service=chrome_executable, options=options)

                browser.maximize_window()

                browser.get('https://web.whatsapp.com/')

                search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

                search_box = WebDriverWait(browser, 500).until(
                    EC.presence_of_element_located(
                        (By.XPATH, search_xpath))
                )

                search_box.clear()

                time.sleep(1)

                pyperclip.copy(username)

                search_box.send_keys(Keys.CONTROL + "v")

                time.sleep(2)

                group_xpath = f'//span[@title="{username}"]'
                group_title = browser.find_element(By.XPATH, group_xpath)

                group_title.click()

                time.sleep(1)

                input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
                input_box = browser.find_element(By.XPATH, input_xpath)
                pyperclip.copy(msg)
                input_box.send_keys(Keys.CONTROL + "v")
                input_box.send_keys(Keys.ENTER)
                time.sleep(3)
                playsound(
                    'C:\\Users\\User\\OneDrive\\Desktop\\Virtual Eye App\\sound\\Whatsapp.mp3')
                Snackbar(text='Sent', bg_color=(
                    75/255, 0/255, 130/255, 1)).open()
                VirtualEye().Speak("Sent")

            elif 'No' in text:
                Snackbar(text="Confirmation Declined", bg_color=(
                    75/255, 0/255, 130/255, 1)).open()
                VirtualEye().Speak("Confirmation Declined")

            else:
                self.confirm()

        except Exception:

            Snackbar(text='Name Not Found', bg_color=(
                75/255, 0/255, 130/255, 1)).open()
            VirtualEye().Speak('Name Not Found')

    def whatsapp_button(self):

        global msg
        global username

        if self.ids.name_label3.text == '':
            pass
        else:
            print("Say receiver's name")
            VirtualEye().Speak("Say receiver's name")
            username = VirtualEye().mic()
            username = username.title()
            print(username)
            msg = self.ids.name_label3.text
            self.confirm()
            self.ids.name_label3.text = ''


class VirtualEyeApp(MDApp):

    def build(self):

        global sm
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(SplashScreen(name='pre_splash'))
        sm.add_widget(VirtualEye(name='screen_one'))
        sm.add_widget(ImageToAudio(name='screen_two'))
        sm.add_widget(TextToSpeech(name='screen_three'))
        sm.add_widget(SpeechToText(name='screen_four'))

        VirtualEye().Speak("Welcome To Virtual Eye")

        return sm

    def send_data(self, name, phoneno):
        self.cursor.execute("select * from contacts")
        name_list = []
        for i in self.cursor.fetchall():
            name_list.append(i[0])

        if name.text.capitalize() in name_list or name.text == "":
            Snackbar(text='Name Already Exists!', bg_color=(
                75/255, 0/255, 130/255, 1)).open()

        else:
            self.cursor.execute(
                f"insert into contacts values('{name.text.capitalize()}', '{phoneno.text}')")
            self.database.commit()
            Snackbar(text='Saved', bg_color=(
                75/255, 0/255, 130/255, 1)).open()
            name.text = ""
            phoneno.text = ""

    def on_start(self):

        Clock.schedule_once(self.first_screen, 13)

    def first_screen(self, *args):

        sm.current = 'screen_one'


if __name__ == '__main__':
    VirtualEyeApp().run()
