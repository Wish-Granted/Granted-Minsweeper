from tkinterhelper import *
from google_sheets_intergration_minesweeper import *
import os
import time
import random
from PIL import Image, ImageTk

SCRIPT_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
default_font: str = "Consolas"
DIFFICULTIES: list[str] = ["    Easy    ", "   Medium   ", "    Hard    ", " Impossible "]
BOARD_SETUPS = ((10, (10,8)), (40,(18,14)), (99,(24,20)), (99, (10,10)))
first_launch = True
first_square_revealed: bool
after_id = None
username: str = ""

def do_LoadImages() -> None:
    global assets
    assets = {"buttons": {}, "other": {}, "tiles": {}, "timer": {}}

    ASSET_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "assets")
    for folder in os.listdir(ASSET_DIRECTORY):
        FOLDER_DIRECTORY = os.path.join(ASSET_DIRECTORY, folder)
        for asset in os.listdir(FOLDER_DIRECTORY):
            asset_path: str = os.path.join(FOLDER_DIRECTORY, asset)
            asset_image = Image.open(asset_path)
            asset_imagetk = ImageTk.PhotoImage(asset_image)
            if asset == "sunglasses.png":
                assets[folder].update({asset[:len(asset)-4]: [asset_imagetk]})
                for rotation in range(int(360/20)):
                    asset_image = Image.open(asset_path).rotate(20*-(rotation+1), expand=True)
                    asset_imagetk = ImageTk.PhotoImage(asset_image)
                    assets["other"]["sunglasses"].append(asset_imagetk)
            else:
                assets[folder].update({asset[:len(asset)-4]: asset_imagetk})

def do_Button_Animation(frame: Frame, button: Label, button_pressed: Label, press: bool) -> None:
    if press:
        button.place_forget()
        button_pressed.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        button_pressed.place_forget()
        button.place(relx=0.5, rely=0.5, anchor=CENTER)

def do_Closing_Animation(main_frame: Frame, on_finish=lambda: None) -> None:
    widgets: list[Widget] = main_frame.winfo_children()
    def do_Destroy_Next_Widget(index=0):
        if index < len(widgets):
            widgets[index].destroy()
            do_Destroy_Next_Widget(index+1)            
        else:
            on_finish()
    do_Destroy_Next_Widget()

def do_return_to_menu(root: Tk, main_frame: Frame) -> None:
    userinput = messagebox.askquestion("Return to menu?", "Do you wish to return to the main menu?")
    if userinput == "yes":
        root.unbind("<Key-Escape>")
        do_Closing_Animation(main_frame)
        run_Welcome(root, main_frame)

