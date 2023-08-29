import openai
import os
from PIL import Image, ImageTk
import requests
import io
from tkinter import Tk, Canvas, Button, LabelFrame, Entry, Label, StringVar, OptionMenu, Radiobutton
import tkinter

def generate():
    #Get api key from environment variables
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    #Setting description to be sent to DALLE2
    imageDescription = descriptionEntry.get() + " in a " + clicked.get() + " style in " + dim.get()

    #Generating the image
    response = openai.Image.create(
        prompt = imageDescription,
        n = 1,
        size = '512x512'
    )

    #Storing the image
    image_url = response['data'][0]['url']
    response = requests.get(image_url)

    #Creating the image object and placing it on the canvas
    image = ImageTk.PhotoImage(Image.open(io.BytesIO(response.content)))
    canvas.image = image
    canvas.create_image(0, 0, anchor="nw", image=image)

#Creating root window
root = Tk()
root.title("Image Generator")
root['bg'] = '#242526'
root['border'] = 10

#Creating the frame for all the options/prompts to be placed onto
frame = LabelFrame(root, padx=5, pady=5, background="#E4E6EB")
frame.pack(pady = 10)

#Creating the image description entry box
descriptionLabel = Label(frame, text = "Image Description: ", bg = "#E4E6EB")
descriptionEntry = Entry(frame)
descriptionLabel.grid(column = 0, row = 0, padx=10, pady=10)
descriptionEntry.grid(column = 1, row = 0, padx=10, pady=10)

#Creating the style option
styleLabel = Label(frame, text = "Style: ", bg='#E4E6EB')
clicked = StringVar()
clicked.set("Realistic")
options = ["Realistic", "Steampunk", "Cartoon"]
styleDropDown = OptionMenu(frame, clicked, *options)
styleLabel.grid(row=1, column = 0, padx=10, pady=10)
styleDropDown.grid(row=1, column=1, padx=10, pady=10)

#Creating the dimension option
dimensionLabel = Label(frame, text = 'Dimension Count: ', bg = '#E4E6EB')
dim = StringVar()
dim.set("3D")
twoDButton = Radiobutton(frame, text = '2D', variable = dim, value = "2D", bg = '#E4E6EB')
threeDButton = Radiobutton(frame, text = '3D', variable = dim, value = "3D", bg = '#E4E6EB')
dimensionLabel.grid(row = 3, column = 0)
twoDButton.grid(row = 4, column = 1)
threeDButton.grid(row = 3, column = 1)

#Creating the generate button
generateButton = Button(frame, text = "Generate", command = generate)
generateButton.grid(row = 5, column = 0, columnspan = 2, sticky="news", padx=10, pady=10)

#Creating the canvas for the image to be placed on
canvas = tkinter.Canvas(root, width = 512, height = 512, background="#3A3B3C")
canvas.pack()

#Loop to constantly update the GUI
root.mainloop()