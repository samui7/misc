# A GUI tile efficiency calculator for Japanese mahjong.
#
# 1. The function of this calculator depends on PhantomJS. 
#    See http://phantomjs.org/
# 2. For information on the formal way to encode a hand,
#    see https://mahjong.guide/2017/03/18/mahjong-tools-1-tenhous-efficiency-calculator/
  

from tkinter import *
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


class Calculator():

    def __init__(self, master):

        top_frame = Frame(master, width=400)
        bottom_frame = Frame(master, width=400)
        top_frame.pack(side=TOP)
        bottom_frame.pack(side=BOTTOM)

        hand_label = Label(top_frame, text="Hand:")
        hand_label.grid(row=0, column=0)

        self.hand_entry = Entry(top_frame, width=28)
        self.hand_entry.grid(row=0, column=1)

        submit_button = Button(top_frame, text="Submit", command=self.calculate)
        submit_button.grid(row=0, column=2)

        message_label = Label(top_frame, text="Click Submit and wait. The process can take up to 10 seconds.")
        message_label.grid(row=1, columnspan=3)

        self.output_box = Text(bottom_frame, width=50, height=10)
        self.output_box.pack(side=LEFT, fill=Y)

        output_scroll_bar = Scrollbar(bottom_frame)
        output_scroll_bar.pack(side=RIGHT, fill=Y)

        output_scroll_bar.config(command=self.output_box.yview)
        self.output_box.config(yscrollcommand=output_scroll_bar.set)

    def calculate(self):
        # clear the output text box
        self.output_box.delete(1.0, END)
        
        # ask tenhou.net
        hand_string = str(self.hand_entry.get())
        url = "https://tenhou.net/2/?q=" + hand_string
        driver = webdriver.PhantomJS()
        driver.get(url)
        result = driver.find_element_by_tag_name('textarea').text
        
        # print the result to the text box below
        self.output_box.insert(END, result)


root = Tk()
cal = Calculator(root)
root.mainloop()