def run_Welcome(root = None, frame_Window = None) -> None:   
    global spin, first_launch
    if first_launch == True:
        root: Tk = Tk()
        do_LoadImages()

        root.wm_iconphoto(False, assets["other"]["app_icon"])
        root.title("MinesweeperGranted")

        frame_Window = Frame(root, bg="#f0f0f0", border=0, relief=SOLID)
        frame_Window.pack(expand=True, fill="both")

        first_launch = False

    WINDOW_DIMENSIONS: tuple = (500, 425)

    root.geometry(f"{WINDOW_DIMENSIONS[0]}x{WINDOW_DIMENSIONS[1]}+{(root.winfo_screenwidth()//2)-(WINDOW_DIMENSIONS[0]//2)}+{(root.winfo_screenheight()//2)-(WINDOW_DIMENSIONS[1]//2)}")    
    root.wm_minsize(width=WINDOW_DIMENSIONS[0], height=WINDOW_DIMENSIONS[1])
    root.wm_maxsize(width=WINDOW_DIMENSIONS[0], height=WINDOW_DIMENSIONS[1])

    canvas_Title: Canvas = Canvas(frame_Window, width=149, height=57, bg=None)
    canvas_Title.create_text(5, 20, text="GRANTED", fill="black", font=(default_font, 8, "bold"), anchor="w")
    canvas_Title.create_text(149/2, 33/2+20, text="Minesweeper", fill="black", font=(default_font, 18, "bold"), anchor="center")

    image_Sunglasses = canvas_Title.create_image(127, 20, image=assets["other"]["sunglasses"][0], anchor="center")
    t=0
    def spin_frame() -> None:
        nonlocal t, image_Sunglasses
        if t < 18:
            canvas_Title.delete(image_Sunglasses)
            image_Sunglasses = canvas_Title.create_image(127, 20, image=assets["other"]["sunglasses"][t], anchor="center")
            t += 1
            root.after(10, spin_frame)
        else:
            t = 0
            canvas_Title.delete(image_Sunglasses)
            image_Sunglasses = canvas_Title.create_image(127, 20, image=assets["other"]["sunglasses"][0], anchor="center")
            canvas_Title.tag_bind(image_Sunglasses, "<Button-1>", spin)
    def spin(_):
        nonlocal t
        spin_frame()
    canvas_Title.tag_bind(image_Sunglasses, "<Button-1>", spin)


    logo_Menu: Label = Label(frame_Window, image=assets["other"]["app_icon"])

    def do_Prepare_Game(on_closing=lambda:None):
        root.bind("<Key-Escape>", func=lambda event: do_return_to_menu(root, frame_Window))
        do_Closing_Animation(main_frame=frame_Window)


        user_input_var: StringVar = StringVar()
        user_input_var.set("Anonymous")

        def validate_input(new_value):
            return len(new_value) <= 20

        vcmd = (root.register(validate_input), '%P')

        frame_input: Frame = Frame(frame_Window)
        frame_input.place(relx=0.5, rely=0.448, anchor=CENTER)
        label_text_prompt: Label = Label(frame_input, text="Enter name for highscores", font=(default_font, 9))
        label_text_prompt.pack(pady=(0,5))
        frame_text_done: Frame = Frame(frame_input)
        frame_text_done.pack()
        text_input: Entry = Entry(frame_text_done, width=20, textvariable=user_input_var, validate="key", validatecommand=vcmd)
        text_input.pack(side="left", padx=(23,0))
        done_button: Label = Label(frame_text_done, text=" done ", font=(default_font, 8), relief=RAISED)
        done_button.pack(side="right", padx=(2,23))

        def set_username_difficulty():
            global username
            nonlocal Difficulty
            username = user_input_var.get()
            Difficulty = DIFFICULTIES.index(optionmenu_User_Input.get())

        done_button.bind("<ButtonPress-1>", lambda events: set_username_difficulty())
        done_button.bind("<ButtonRelease-1>", on_closing)
        text_input.bind("<KeyPress-Return>", lambda events: set_username_difficulty())
        text_input.bind("<KeyRelease-Return>", on_closing)
        text_input.focus_set()
        text_input.icursor(END)

        label_text_difficulty: Label = Label(frame_input, text="Select Difficulty", font=(default_font, 9))
        label_text_difficulty.pack(pady=(20,3))
        optionmenu_User_Input = StringVar(root)
        optionmenu_User_Input.set("    Easy    ")
        optionmenu_Difficulty: OptionMenu = OptionMenu(frame_input, optionmenu_User_Input, *DIFFICULTIES)
        optionmenu_Difficulty.config(font=(default_font, 8))
        optionmenu_Difficulty_options: Menu = frame_input.nametowidget(optionmenu_Difficulty.menuname)
        optionmenu_Difficulty_options.config(font=(default_font, 8))
        optionmenu_Difficulty.pack()

        label_text_escape: Label = Label(frame_input, text="Press \"ESC\" to return to the menu at any time", font=(default_font, 10))
        label_text_escape.pack(pady=(40,0))

    Difficulty = 0
    button_Menu_Singleplayer: Button = Button(frame_Window, command=lambda:[do_Prepare_Game(on_closing=lambda events:[do_Closing_Animation(main_frame=frame_Window), run_Singleplayer(root, Difficulty, frame_Window)], )], text="  Singleplayer  ", font=(default_font, 10))

    def do_Prepare_Other(on_closing=lambda:None):
        root.bind("<Key-Escape>", func=lambda event: do_return_to_menu(root, frame_Window))
        do_Closing_Animation(main_frame=frame_Window, on_finish=on_closing)

    button_Menu_Highscores: Button = Button(frame_Window, command=lambda:[do_Prepare_Other(on_closing=lambda:[run_highscores(root, frame_Window)])],text="  Highscores  ", font=(default_font, 10))

    button_Menu_Settings: Button = Button(frame_Window, command=lambda:[do_Prepare_Other(on_closing=lambda:[run_settings(root, frame_Window)])], text="  Settings  ", font=(default_font, 10))

    canvas_Title.place(relx=0.5, rely=0.23, anchor=CENTER)

    logo_Menu.place(relx=0.5, rely=0.4, anchor=CENTER)
    button_Menu_Singleplayer.place(relx=0.5, rely=0.55, anchor=CENTER)
    button_Menu_Highscores.place(relx=0.5, rely=0.675, anchor=CENTER)
    button_Menu_Settings.place(relx=0.5, rely=0.8, anchor=CENTER)

    root.mainloop()

