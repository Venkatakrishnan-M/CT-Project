from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
from pymongo import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


connString = "mongodb+srv://admin:8569VkMk$2001@myfirstdb.rpjfd2i.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connString)

# ============================================================================================================
#   Root Frame creation
# ============================================================================================================

root = tk.Tk()
root.title("Restaurant & Snack bar Recommender")
root.iconbitmap(R"C:\Users\venka\Desktop\shop.ico")
root.config(background="#008ae6")
root.geometry("1500x750")


def plotDisplay():
    global canvas
    temp = clicked.get()
    cursor = collection.find({"Location": temp})

    df = pd.DataFrame(list(cursor))
    abc, ax = plt.subplots()
    plt.scatter(df['dineRating'], df['priceFor2'])
    plt.xlabel('dineRating')
    plt.ylabel('priceFor2')
    plt.title('Scatter Plot of Rating vs Average Cost')
    fig = plt.gcf()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=3, column=3, padx=50)


# ==============================================================================================================
#   Function to Create and Configure Listbox and Scroll Bar
# ==============================================================================================================


def create():
    global listbox
    global scrollbar
    listbox = tk.Listbox(root, width=60, height=20)
    scrollbar = tk.Scrollbar(root, orient="vertical")
    scrollbarx = tk.Scrollbar(root, orient="horizontal")
    listbox.config(yscrollcommand=scrollbar.set, xscrollcommand=scrollbarx.set, font=(
        "Bahnschrift SemiBold SemiConden", 15))
    scrollbarx.config(command=listbox.xview)
    scrollbar.config(command=listbox.yview)
    listbox.grid(row=3, column=2, sticky="nsew")
    scrollbar.grid(row=3, column=0, sticky="ns")
    scrollbarx.grid(row=4, column=2, sticky="we", padx=25, pady=20)

# ============================================================================================================
#   Function to do process when search button is clicked
# ============================================================================================================


def analyse():

    global count
    count = 0
    flag = 0
    temp = clicked.get()
    query = {"Location": temp}
    documents = collection.find(query)
    cursor = pd.DataFrame(list(documents))
    cursor = cursor.sort_values(
        by=["dineRating", "priceFor2"], ascending=[False, True])

    correlation = cursor[['dineRating', 'priceFor2']].corr()
    value = correlation.loc['dineRating', 'priceFor2']

    if str(value) > str(0.2):
        flag = 1
        listbox.insert(tk.END, "Results based on analysis b/w rating & Price")
        listbox.insert(tk.END, " ")
        for index, row in cursor.iterrows():
            if (row.dineRating >= 3.5 and row.priceFor2 <= 550 and row.priceFor2 >= 200):
                listbox.insert(tk.END, "Restaurant Name: " +
                               str(row.restaurantName))
                listbox.insert(tk.END, "Address: "+str(row.Address))
                listbox.insert(tk.END, "Rating: "+str(row.dineRating))
                listbox.insert(tk.END, "Price For 2: "+str(row.priceFor2))
                listbox.insert(tk.END, " ")
                count = count+1

    if (count < 7):
        location = clicked.get()
        data = list(collection.find({"Location": location}))
        df = pd.DataFrame(data)
        inter = df.explode("Cuisine")
        dishes = inter.groupby(['Cuisine']).size().sort_values(ascending=False)

        if (flag == 0):
            listbox.insert(
                tk.END, "Results based on Popular dish in {}".format(location))
        else:
            listbox.insert(
                tk.END, "Additional results based on Popular dish in {}".format(location))
        # listbox.insert(
            # tk.END, "Three Most popular dish in {} are {}".format(location, dishes.iloc[0:0, 0:3]))
        listbox.insert(tk.END, " ")
        for index, row, in df.iterrows():
            if (((dishes.index[:3]) & row['Cuisine']).any()):
                listbox.insert(tk.END, "Restaurant Name: " +
                               str(row.restaurantName))
                listbox.insert(tk.END, "Address: "+str(row.Address))
                listbox.insert(tk.END, "Rating: "+str(row.dineRating))
                listbox.insert(tk.END, "Price For 2: "+str(row.priceFor2))
                listbox.insert(tk.END, " ")


# ============================================================================================================
#   Function to do process when search button is clicked
# ============================================================================================================


def onClick():

    global db
    global collection

    db = client.Project
    collection = db.dummy

    create()
    analyse()
    plotDisplay()


# ============================================================================================================
#   Drop Box Creation
# =============================================================================================================

locations = [
    "Abhiramapuram", "Adambakkam", "Adyar", "Akkarai", "Alandur", "Alwarpet", "Ambattur", "Aminijikarai", "Anna Nagar", "Anna Salai", "Arumbakkam", "Ashok Nagar", "Avadi", "Besant Nagar", "Chengalpattu", "Chetpet", "Choolaimedu", "Chromepet", "ECR", "Egatoor", "Egmore", "Ekkaduthangal", "GST Road", "George Town", "Gopalapuram", "Guindy", "Injambakkam", "K.K. Nagar", "Kanathur", "Kanchipuram", "Karapakkam", "Kelambakkam", "Kilpauk", "Kodambakkam", "Kolathur", "Kottivakkam", "Kotturpuram", "Kovalam", "Koyambedu", "MRC Nagar", "Madhavaram", "Madipakkam", "Maduravoyal", "Mahabalipuram", "Mandaveli", "Medavakkam", "Meenambakkam", "Mogappair", "Muttukadu", "Mylapore", "Nandanam", "Nanganallur", "Navallur", "Neelangarai", "Nungambakkam", "OMR", "Okkiyampet", "Oragadam", "Padur", "Palavakkam", "Pallavaram", "Pallikaranai", "Park Town", "Parrys", "Perambur", "Perungudi", "Poonamalle", "Porur", "Potheri", "Purasavakkam", "RA Puram", "RK Salai", "Ramapuram", "Red Hills", "Royapettah", "Royapuram", "Saidapet", "Saligramam", "Santhome", "Selaiyur", "Semmancheri", "Shenoy Nagar", "Sholinganallur", "Sipcot", "Somerset Greenways", "Sowcarpet", "Sriperumbudur", "St. Thomas Mount", "T. Nagar", "Tambaram", "Taramani", "Teynampet", "Thiruvallur", "Thiruvanmiyur", "Thuraipakkam", "Tiruvottiyur", "Triplicane", "Vadapalani", "Valasaravakkam", "Vandalur", "Velachery", "Vepery", "Vettuvankeni", "Virugambakkam", "Washermenpet", "West Mambalam"
]

global clicked
clicked = tk.StringVar()
clicked.set("Select location")

label = tk.Label(root, text="Prototype", background="#008ae6")
label.config(font=('Helvetica bold', 15))
label.grid(row=0, column=0)

dropbox = ttk.Combobox(root, textvariable=clicked, values=locations)
dropbox.config(width=30, font="Arial")
dropbox.grid(row=1, column=2, padx=50)


# ============================================================================================================
#   Search Button Creation
# ============================================================================================================


button = tk.Button(root, text="Search", font="Arial", command=onClick)
button.grid(row=1, column=3, pady=20, padx=20)

root.mainloop()
