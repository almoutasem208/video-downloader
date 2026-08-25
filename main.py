import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase

import arabic_reshaper
from bidi.algorithm import get_display
import yt_dlp

if os.path.exists('arial.ttf'):
    LabelBase.register(name='Arabic', fn_regular='arial.ttf')
    FONT_NAME = 'Arabic'
else:
    FONT_NAME = None

def fix_arabic(text):
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

class DownloaderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        
        self.title_label = Label(
            text=fix_arabic("تطبيق تنزيل الفيديوهات"),
            font_name=FONT_NAME,
            font_size='24sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.title_label)
        
        self.url_input = TextInput(
            hint_text='ضع رابط الفيديو هنا / Paste Link Here',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.url_input)
        
        self.download_btn = Button(
            text=fix_arabic("بدء التنزيل"),
            font_name=FONT_NAME,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.download_btn.bind(on_press=self.start_download)
        self.add_widget(self.download_btn)
        
        self.status_label = Label(
            text=fix_arabic("جاهز للتنزيل..."),
            font_name=FONT_NAME,
            font_size='16sp'
        )
        self.add_widget(self.status_label)

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = fix_arabic("يرجى إدخال رابط صحيح!")
            return
            
        self.status_label.text = fix_arabic("جاري التحميل...")
        try:
            ydl_opts = {
                'outtmpl': '/sdcard/Download/%(title)s.%(ext)s',
                'format': 'best',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.text = fix_arabic("تم التنزيل بنجاح في مجلد Downloads!")
        except Exception as e:
            self.status_label.text = fix_arabic("حدث خطأ أثناء التنزيل")

class DownloaderApp(App):
    def build(self):
        return DownloaderLayout()

if __name__ == '__main__':
    DownloaderApp().run()
