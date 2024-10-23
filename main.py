

import customtkinter as ctk
from customtkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk 
import openai
import base64
from random import randint
from time import sleep
import os
import shutil

key = open(r"C:\Users\sonja\Desktop\SciFinder\APIKey.txt")
openai.api_key = key.read()

#Bahnschrift font

#Background color: #292930
#Active Background color: #1F1F24
#Foreground/text color: #8EABE6
#Active Foreground color: #7289B8

# For testing images via url in OpenAI use this:
# "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
def identify():
    window.destroy()
    renderFrame(filename)
    root.update()
    
    loadingText = ctk.CTkLabel(window, text="   Identifying...", font=("Bahnschrift", 30), fg_color="transparent", bg_color = "transparent", text_color="#8EABE6", height=35)
    loadingText2 = ctk.CTkLabel(window, text="(may take a few seconds)", font = ("Bahnschrift", 12), fg_color = "transparent", bg_color = "transparent", text_color="#8EABE6")

    renderLoading(loadingText, loadingText2)
    answer = getImageResponse()



    loadingText.destroy()
    loadingText2.destroy()

    if ";" in answer:
        paddingIden = ctk.CTkLabel(window, text="", bg_color="transparent", fg_color="transparent", height = 10)
        paddingIden.pack()

        stanName = answer[:answer.index(";")]
        sciName = answer[answer.index(";") + 2:]

        standardName = ctk.CTkLabel(window, text = stanName, font=("Bahnschrift", 28), bg_color="transparent", fg_color="transparent", text_color="#FFFFFF", height=35)
        standardName.pack()
        scientificName = ctk.CTkLabel(window, text="(" + sciName + ")", font=("Bahnschrift", 17), bg_color = "transparent", fg_color="transparent", text_color="#8EABE6", height = 35)
        scientificName.pack()
    else:
        failLabel = ctk.CTkLabel(text = "Could not identify a creature. Try a different image.", font=("Bahnschrift", 12), bg_color = "#292930", fg_color="#8EABE6")
        failLabel.pack()
    
    learnButton = ctk.CTkButton(window, text="Learn more", bg_color="transparent", font=("Bahnschrift", 17), hover_color="#FFFFFF", fg_color = "transparent", text_color="#8EABE6", border_color= "#8EABE6", border_width=2, corner_radius=100, width=70, height = 30, command= lambda: learnMore(stanName))
    learnButton.pack()

def learnMore(stan):
    window.destroy()
    renderFrame(filename)
    root.update()


    learnLoadingText = ctk.CTkLabel(window, text="   Getting description...", font=("Bahnschrift", 26), fg_color="transparent", bg_color = "transparent", text_color="#8EABE6", height=35)
    learnLoadingText2 = ctk.CTkLabel(window, text="(may take a few seconds)", font = ("Bahnschrift", 12), fg_color = "transparent", bg_color = "transparent", text_color="#8EABE6")
    learnLoadingText.pack()
    learnLoadingText2.pack()
    root.update()

    ans = getTextResponse(stan)

    learnLoadingText.destroy()
    learnLoadingText2.destroy()

    paddingLearn = ctk.CTkLabel(window, text="", bg_color="transparent", fg_color="transparent", height = 10)
    paddingLearn.pack()
    description = ctk.CTkLabel(window, wraplength=400, text=ans, text_color="#8EABE6", font = ("Bahnschrift", 12), fg_color="transparent", bg_color="transparent")
    description.pack()
    pass

def renderLoading(text, text2):
    text.pack()
    text2.pack()
    root.update()

def getTextResponse(standardName):
    response = openai.chat.completions.create(model="gpt-4o", messages=[
            {"role": "system", "content": "You are identifying organisms."},
            {
                "role": "user",
                "content": [
            {"type": "text", "text": "Tell me a few sentences about " + standardName + "."},
        ],
            }
    ])
    return response.choices[0].message.content

def getImageResponse():
    response = openai.chat.completions.create(model="gpt-4o", messages=[
            {"role": "system", "content": "You are identifying organisms."},
            {
                "role": "user",
                "content": [
            {"type": "text", "text": "What is the creature in this image in the format 'name; scientific name'"},
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/png;base64,{b64Image}",  
                "detail": "low"
              },
            },
          ],
            }
        ])
    return response.choices[0].message.content