def do_Generate_New_Board(DIFFICULTY) -> list:
    minesweeper_layout = []
    temp_layout: list[str] = ["X"] * BOARD_SETUPS[DIFFICULTY][0] + ["O"] * (BOARD_SETUPS[DIFFICULTY][1][1] * BOARD_SETUPS[DIFFICULTY][1][0] - BOARD_SETUPS[DIFFICULTY][0])
    random.shuffle(temp_layout)
    for y_grid in range(BOARD_SETUPS[DIFFICULTY][1][1]):
        minesweeper_layout.append([])
        minesweeper_layout[y_grid] += temp_layout[0+BOARD_SETUPS[DIFFICULTY][1][0]*y_grid:BOARD_SETUPS[DIFFICULTY][1][0]+BOARD_SETUPS[DIFFICULTY][1][0]*y_grid]        

    number_layout: list[list[str]] = []
    for y_pos, row in enumerate(minesweeper_layout):
        number_layout.append([])
        for x_pos, tile in enumerate(row):
            mines_adjacent: int = 0
            if tile == "O":
                if y_pos > 0: 
                    mines_adjacent += 1 if minesweeper_layout[y_pos-1][x_pos] == "X" else 0
                    if x_pos > 0:
                        mines_adjacent += 1 if minesweeper_layout[y_pos-1][x_pos-1] == "X" else 0
                    if x_pos < BOARD_SETUPS[DIFFICULTY][1][0]-1:
                        mines_adjacent += 1 if minesweeper_layout[y_pos-1][x_pos+1] == "X" else 0
                if y_pos < BOARD_SETUPS[DIFFICULTY][1][1]-1:
                    mines_adjacent += 1 if minesweeper_layout[y_pos+1][x_pos] == "X" else 0
                    if x_pos > 0:
                        mines_adjacent += 1 if minesweeper_layout[y_pos+1][x_pos-1] == "X" else 0
                    if x_pos < BOARD_SETUPS[DIFFICULTY][1][0]-1:
                        mines_adjacent += 1 if minesweeper_layout[y_pos+1][x_pos+1] == "X" else 0
                if x_pos > 0:
                    mines_adjacent += 1 if minesweeper_layout[y_pos][x_pos-1] == "X" else 0
                if x_pos < BOARD_SETUPS[DIFFICULTY][1][0]-1:
                    mines_adjacent += 1 if minesweeper_layout[y_pos][x_pos+1] == "X" else 0
                minesweeper_layout[y_pos][x_pos] = str(mines_adjacent)
            number_layout[y_pos].append(mines_adjacent)
    return minesweeper_layout

