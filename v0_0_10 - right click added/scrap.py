# Set up pre-loop label and text box and grid them into xy_frame
pre_loop_label = Label(xy_frame, text="PRE-LOOP (RUNS ONCE)")
pre_loop_label.grid(row=0, column=0, sticky=EW)
pre_loop_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
pre_loop_text_box.grid(row=1, column=0)
pre_loop_text_box.config(insertbackground="#FFFFFF")

# Set up main loop label and text box and grid them into xy_frame
main_loop_label = Label(xy_frame, text="MAIN LOOP (RUNS Total Loops TIMES)")
main_loop_label.grid(row=2, column=0, sticky=EW)
main_loop_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
main_loop_text_box.grid(row=3, column=0)
main_loop_text_box.config(insertbackground="#FFFFFF")

# Set up post-loop label and text box and grid them into xy_frame
post_loop_label = Label(xy_frame, text="POST LOOP (RUNS ONCE)")
post_loop_label.grid(row=4, column=0, sticky=EW)
post_loop_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
post_loop_text_box.grid(row=5, column=0)
post_loop_text_box.config(insertbackground="#FFFFFF")

# spacer label #1 to separate columns zero and 2
spacer_label_1 = Label(xy_frame, text="  ")
spacer_label_1.grid(row=1, column=1, sticky=EW)

# Set up click locations label and text box and grid them into xy_frame
click_locations_label = Label(xy_frame, text="CLICK LOCATIONS (name, x, y)")
click_locations_label.grid(row=0, column=2, sticky=EW)
click_locations_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
click_locations_text_box.grid(row=1, column=2)
click_locations_text_box.config(insertbackground="#FFFFFF")

# Set up data label and text box and grid them into xy_frame
data_label = Label(xy_frame, text="DATA")
data_label.grid(row=2, column=2, sticky=EW)
data_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
data_text_box.grid(row=3, column=2)
data_text_box.config(insertbackground="#FFFFFF")

# Set up notes label and text box and grid them into xy_frame
notes_label = Label(xy_frame, text="NOTES")
notes_label.grid(row=4, column=2, sticky=EW)
notes_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
notes_text_box.grid(row=5, column=2)
notes_text_box.config(insertbackground="#FFFFFF")

# spacer label #2 to separate columns 2 and 4
spacer_label_2 = Label(xy_frame, text="  ")
spacer_label_2.grid(row=1, column=3, sticky=EW)

# Set up subroutine #1 label and text box and grid them into xy_frame
subroutine_1_label = Label(xy_frame, text="SUBROUTINE #1")
subroutine_1_label.grid(row=0, column=4, sticky=EW)
subroutine_1_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
subroutine_1_text_box.grid(row=1, column=4)
subroutine_1_text_box.config(insertbackground="#FFFFFF")

# Set up subroutine #2 label and text box and grid them into xy_frame
subroutine_2_label = Label(xy_frame, text="SUBROUTINE #2")
subroutine_2_label.grid(row=2, column=4, sticky=EW)
subroutine_2_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
subroutine_2_text_box.grid(row=3, column=4)
subroutine_2_text_box.config(insertbackground="#FFFFFF")

# Set up subroutine #3 label and text box and grid them into xy_frame
subroutine_3_label = Label(xy_frame, text="SUBROUTINE #3")
subroutine_3_label.grid(row=4, column=4, sticky=EW)
subroutine_3_text_box = Text(xy_frame, width=30, height=5, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
subroutine_3_text_box.grid(row=5, column=4)
subroutine_3_text_box.config(insertbackground="#FFFFFF")

# button frame to hold the RUN, LOAD SCRIPT and SAVE SCRIPT buttons and the label and text widget
# for entering total loops (i.e. the number of times the user wants the main loop to run)
button_frame = ttk.Frame(root)

# run button
run_button = ttk.Button(button_frame, text='RUN', command=guiscript_run)
run_button.grid(row=0, column=0, sticky=EW)

# load script button
load_script_button = ttk.Button(button_frame, text='LOAD SCRIPT', command=load_script)
load_script_button.grid(row=0, column=1, sticky=EW)

# save script button
save_script_button = ttk.Button(button_frame, text='SAVE SCRIPT', command=save_script)
save_script_button.grid(row=0, column=2, sticky=EW)

# spacer label #3 in between three buttons and total loops label
spacer_label_3 = Label(button_frame, text="  ")
spacer_label_3.grid(row=0, column=3, sticky=EW)

# "total loops" label and text widget in which the user can enter total number of times the main loop
# will run
total_loops_label = Label(button_frame, text="Total loops")
total_loops_label.grid(row=0, column=4, sticky=EW)
total_loops_text_box = Text(button_frame, width=10, height=1, background='#000000', foreground='#FFFF00',
                font=('Courier', 10, 'bold'))
total_loops_text_box.grid(row=0, column=5)
total_loops_text_box.config(insertbackground="#FFFFFF")

# Grid xy_frame into root
xy_frame.grid(row=0, column=0, sticky=W)

# Grid button_frame into root
button_frame.grid(row=1, column=0, sticky=W)

# Start 'er up!