def encode(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
    
def openImageFile():
    file = filedialog.askopenfilename(filetypes=[("Allowed Types", "*.png *.jpeg *.jpg *.ppm *.pnm *.gif")], title="Import an image into SciFinder")
    print(file)
    if not (file == None or (len(file) < 4 or "." not in file)):
        packImage(file)
        window.destroy()
        renderFrame(file)

def packImage(imgFile):
    im = Image.open(imgFile)

    if (not ("/" in imgFile) or ("\\" in imgFile)):
        imgNewFilename = imgFile
    else:
        print("Changing filename")
        idx = 0
        for i in range(len(imgFile)):
            if imgFile[i] == "/" or imgFile[i] == "\\":
                idx = i

        imgNewFilename = imgFile[idx + 1:]

    
    im.save(imgNewFilename)
    imageFile = imgNewFilename
    validTypes = ["gif", "png"]

    imageName = imageFile[:imageFile.index(".")]
    imageType = imageFile[imageFile.index(".") + 1:]

    #print("Image type of " + imageFile + ": " + imageType)

    img = Image.open(imageFile)
    if not imageType in validTypes:
        img.save(imageName + ".png")
        imageFile = imageName + ".png"

    OG_IMAGE = ImageTk.PhotoImage(Image.open(imageFile))

    if OG_IMAGE.height() > 250 or OG_IMAGE.width() > WINDOW_WIDTH - 100:
        resized = True
        newWidth = OG_IMAGE.width()
        newHeight = OG_IMAGE.height()
        if newWidth > WINDOW_WIDTH - 100:
            newHeight = (WINDOW_WIDTH - 100)/newWidth * newHeight
            newWidth = WINDOW_WIDTH - 100
        if newHeight > 250:
            newWidth = 250/newHeight * newWidth
            newHeight = 250

        img.save("RESIZED" + imageFile)
        img = Image.open("RESIZED" + imageFile)
        img = img.resize(size=(int(newWidth), int(newHeight)))
        RESIZED_IMAGE = ImageTk.PhotoImage(img)

    global IMAGE
    global filename

    if resized:
        IMAGE = RESIZED_IMAGE
        filename = "RESIZED" + imageFile
    else:
        IMAGE = OG_IMAGE
        filename = imageFile

    global b64Image
    b64Image = encode(filename)
    #print(b64Image)

    imageLabel = ctk.CTkLabel(window, text="", image=CTkImage(img, size=(IMAGE.width(), IMAGE.height())).create_scaled_photo_image(widget_scaling=1, appearance_mode="dark"), fg_color="#8EABE6", width=IMAGE.width()+30, height=IMAGE.height()+30, corner_radius=15)
    imageLabel.pack()

def renderFrame(fl):
    global window
    window = ctk.CTkFrame(root)
    window.configure(fg_color = "#292930")
    window.pack()

    set_default_color_theme("blue")

    
    sciFinderLabel = ctk.CTkLabel(window, text= "SciFinder", font=("Britannic Bold", 50), bg_color = "transparent", text_color = "#8EABE6", width= 500, height = 80)
    sciFinderLabel.pack()
    
    uploadButton = ctk.CTkButton(window, text="Upload Image", font=("Bahnschrift", 30), bg_color = "transparent", hover_color="#FFFFFF", fg_color = "transparent", text_color="#8EABE6", border_color= "#8EABE6", border_width=2, corner_radius=100, width= 250, height =80, command=openImageFile)
    uploadButton.pack()

    paddingLabel = ctk.CTkLabel(window, text="", bg_color="transparent", fg_color="transparent", height = 20)
    paddingLabel.pack()
    
    packImage(fl)

    paddingLabel2 = ctk.CTkLabel(window, text="", bg_color="transparent", fg_color="transparent", height = 20)
    paddingLabel2.pack()
    
    button = ctk.CTkButton(window, text="Identify!", text_color="#292930",font=("Bahnschrift", 20), bg_color="transparent", hover_color="#FFFFFF", fg_color="#8EABE6", command=identify, width = 120, height = 40, corner_radius= 100)
    button.pack()

def startup():
    height = 30
    while height < WINDOW_HEIGHT:
        height += WINDOW_HEIGHT/50
        root.geometry(str(WINDOW_WIDTH) + "x" + str(int(height)))
        sleep(0.001)
        root.update()

def chooseSampleImage():
    directory = "SampleImages"

    validSamples = []
    for fln in os.listdir(directory):
        path = os.path.join(directory, fln)
        if os.path.isfile(path):
            validSamples.append(path)

    chosenSample = validSamples[randint(0, len(validSamples) - 1)]
    shutil.copy(chosenSample, r"C:\Users\sonja\Desktop\SciFinder")
    chosenSample = chosenSample[chosenSample.index("\\") + 1:]
    return chosenSample

def clearFiles():
    directory = r"C:\Users\sonja\Desktop\SciFinder"

    for fln in os.listdir(directory):
        path = os.path.join(directory, fln)
        if os.path.isfile(path):
            if not path.endswith((".py", ".txt", "bgimage.png")):
                os.remove(path)


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 700

root = ctk.CTk()
root.geometry(str(WINDOW_WIDTH) + "x" + str(0))
root.title("SciFinder")
root.configure(fg_color = "#292930")

clearFiles()
renderFrame(chooseSampleImage()) #change
startup()
root.mainloop()