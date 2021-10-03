'''
    Youtube Downloader GUI code version 01
    Auxillary project meant to download youtube's video intially
    will be upgraded to download from any sites
    Still under modifications
    Secured source license
'''

#!/usr/bin/env python3
# enconding: utf-8

__version__ = 1.4
__status__ = "Prototype"
__author__ = "Jamiu Mustorpha"
__date__ = "09-08-2021"
__all__ = "YoutubeDownloader : __init, searchVideo, progressbar, clear, videodownload"

import builtins
import io
from logging import PercentStyle
from tkinter import* 
from tkinter import ttk
from tkinter import messagebox
from pytube import* 
from PIL import Image,ImageTk
import requests

class YoutubeDownload:

    def __init__(self,root):
        self.root=root
        self.root.title("Youtube Downloader")
        self.root.geometry("600x650+100+50")
        self.root.resizable(False,False)
        self.root.config(bg="white")

        sframe1=Frame(self.root,bg="white").place(x=20,y=50,width=560,height=540)
        lbl_heading=Label(self.root,text="Youtube Downloader ",font=("foco",20),bg="white",fg="blue",padx=30,pady=5).place(x=20,y=10,width=560,height=30)
        lbl_footer=Label(self.root,text="Developed by Mustorpha M.O #2021",font="foco",bg="white",fg="#2c2b78",padx=30,pady=5)
        lbl_footer.place(x=20,y=595,width=560,height=30)

        lbl_url=Label(self.root,text="Link URL:",font="foco",bg="#73243e",fg="#fff",padx=10,pady=5,anchor=NW)
        lbl_url.place(x=20,y=90,width=100,height=30)
        self.enterUrl=StringVar()
        self.entryUrl=Entry(self.root,font="foco",borderwidth=1 ,relief="solid",textvariable=self.enterUrl)
        self.entryUrl.place(x=125,y=90,width=454,height=30)
        self.qualityHD=["Select","Low Quality","High Quality","Audio"]
        self.lbl_quality=Label(self.root,text="Quality",font="foco",bg="#73243e",fg="#fff",padx=10,pady=5,anchor=NW)
        self.lbl_quality.place(x=20,y=130,width=100,height=30)
        self.lbl_choose=ttk.Combobox(self.root,values=self.qualityHD,state="readonly",font="foco")
        self.lbl_choose.place(x=125,y=130,width=454,height=30)
        self.lbl_choose.current(0)
        btn_Clear=Button(self.root,text="Clear",command=self.clear,font="foco",background="#73243e",fg="white").place(x=20,y=164,width=100,height=30)
        btn_search=Button(self.root,text="Search",command=self.searchVideo,font="foco",bg="#17a2b8",fg="white").place(x=125,y=164,width=454,height=30)

        frame2=Frame(self.root, bg="#6c0979").place(x=22,y=200,width=555,h=375)
        self.lbl_title=Label(self.root,text="Title",font=("foco",14),foreground="black",anchor=NW)
        self.lbl_title.place(x=22,y=200,width=555,height=31)
        self.lbl_desc=Text(self.root,borderwidth=1,relief="solid")
        self.lbl_desc.place(x=22,y=233,width=375,height=215)
        self.lbl_img=Label(self.root,text="Thumbnail",font="foco",padx=10,pady=5,bg="white")
        self.lbl_img.place(x=398,y=233,width=177,height=215)
        lbl_size_tex=Label(self.root,text="File size:",bg="#50D8D7",fg="black",font="foco",anchor=NW).place(x=22,y=455,width=80,height=30)
        self.lbl_size=Label(self.root,text="0 MB",font="foco",anchor=NW)
        self.lbl_size.place(x=103,y=455,width=90,height=30)
        self.btn_download=Button(self.root,text="Download",command=self.videoDownload,state="disabled",bg="#17a2b8",fg="#fff",font="foco")
        self.btn_download.place(x=195,y=455,width=380,height=30)
        self.lbl_downloading=Label(self.root,text="Downloading... 0%",font="foco",padx=10,pady=5)
        self.lbl_downloading.place(x=150,y=490,width=315,height=30)
        self.progressBar=ttk.Progressbar(self.root,orient=HORIZONTAL,length=500,mode="determinate")
        self.progressBar.place(x=22,y=525,width=555,height=50)

    def searchVideo(self):
        choice=self.lbl_choose.get()
        url=self.enterUrl.get()
        if self.enterUrl.get()=='':
            messagebox.showerror("Error","Link URL Required....")
        else:
          
            if(len(url)>1):

                
                yt=YouTube(url)
                if(choice== self.qualityHD[1]):
                    dooro=yt.streams.filter(progressive=True).first()
            
                elif(choice==self.qualityHD[2]):
                    dooro=yt.streams.filter(progressive=True).last()
                elif(choice==self.qualityHD[3]):
                    dooro=yt.streams.filter(only_audio=True).first()
                        
                else:
                    messagebox.showerror("Error","Kalab")
                  
                  
                self.lbl_title.config(text=yt.title)
                self.lbl_desc.delete('1.0',END)
                self.lbl_desc.insert(END,yt.description[:200])

                readImg=requests.get(yt.thumbnail_url)
                imgio=io.BytesIO(readImg.content)
                self.load=Image.open(imgio)
                self.load=self.load.resize((180,164),Image.ANTIALIAS)
                self.render=ImageTk.PhotoImage(self.load)
                self.lbl_img.config(image=self.render)
                self.lbl_img.image=self.render
                


                self.file_size=dooro.filesize
                xl=self.file_size/1024000
                to_mb=(str(round(xl,2)))+ ' MB'
                self.lbl_size.config(text=to_mb)
                self.btn_download.config(state=NORMAL)

    def progressbar(self,streams,chunk,bytes_remaining):
        
        percentage=(float(abs(bytes_remaining-self.file_size)/self.file_size)) *float(100)
        self.progressBar['value']=percentage
        self.progressBar.update()
        self.lbl_downloading.config(text=f'Downloading... {str(round(percentage,2))} %')
        if round(percentage,2)==100:
            messagebox.showinfo("Successfull","Video Has been Download..")
            self.btn_download.config(state=DISABLED)
            self.clear()

    def clear(self):
        self.enterUrl.set('')
        self.btn_download.config(state=DISABLED)
        self.progressBar['value']=0
        self.lbl_downloading.config(text='Download 0%')
        self.lbl_choose.current(0)
        self.lbl_desc.delete('1.0',END)
        self.lbl_size.config(text="0 MB")
        self.lbl_img.config(image="")
        self.lbl_title.config(text="Title")


    def videoDownload(self):
        xchoice=self.lbl_choose.get()
        url=self.enterUrl.get()
        if(len(url)):
            yt=YouTube(url,on_progress_callback=self.progressbar)
            if(xchoice == self.qualityHD[1]):
                dooro=yt.streams.filter(progressive=True).first()
            elif(xchoice==self.qualityHD[2]):
                dooro=yt.streams.filter(progressive=True).last()
            elif(xchoice == self.qualityHD[3]):
                dooro=yt.streams.filter(only_audio=True).first()
            else:
                messagebox.showerror("Error","Failed...")
            
            dooro.download("C:")
            



root=Tk()
oj=YoutubeDownload(root)
root.mainloop()
