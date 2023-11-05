###################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
    from dotenv import load_dotenv
    from constants import *
    load_dotenv()
except Exception as e:
	raise e

""" System Modules """
try:
	import os
	import speech_recognition as sr
	import pyttsx3
	from tkinter import *
	from time import sleep
	from threading import Thread
	import webbrowser as wb
	import datetime
	from PIL import ImageGrab 
	import requests
 
except Exception as e:
	print(e)

############################################ SET UP VOICE ###########################################
try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
except Exception as e:
	print(e)

####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Speaking...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	engine.say(text)
	engine.runAndWait()

####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
	print('\nListening...')
	AITaskStatusLbl['text'] = 'Listening...'
	r = sr.Recognizer()
	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			AITaskStatusLbl['text'] = 'Processing...'
			said = r.recognize_google(audio)
			print(f"\nMe: {said}")
			if clearChat:
				clearChatScreen()
			if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(said)
		except Exception as e:
			print(e)
			if "connection failed" in str(e):
				speak("Your System is Offline...", True, True)
			return 'None'
	return said.lower()

def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def voiceMedium():
    while True:
        query = record()
        if query == 'None': continue
        if isContain(query, EXIT_COMMANDS):
            speak("Good Bye! I love you", True, True)
            os._exit(0)
        else: main(query.lower())

def keyboardInput(e):
	user_input = UserField.get().lower()
	if user_input!="":
		clearChatScreen()
		if isContain(user_input, EXIT_COMMANDS):
			speak("Good Bye! I love you", True, True)
			os._exit(0)
		else:
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(user_input.capitalize())
			Thread(target=main, args=(user_input,)).start()
		UserField.delete(0, END)

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()

######################## CHANGING CHAT MODE #########################
chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		# appControl.volumeControl('mute')
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
		chatMode=0
	else:
		# appControl.volumeControl('full')
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		root.focus()
		chatMode=1

########################################################################

# Function to get weather information for a specific city from OpenWeatherMap API
def get_weather(city):
    api_key = "fe8d8c65cf345889139d8e545f57819a"  
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    weather_data = response.json()
    
    if weather_data["cod"] != "404":
        # Extracting data
        main_data = weather_data["main"]
        temperature_kelvin = main_data["temp"]
        temperature_celsius = round(temperature_kelvin - 273.15)
        humidity = main_data["humidity"]
        weather_desc = weather_data["weather"][0]["description"]
        city_name = weather_data["name"]

        weather_info = f"In {city_name}\nThe temperature is: {temperature_celsius}°C\nThe humidity is: {humidity}%\nWeather description: {weather_desc}"
        return weather_info
    else:
        return "City not found. Please enter a valid city name."


def main(text):
    while True:
        if isContain(text, ['hello', 'hi']):
            hour=datetime.datetime.now().hour
            if hour >=0 and hour<12:
                speak('Good Morning Sir! Can I help you?', True, True)
                return
            if hour>=12 and hour<18:
                speak('Good Afternoon Sir! Can I help you?', True, True)
                return
            elif hour>=18 and hour<24:
                speak("Good Evening sir! Can I help you?", True, True)
                return
        
        elif 'name' in text:
            speak('My name is PONY. Nice to meet you!', True, True)
            return
        
        elif "google" in text:
            speak('What do you want to search?', True, True)
            search=record().lower()
            url = f"https://google.com/search?q={search}"
            wb.get().open(url)
            speak(f'Here is your {search} on Google', True, True)
            return
        
        elif "open website" in text:
            speak("Please specify the website URL!", True, True)
            website = record().lower()
            website = f"https://{website}.com"
            wb.get().open(website)
            speak(f"Opening the website: {website}", True, True)
            return
        
        elif "youtube" in text:
            speak('What do you want to watch?', True, True)
            search=record().lower()
            url = f"https://youtube.com/search?q={search}"
            wb.get().open(url)
            speak(f'Here is your {search} on Youtube', True, True)
            return
            
        elif "music" in text:
            speak('Which song?', True, True)
            song = record().lower()
            if "attention" in song:
                mu = r'C:\Users\thenh\OneDrive\Desktop\Music\attention.mp3'
                os.startfile(mu)
                return song
            elif "see you again" in song:
                mu1 = r'C:\Users\thenh\OneDrive\Desktop\Music\See you again.mp3'
                os.startfile(mu1)
            return
        
        elif "time" in text:
            Time=datetime.datetime.now().strftime("%I:%M %p") 
            speak("It's " + Time, True, True) 
            return
        
        elif isContain(text,['word', 'work']):
            word = r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'
            os.startfile(word)
            return
                
        elif "excel" in text:
            excel = r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE'
            os.startfile(excel)
            return
        
        elif isContain(text,['screenshot', 'capture']): 
            file_path = r'C:\Users\thenh\OneDrive\Pictures\Screenshots\screenshot.png'
            im = ImageGrab.grab()  
            im.save(file_path)             
            os.startfile(file_path)
            speak("Screenshot taken and saved.", True, True)
            return
        
        elif "weather" in text:
            city = text.split("in")[-1].strip()
            weather_info = get_weather(city)
            speak(weather_info, True, True)
            return
       
        else:
            speak("I don't know anything about this :<", True, True)
            return

#####################################  MAIN GUI ####################################################

if __name__ == '__main__':
	root = Tk()
	root.title('PONY')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)
	root3 = Frame(root, bg=background)

	for f in (root1, root2, root3):
		f.grid(row=0, column=0, sticky='news')	
	
	#Chat Frame
	chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	TextModeFrame.pack_forget()

	cblDarkImg = PhotoImage(file='assets/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Keyboard Button
	kbphDark = PhotoImage(file = 'assets/images/keyboard1.png')
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "assets/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Text Field
	TextFieldImg = PhotoImage(file='assets/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.insert(0, "")
	UserField.bind('<Return>', keyboardInput)
	
	#User and Bot Icon
	userIcon = PhotoImage(file="assets/images/avatars/ChatIcons/a2.png")
	botIcon = PhotoImage(file="assets/images/assistant.png")
	botIcon = botIcon.subsample(2,2)

	try:  
		Thread(target=voiceMedium).start()
	except:
		pass

	root.iconbitmap('assets/images/logo.ico')
	raise_frame(root1)
	root.mainloop()