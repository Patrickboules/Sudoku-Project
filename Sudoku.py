#Importing the necessary libraries
from customtkinter import *
from CTkMessagebox import *
from PIL import Image,ImageTk

def main():
    #Declaring the user's name as a global variable
    global frame
    global finale
    global numbar
    global player_name
    global buttons
    global quitb

    #Function that occurs for a new player
    def new_p(root,intro,bar,npb,opb,rbtn,subbtn,intbar,frame,qbtn):
        #Displaying and unshowing widgets
        bar.grid(row = 2, column =1)
        npb.grid_forget()
        opb.grid_forget()
        rbtn.grid(row = 3, column = 1)
    
        #Updating the buttons' commands
        rbtn.configure(command=lambda:r_back(npb,opb,rbtn,bar))
        subbtn.configure(command=lambda:submit_new(root,intro,bar,npb,opb,rbtn,subbtn,intbar,frame,qbtn))
        
    #Function that occurs for an old player
    def old_p(root,intro,menu,npb,opb,rbtn,subbtn,intbar,frame,qbtn):
        #Displaying and unshowing widgets
        menu.grid(row = 5, column = 1)
        npb.grid_forget()
        opb.grid_forget()
        rbtn.grid(row = 4, column = 1)
    
        #Updating the buttons' commands    
        rbtn.configure(command=lambda:r_back(npb,opb,rbtn,menu))
        subbtn.configure(command=lambda:submit_old(root,intro,menu,npb,opb,rbtn,subbtn,intbar,frame,qbtn))

    #Adding the new player and printing the grid
    def submit_new(root,intro,bar,npb,opb,rbtn,subbtn,intbar,frame,qbtn):
        #Taking the player's name as a variable
        global player_name
        player_name = bar.get()
        
        #Reading the Sudoku from a file and making a list
        with open('sudoku.txt', 'r') as f:
            sudoku_contents = f.read()
            sudoku_contents = sudoku_contents.replace("\n","")
            sudoku_list = list(sudoku_contents)
    
        #Making sure the new user's name is not duplicated
        if player_name != "":
            with open("players.txt","a+") as a_plyer:
                a_plyer.seek(0)
                plist =[line.rstrip("\n") for line in a_plyer]
                if player_name.lower() in plist:
                     CTkMessagebox(title="Error", message="Username Taken", icon="cancel")
                else:
                    #Destroying the unwanted widgets then printing the grid
                    intro.destroy()
                    bar.destroy()
                    npb.destroy()
                    opb.destroy()
                    rbtn.destroy()
                    subbtn.destroy()
            
                    #The print_grid function takes the list as a parameter
                    print_grid(intbar,frame,sudoku_list,qbtn)
            
                    #Updating the button's command 
                    qbtn.configure(command = lambda:end_game(root,player_name))
        else:
            CTkMessagebox(title="Error", message="Username Invalid", icon="cancel")

    #Loading progress of pervious player and printing the grid
    def submit_old(root,intro,menu,npb,opb,rbtn,subbtn,intbar,frame,qbtn):
        #Taking the player's name as a variable
        global player_name
        player_name = menu.get()
        #Checking if the file exists
        try:
            #Loading the saved progress
            f = f"{player_name}.txt"
            with open(f,"r") as old_file:
                nums = list(old_file.read())
                #Destroying the unwanted widgets then printing the grid
                intro.destroy()
                menu.destroy()
                npb.destroy()
                opb.destroy()
                rbtn.destroy()
                subbtn.destroy()
        
                #Printing the grid
                print_grid(intbar,frame,nums,qbtn)
        
                #Updating the button's command
                qbtn.configure(command = lambda:end_game(root,player_name))
        except FileNotFoundError:
            CTkMessagebox(title="Error", message="Choose a Correct File", icon="cancel")
    #Printing the buttons
    def print_grid(entry,frame,lst,qbtn):
        global buttons
    
        #reading the main Sudoku list 
        with open('sudoku.txt', 'r') as f:
            sudoku_contents = f.read()
            sudoku_contents = sudoku_contents.replace("\n","")
            sudoku_list = list(sudoku_contents)
            
        #Displaying widgets 
        entry.grid(row = 0, column = 1)
        frame.grid(row = 1, column = 1)
        qbtn.grid(row = 2, column = 1)
    
        #Tuple full of acceptable values
        nums = ("1","2","3","4","5","6","7","8","9")
    
        #Making a dictionary for the buttons and its values
        buttons = {}
    
        #Variable for iteration
        i = 0
        #Loops for the position of the buttons
        for row in range(1,10):
            for box in range(1,10):
            
                #Checking if the number is 0 or not
                if lst[i] in nums:
                
                    #Comparing the user's list and the main list
                    if lst[i] == sudoku_list[i]:
                    
                        #Disabling button    
                        button = CTkButton(frame,text=f"{lst[i]}", height=75, width=75, border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=mbfont,text_color="black",state="Disable")
                    else:
                        button = CTkButton(frame,text=f"{lst[i]}", height=75, width=75, border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")
                        button.configure(command=lambda button=button: write(buttons,button,entry))
                else:
                    button = CTkButton(frame,text="", height=75, width=75, border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")
                    #Updating the buttons to be edited
                    button.configure(command=lambda button=button: write(buttons,button,entry))
            
                #Appending the buttons and its value to the dictionary
                buttons[button] = lst[i]
                button.grid(column=box, row=row, padx=0, pady=0)
                i+=1

    #Return to Main Menu 
    def r_back(npb,opb,rbtn,wid):
        #Destroying and displaying the widgets
        npb.grid(row=2,column =1)
        opb.grid(row=3,column =1)
        rbtn.grid_forget()
        wid.grid_forget()
    
    #Saving progress
    def end_game(root,name):
        global buttons
        name = name.lower()
        with open("players.txt","a+") as a_plyer:
            a_plyer.seek(0)
            players =[]
            for line in a_plyer:
                players.append(line.rstrip("\n"))
            if name not in players:
                a_plyer.write("\n" + name)
        #Making a list of values of the dictionary
        nums = list(buttons.values())
    
        #Opening the user's file and writing the list
        with open(f"{name}.txt","w") as wr_plyers:
            for i in range(len(nums)):
                wr_plyers.write(nums[i])       
    
        #Closing the room
        root.destroy()

    #Ending the game
    def end():
        #Declaring global variables
        global frame
        global finale
        global numbar
        global player_name
        global buttons
        global quitb
    
        #Reading the main Sudoku list
        with open('sudoku.txt', 'r') as f:
            sudoku_contents = f.read()
            sudoku_contents = sudoku_contents.replace("\n","")
            sudoku_list = list(sudoku_contents)
    
        #Rewriting the player's progress to be the main list
        with open(f"{player_name}.txt","w") as wr_plyers:
            for i in range(len(sudoku_list)):
                wr_plyers.write(sudoku_list[i])       
    
        #Displaying the Finale label
        frame.destroy()
        numbar.destroy()
        quitb.destroy()
        finale.grid(row = 0, column = 1)
   
    #Checking values of the rows
    def check_row(klst,vlst,num,btn):
        #Declaring Variables
        index = 0
        strng = str(num)
        results = []
    
        #Iterating over every list and checking is the number is in it
        for i in range(9):
            if strng in vlst[i]:
                val = "0"
            else: 
                val = strng
            results.append(val)
    
        #Searching for the position of the button
        for i in range(9):
            if btn in klst[i]:
                index = i
                break
        
        #Identifing the value corresponding the button's position
        if results[index] == "0":
            flag = False
        else:
            flag = True
        return flag

    #Checking values of column    
    def check_column(klst,vlst,num,btn):
        #Declaring Variables
        index = 0
        #Making a list of the columns for the buttons and values
        new_matrix = [vlst[i:len(vlst):9] for i in range(9)]
        new_keys_matrix = [klst[i:len(klst):9] for i in range(9)]
        results = []
    
        #Iterating over every list and checking is the number is in it
        for column in range(9):
            if str(num) in new_matrix[column]:
                val = "0"
            else:
                val = str(num)
            results.append(val)
    
        #Searching for the position of the button    
        for i in range(9):
            if btn in new_keys_matrix[i]:
                index = i
                break
    
        #Identifing the value corresponding the button's position
        if results[index] == "0":
            flag = False
        else:
            flag = True
        return flag

    #Checking values of boxes
    def check_box(klst,vlst,num,button):
        #Declaring Variables
        index = 0
        boxes_btns_matrix = []
        boxes_values_matrix = []
        inner_values = []
        inner_buttons = []
    
        #Iterating over 3 rows
        for group in range(0,8,3):
            #Iterating over each box in the row
            for box in range(0,8,3):
                v = []
                btn = []
                #Iterating over each row
                for row in range(3):
                    #Iterating over each column 
                    for column in range(3):
                        x = vlst[row+group][column+box]
                        j = klst[row+group][column+box]
                        inner_values.append(x)
                        inner_buttons.append(j)
                    v += inner_values
                    btn += inner_buttons
                    inner_values = []
                    inner_buttons = []
                boxes_values_matrix.append(v)
                boxes_btns_matrix.append(btn)
        results = []
    
        #Iterating over every list and checking is the number is in it
        for i in range(9):
            if str(num) in boxes_values_matrix[i]:
                val = "0"
            else:
                val = str(num)
            results.append(val)
        
        #Searching for the position of the button
        for i in range(9):
            if button in boxes_btns_matrix[i]:
                index = i
                break
        
        #Identifing the value corresponding the button's position
        if results[index] == "0":
            flag = False
        else:
            flag = True
        return flag
  
    #Writing the number in the box
    def write(buttons,button,bar):
        #Declaring Variables
        number = 0
        dict_values = list(buttons.values())
        dict_buttons = list(buttons.keys())
        keys_list = []
        values_list = []
    
        #Making the dictionary items into 2D lists
        for i in range(9):
            lk = dict_buttons[9*i:9*(i+1)]
            lv = dict_values[9*i:9*(i+1)]
            values_list.append(lv)
            keys_list.append(lk)
        
        #Checking if the input is an integer
        try:
            number = int(bar.get())
        except ValueError:
            CTkMessagebox(title="Error", message="Not A Number", icon="warning")
        else:
            if number < 10 and number > 0:
                #Checking the validity of the number
                checkr = check_row(keys_list,values_list,number,button)
                checkc = check_column(dict_buttons,dict_values,number,button)
                checkb = check_box(keys_list,values_list,number,button)
                if checkr == False or checkc == False or checkb == False: 
                    CTkMessagebox(title="Error", message="TRY ANOTHER BOX!", icon="warning")
                else:
                    button.configure(text = str(number),font=bfont)
                    buttons[button] = str(number)     
            else:
                CTkMessagebox(title="Error", message="INCORRECT NUMBER!", icon="warning")
        
        
        #Ending the Game
        final = list(buttons.values())
        if "0" not in final:
            end()

    #Creating the main window
    root = CTk(fg_color="#E4E4DA")
    frame = CTkFrame(root)

    #Making list of pervious players
    PLAYER_NAMES = []
    with open("players.txt","r") as r_plyers:
        for line in r_plyers:
            line = line.rstrip("\n")
            PLAYER_NAMES.append(line)
       
    #Creating fonts
    ifont = CTkFont(family="Verdana", size=50)
    mbfont = CTkFont(family="Verdana", size=20, weight = "bold")
    bfont = CTkFont(family="Verdana", size=20)

    #Creating images
    intro_image = CTkImage(light_image=Image.open("WS.png"),size=(699,200))
    finale_image = CTkImage(light_image=Image.open("Congrats.png"),size=(699,200))
    #Creating Labels
    intro = CTkLabel(root,fg_color="#E4E4DA", image=intro_image,text="")
    finale = CTkLabel(root,fg_color="#E4E4DA",image=finale_image,text="")

    #Creating Buttons
    new_player = CTkButton(root,text ="New Player",width = 224,border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")
    old_player = CTkButton(root,text = "Pervious Player",width = 224,border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")
    submit_player = CTkButton(root,text = "Start",width = 224,border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")
    returnb = CTkButton(root,text = "Return to Main Menu", width = 224,border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")
    quitb = CTkButton(root,text="Save & Quit", width = 224,border_color="black", corner_radius=0, border_width=5, fg_color="#E4E4DA",font=bfont,text_color="black")

    #Creating Entries
    numbar = CTkEntry(root,width=430,placeholder_text="Enter a Number")
    namebar = CTkEntry(root,width=224,placeholder_text="Enter Your Name")

    #Creating a Combobox
    nameboxes = CTkComboBox(root, values=PLAYER_NAMES,)
    nameboxes.set("Choose Player")
   
    #Updating buttons' commands
    new_player.configure(command=lambda:new_p(root,intro,namebar,new_player,old_player,returnb,submit_player,numbar,frame,quitb))
    old_player.configure(command=lambda:old_p(root,intro,nameboxes,new_player,old_player,returnb,submit_player,numbar,frame,quitb))

    #Displaying widgets
    intro.grid(row = 0, column = 1)
    submit_player.grid(row = 6, column = 1)
    new_player.grid(row = 1, column = 1)
    old_player.grid(row = 3, column = 1)
    root.mainloop()
    
main()