def run_Singleplayer(root: Tk, DIFFICULTY: str, frame_Window: Frame) -> None:  
    print(f"{username}, {DIFFICULTY}")
    time.sleep(0.1)
    minesweeper_layout: list[list[str]]
    label_mines: list[list[Label]] = []
    root.wm_minsize(0,0)

    frame_Window_Header: Frame = Frame(frame_Window, border=2, relief=RAISED)
    number_of_mines: int = BOARD_SETUPS[DIFFICULTY][0]
    canvas_Number_of_Mines: Canvas = Canvas(frame_Window_Header, width=78, height=46, bg="LightGray", borderwidth=2, relief=RAISED)

    def do_update_number_of_mines(n_of_mines: int) -> None:
        negative: bool = False
        if n_of_mines < 0:
            n_of_mines *= -1
            negative = True
        number_of_mines: list[str] = list(str(n_of_mines).zfill(3))
        n_of_mines = str(n_of_mines)
        if negative:
            temp_number_of_mines = number_of_mines
            temp_number_of_mines[2-len(n_of_mines)] = "dash" if len(n_of_mines) < 3 else number_of_mines[2-len(n_of_mines)]
            temp_number_of_mines[1-len(n_of_mines)] = "none" if len(n_of_mines) < 2 else number_of_mines[1-len(n_of_mines)]
            number_of_mines = temp_number_of_mines
        canvas_Number_of_Mines.delete("all")
        canvas_Number_of_Mines.create_image(4, 4, image=assets["timer"][number_of_mines[0]], anchor="nw") #left digit mine counter
        canvas_Number_of_Mines.create_image(56, 4, image=assets["timer"][number_of_mines[1]], anchor="ne") #middle digit mine counter
        canvas_Number_of_Mines.create_image(82, 4, image=assets["timer"][number_of_mines[2]], anchor="ne") #right digit mine counter

    do_update_number_of_mines(number_of_mines)

    frame_Game_Header = Frame(frame_Window_Header, bg="#f0f0f0", border=0, relief=SOLID, width=BOARD_SETUPS[DIFFICULTY][1][0]*16, height=48)
    frame_Game_Header.pack_propagate(False)
    image_Header_Button = Label(frame_Game_Header, image=assets["buttons"]["happy"])
    image_Header_Button_Pressed = Label(frame_Game_Header, image=assets["buttons"]["happy_pressed"])
    image_Header_Button_Pressed.place(x=1, y=1)
    image_Header_Button_Pressed.place_forget()
    image_Header_Button.bind("<ButtonPress-1>", func=lambda event:do_Button_Animation(frame_Game_Header, image_Header_Button, image_Header_Button_Pressed, True))
    image_Header_Button.bind("<ButtonRelease-1>", func=lambda event:[do_Button_Animation(frame_Game_Header, image_Header_Button, image_Header_Button_Pressed, False), do_Draw_New_Board()])

    canvas_Timer: Canvas = Canvas(frame_Window_Header, width=78, height=46, bg="LightGray", borderwidth=2, relief=RAISED)

    frame_Game: Frame = Frame(frame_Window)
    def do_Draw_New_Board() -> None:
        global first_square_revealed
        nonlocal label_mines
        first_square_revealed = False
        image_Header_Button.config(image=assets["buttons"]["happy"])
        image_Header_Button_Pressed.config(image=assets["buttons"]["happy_pressed"])
        def stop_timer():
            global after_id
            if after_id is not None:
                root.after_cancel(after_id)
                after_id = None
        stop_timer()
        game_time_elapsed: int = 0
        canvas_Timer.create_image(4, 4, image=assets["timer"]["0"], anchor="nw")
        canvas_Timer.create_image(56, 4, image=assets["timer"]["0"], anchor="ne")
        canvas_Timer.create_image(82, 4, image=assets["timer"]["0"], anchor="ne")
        
        if label_mines != []:
            for y_grid, row in enumerate(label_mines):
                for x_grid ,tile in enumerate(row):
                    tile.config(image=assets["tiles"]["undiscovered"])
                    tile.unbind("<ButtonPress-1>")
                    tile.unbind("<ButtonRelease-1>")
                    tile.unbind("<Button-3>")
                    tile.bind("<ButtonPress-1>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<ButtonPress-1>"))
                    tile.bind("<ButtonRelease-1>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<ButtonRelease-1>"))
                    tile.bind("<Button-3>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<Button-3>"))
                    tile.asset = assets["tiles"]["undiscovered"]
        else:
            for y_grid in range(BOARD_SETUPS[DIFFICULTY][1][1]):
                label_mines.append([])
                for x_grid in range(BOARD_SETUPS[DIFFICULTY][1][0]):
                    temp_label: Label = Label(frame_Game, image=assets["tiles"]["undiscovered"], borderwidth=0)
                    temp_label.grid(row=y_grid+1, column=x_grid+1)
                    temp_label.bind("<ButtonPress-1>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<ButtonPress-1>"))
                    temp_label.bind("<ButtonRelease-1>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<ButtonRelease-1>"))
                    temp_label.bind("<Button-3>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<Button-3>"))
                    temp_label.asset = assets["tiles"]["undiscovered"]
                    label_mines[y_grid].append(temp_label)
        number_of_mines = BOARD_SETUPS[DIFFICULTY][0]
        do_update_number_of_mines(number_of_mines)

        def do_Timer_Loop() -> None:
            global first_square_revealed, after_id
            nonlocal game_time_elapsed

            if not first_square_revealed:
                return

            time_str = str(game_time_elapsed).zfill(3)
            digit_hundreds = time_str[0]
            digit_tens = time_str[1]
            digit_ones = time_str[2]

            canvas_Timer.delete("all")
            canvas_Timer.create_image(4, 4, image=assets["timer"][digit_hundreds], anchor="nw")
            canvas_Timer.create_image(56, 4, image=assets["timer"][digit_tens], anchor="ne")
            canvas_Timer.create_image(82, 4, image=assets["timer"][digit_ones], anchor="ne")

            if game_time_elapsed < 999:
                game_time_elapsed += 1
                after_id = root.after(1000, do_Timer_Loop)         

        def do_process_tile_presses(event, x_position, y_position, button_pressed) -> None:
            global first_square_revealed
            nonlocal number_of_mines, DIFFICULTY, minesweeper_layout
            if button_pressed == "<Button-3>":
                if label_mines[y_position][x_position].asset == assets["tiles"]["undiscovered"]:
                    label_mines[y_position][x_position].config(image=assets["tiles"]["flagged"])
                    label_mines[y_position][x_position].asset = assets["tiles"]["flagged"]
                    label_mines[y_position][x_position].unbind("<ButtonPress-1>")
                    label_mines[y_position][x_position].unbind("<ButtonRelease-1>")
                    number_of_mines -= 1
                elif label_mines[y_position][x_position].asset == assets["tiles"]["flagged"]:
                    label_mines[y_position][x_position].config(image=assets["tiles"]["undiscovered"])
                    label_mines[y_position][x_position].asset = assets["tiles"]["undiscovered"]
                    label_mines[y_position][x_position].bind("<ButtonPress-1>", func=lambda event, x_pos=x_grid, y_pos=y_grid: do_process_tile_presses(event, x_pos, y_pos, "<ButtonPress-1>"))
                    label_mines[y_position][x_position].bind("<ButtonRelease-1>", func=lambda event, x_pos=x_position, y_pos=y_position: do_process_tile_presses(event, x_pos, y_pos, "<ButtonRelease-1>"))
                    number_of_mines += 1
                do_update_number_of_mines(number_of_mines)
            elif button_pressed == "<ButtonPress-1>":
                image_Header_Button.config(image=assets["buttons"]["shocked"])
            elif button_pressed == "<ButtonRelease-1>":
                image_Header_Button.config(image=assets["buttons"]["happy"])
                if not first_square_revealed:
                    if y_position in [BOARD_SETUPS[DIFFICULTY][1][1]//2, BOARD_SETUPS[DIFFICULTY][1][1]//2-1] and x_position in [BOARD_SETUPS[DIFFICULTY][1][0]//2, BOARD_SETUPS[DIFFICULTY][1][0]//2-1]:
                        try:
                            if elias_easter_egg:
                                pass
                        except UnboundLocalError:
                            elias_easter_egg = Label(root, text="Elias is cool", font=default_font)
                            elias_easter_egg.pack()
                            root.wm_maxsize(screen_dimensions[0], screen_dimensions[1]+29)
                    global start_time
                    start_time = time.perf_counter()
                    first_square_revealed = True
                    do_Timer_Loop()
                    minesweeper_layout = do_Generate_New_Board(DIFFICULTY)
                    while minesweeper_layout[y_position][x_position] != "0" and DIFFICULTY != 3:
                        minesweeper_layout = do_Generate_New_Board(DIFFICULTY)

                asset_tile_uncovered: ImageTk.PhotoImage = assets["tiles"][minesweeper_layout[y_position][x_position] if minesweeper_layout[y_position][x_position] != "X" else "mine_pressed"]
                label_mines[y_position][x_position].config(image=asset_tile_uncovered)
                label_mines[y_position][x_position].asset = asset_tile_uncovered
                if minesweeper_layout[y_position][x_position] == "0":
                    label_mines[y_position][x_position].unbind("<ButtonPress-1>")
                    label_mines[y_position][x_position].unbind("<ButtonRelease-1>")
                if minesweeper_layout[y_position][x_position] == "X": # LOSE CONDITION
                    stop_timer()
                    image_Header_Button.config(image=assets["buttons"]["dead"])
                    image_Header_Button_Pressed.config(image=assets["buttons"]["dead_pressed"])
                    for y_pos, row in enumerate(label_mines):
                        for x_pos, tile in enumerate(row):
                            if minesweeper_layout[y_pos][x_pos] == "X" and label_mines[y_pos][x_pos].asset != assets["tiles"]["flagged"] and (y_position, x_position) != (y_pos, x_pos):
                                tile.config(image=assets["tiles"]["mine"])
                                tile.image = assets["tiles"]["mine"]
                            elif tile.asset == assets["tiles"]["flagged"] and minesweeper_layout[y_pos][x_pos] != "X":
                                tile.config(image=assets["tiles"]["not_mine"])
                                tile.image = assets["tiles"]["not_mine"]
                            if tile.asset in [assets["tiles"]["undiscovered"], assets["tiles"]["mine_pressed"], assets["tiles"]["mine"]]:
                                tile.unbind("<ButtonPress-1>")
                                tile.unbind("<ButtonRelease-1>")
                            tile.unbind("<Button-3>")
        
                else:
                    undiscovered_tiles_remaining: list[Label] = []
                    for row in label_mines:
                        for item in row:
                            if item.asset in [assets["tiles"]["undiscovered"], assets["tiles"]["flagged"]]:
                                undiscovered_tiles_remaining.append(item)
                    if len(undiscovered_tiles_remaining) == BOARD_SETUPS[DIFFICULTY][0]: # WIN CONDITION
                        stop_timer()
                        end_time = time.perf_counter()
                        real_time_elapsed = end_time - start_time
                        print(real_time_elapsed)
                        for row in label_mines:
                            for tile in row:
                                if tile.asset in [assets["tiles"][str(n)] for n in range(1,9)]:
                                    tile.unbind("<ButtonPress-1>")
                                    tile.unbind("<ButtonRelease-1>")
                        for tile in undiscovered_tiles_remaining:
                            tile.unbind("<Button-3>")
                            if tile.asset == assets["tiles"]["undiscovered"]:
                                tile.config(image=assets["tiles"]["flagged"])
                                tile.asset = assets["tiles"]["flagged"]
                                tile.unbind("<ButtonPress-1>")
                                tile.unbind("<ButtonRelease-1>")
                                do_update_number_of_mines(0)
                        image_Header_Button.config(image=assets["buttons"]["coolbeans"])
                        image_Header_Button_Pressed.config(image=assets["buttons"]["coolbeans_pressed"])
                        submit_score(username, str(real_time_elapsed), DIFFICULTIES[DIFFICULTY].strip())

                if label_mines[y_position][x_position].asset in [assets["tiles"][str(n)] for n in range(9)]:
                    adjacent_positions: list[tuple[int]] = []
                    if y_position > 0: 
                        adjacent_positions.append((0,-1))
                        if x_position > 0:
                            adjacent_positions.append((-1,-1))
                        if x_position < BOARD_SETUPS[DIFFICULTY][1][0]-1:
                             adjacent_positions.append((1,-1))
                    if y_position < BOARD_SETUPS[DIFFICULTY][1][1]-1:
                        adjacent_positions.append((0,1))
                        if x_position > 0:
                            adjacent_positions.append((-1,1))
                        if x_position < BOARD_SETUPS[DIFFICULTY][1][0]-1:
                            adjacent_positions.append((1,1))
                    if x_position > 0:
                        adjacent_positions.append((-1,0))
                    if x_position < BOARD_SETUPS[DIFFICULTY][1][0]-1:
                        adjacent_positions.append((1,0))

                    do_chord = False
                    if label_mines[y_position][x_position].asset in [assets["tiles"][str(n)] for n in range(1,9)]:
                        number_of_adjacent_mines: int = 0
                        for displacement in adjacent_positions:
                            if label_mines[y_position+displacement[1]][x_position+displacement[0]].asset == assets["tiles"]["flagged"]:
                                number_of_adjacent_mines += 1
                        if number_of_adjacent_mines == int(minesweeper_layout[y_position][x_position]):
                            do_chord = True
                    for displacement in adjacent_positions:
                        if label_mines[y_position + displacement[1]][x_position + displacement[0]].asset == assets["tiles"]["undiscovered"]:
                            if label_mines[y_position][x_position].asset == assets["tiles"]["0"] or do_chord:
                                do_process_tile_presses("", x_position + displacement[0], y_position + displacement[1], "<ButtonRelease-1>")                       
                

    do_Draw_New_Board()

    frame_Window_Header.grid(row=0, column=0, sticky="ew")

    frame_Window_Header.columnconfigure(0, weight=1)
    frame_Window_Header.columnconfigure(1, weight=0)
    frame_Window_Header.columnconfigure(2, weight=1)
    
    canvas_Number_of_Mines.grid(row=0, column=0, padx=1, pady=1, sticky="w")

    frame_Game_Header.grid(row=0, column=1, padx=1, pady=1)
    image_Header_Button.place(relx=0.5, rely=0.5, anchor=CENTER)

    canvas_Timer.grid(row=0, column=2, padx=1, pady=1, sticky="e")  


    frame_Game.grid(row = 1, column=0)


    frame_Window_Header.columnconfigure(0, weight=1)
    frame_Window_Header.columnconfigure(1, weight=0)
    frame_Window_Header.columnconfigure(2, weight=1)

    screen_dimensions: tuple = (get_dimensions(frame_Window_Header)[0], get_dimensions(frame_Window_Header)[1]+get_dimensions(frame_Game)[1])
    root.geometry(f"{screen_dimensions[0]}x{screen_dimensions[1]}+{(root.winfo_screenwidth()//2)-(screen_dimensions[0]//2)}+{(root.winfo_screenheight()//2)-(screen_dimensions[1]//2)}")
    root.wm_minsize(screen_dimensions[0], screen_dimensions[1])
    root.wm_maxsize(screen_dimensions[0], screen_dimensions[1])

def run_highscores(root: Tk, frame_window: Frame) -> None:
    label_loading: Label = Label(frame_window, text="loading...", font=(default_font, 11))
    label_loading.pack(expand=True)
    root.update()
    current_leaderboard = get_leaderboard("easy")
    label_loading.pack_forget()
    if not current_leaderboard:
        label_failed: Label = Label(frame_window, text="internet connection failed", font=(default_font, 14), foreground="red")
        label_failed.pack(expand=True)

        button_retry: Button = Button(frame_window, text="retry?", command=lambda:do_Closing_Animation(frame_window, lambda:run_highscores(root, frame_window)), font=(default_font, 10))
        button_retry.place(relx=0.5, rely=0.6, anchor=CENTER)
    else:
        label_title: Label = Label(frame_window, text="Highscores", font=(default_font, 18))
        label_return_to_menu: Label = Label(frame_window, text="Press \"ESC\" to return to the menu", font=(default_font, 10))
        label_return_to_menu.place(relx=0.5, rely=0.8, anchor=CENTER)
        frame_highscore_main: Frame = Frame(frame_window)

        frame_highscore_list: Frame = Frame(frame_highscore_main)
        label_loading.master = frame_highscore_list
    
        listbox_highscores: Listbox = Listbox(frame_highscore_list, height=10, width=40, font=(default_font, 9))
        for positon, item in enumerate(current_leaderboard, 1):
            listbox_highscores.insert(END, f"{positon}.{" " if positon < 10 else ""} {item.get("name")}{" "*(29-len(item.get("name"))+7-len(str(f"{(item.get("time") if item.get("time") < 1000 else 999.999):.3f}")))}{(item.get("time") if item.get("time") < 1000 else 999.999):.3f}")
        listbox_highscores.bind("<Button-1>", lambda e: "break")

        scrollbar_highscores: Scrollbar = Scrollbar(frame_highscore_list)
        listbox_highscores.config(yscrollcommand = scrollbar_highscores.set)
        scrollbar_highscores.config(command = listbox_highscores.yview)

        scrollbar_highscores.pack(side=RIGHT, fill=BOTH)
        listbox_highscores.pack()

        def do_change_difficulty_displayed(label_clicked: Label):
            nonlocal difficulty_selected, current_leaderboard
            if label_clicked != difficulty_selected:
                label_clicked.config(relief=SUNKEN)
                difficulty_selected.config(relief=RAISED)

                label_loading.place(relx=0.5, rely=0.9, anchor=CENTER)
                root.update()
                current_leaderboard = get_leaderboard(label_clicked.difficulty)
                label_loading.place_forget()

                listbox_highscores.delete(0,END)
                for position, item in enumerate(current_leaderboard, 1):
                    listbox_highscores.insert(END, f"{position}.{" " if position < 10 else ""} {item.get("name")}{" "*(29-len(item.get("name"))+7-len(str(f"{(item.get("time") if item.get("time") < 1000 else 999.999):.3f}")))}{(item.get("time") if item.get("time") < 1000 else 999.999):.3f}")
                
                difficulty_selected = (label_clicked)

        difficulty_change_buttons: list[Label] = []

        frame_highscore_footer: Frame = Frame(frame_highscore_main)
        for difficulty in ["Easy", "Medium", "Hard", "Impossible"]:
            temp_label: Label = Label(frame_highscore_footer, text=f" {difficulty} ", font=(default_font, 9), relief=RAISED)
            temp_label.bind("<Button-1>", func=lambda event, label=temp_label:do_change_difficulty_displayed(label))
            temp_label.pack(side="left", padx=2)
            temp_label.difficulty = difficulty
            difficulty_change_buttons.append(temp_label)
        
        difficulty_change_buttons[0].config(relief=SUNKEN)
        difficulty_selected = difficulty_change_buttons[0]

        def do_update_listbox(*args):
            search_term = search_var.get().lower()
            listbox_highscores.delete(0, END)
            for position, item in enumerate(current_leaderboard, 1):
                if search_term in item.get("name").lower():
                    listbox_highscores.insert(END, f"{position}.{" " if position < 10 else ""} {item.get("name")}{" "*(29-len(item.get("name"))+7-len(str(f"{(item.get("time") if item.get("time") < 1000 else 999.999):.3f}")))}{(item.get("time") if item.get("time") < 1000 else 999.999):.3f}")

        search_var = StringVar()
        search_var.trace_add("write", do_update_listbox)
        entry_search_bar = Entry(frame_window, textvariable=search_var)
        entry_search_bar.place(relx=0.5, rely=0.22, anchor=CENTER)

        frame_highscore_list.pack()
        frame_highscore_footer.pack(expand=True, pady=(5,0))

        label_title.place(relx=0.5, rely=0.1, anchor=CENTER)
        frame_highscore_main.place(relx=0.5, rely=0.5, anchor=CENTER)

def run_settings(root: Tk, frame_window: Frame) -> None:
    ... # not implemented

def main() -> None:
    run_Welcome()

if __name__ == "__main__":
    main()
