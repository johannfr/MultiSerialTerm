#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Label, StringVar, Entry, Scrollbar, Text, Radiobutton, Checkbutton, PhotoImage, Listbox, END, N, S, E, W, VERTICAL, HORIZONTAL, YES, NO, TOP, FLAT, SUNKEN
#from ttk import Treeview

class TreeTest(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Condition Editor")

        shared_pad_x = 3
        shared_pad_y = 3

        main_frame = Frame(self)
        main_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        up_down_button_frame = Frame(main_frame)

        self.up_icon = PhotoImage(file="gtk-go-up.png")
        up_button = Button(up_down_button_frame, text="Move up", image=self.up_icon, command=self.up_pressed)
        up_button.grid(column=0, row=0, sticky=(E))

        self.down_icon = PhotoImage(file="gtk-go-down.png")
        down_button = Button(up_down_button_frame, text="Move down", image=self.down_icon, command=self.down_pressed)
        down_button.grid(column=0, row=1, sticky=(E))


        up_down_button_frame.grid(column=0, row=0, sticky=(E))


        condition_list = Frame(main_frame, relief=SUNKEN, borderwidth=1)
        condition_list.grid(column=1, row=0, sticky=(N, S, E, W), padx=shared_pad_x, pady=shared_pad_y, columnspan=1)
        self.condition_list_scrollbar = Scrollbar(condition_list)
        self.state_listbox = Listbox(condition_list, relief=FLAT, borderwidth=0, highlightthickness=0,  yscrollcommand=self.other_scroll)
        self.state_listbox.grid(column=0, row=0, padx=0)
        self.condition_listbox = Listbox(condition_list, relief=FLAT, borderwidth=0, highlightthickness=0, yscrollcommand=self.other_scroll)
        self.condition_listbox.grid(column=1, row=0, sticky=(E, W), padx=0)
        self.execution_target_listbox = Listbox(condition_list, relief=FLAT, borderwidth=0, highlightthickness=0,  yscrollcommand=self.other_scroll)
        self.execution_target_listbox.grid(column=2, row=0, padx=0)
        self.condition_list_scrollbar.grid(column=3, row=0, sticky=(N, S))
        self.condition_list_scrollbar["command"] = self.condition_list_scroll


        for i in range(30):
            self.state_listbox.insert(END, "Foo %d"%i)
            self.condition_listbox.insert(END, "Bar %d"%i)
            self.execution_target_listbox.insert(END, "Baz %d"%i)


        if_label = Label(main_frame, text="If:", padx=10)
        if_label.grid(column=0, row=1, sticky=(N, E))
        if_text_variable = StringVar()
        if_entry = Entry(main_frame, textvariable=if_text_variable)
        if_entry.grid(column=1, row=1, sticky=(E, W), padx=shared_pad_x, pady=shared_pad_y)

        then_label = Label(main_frame, text="Then:", padx=10)
        then_label.grid(column=0, row=2, sticky=(N, E))
        then_entry = Text(main_frame)
        then_entry.grid(column=1, row=2, sticky=(N, S, E, W), padx=shared_pad_x, rowspan=2)

        option_frame = Frame(main_frame)
        execution_target_label = Label(option_frame, text="Execution target:")
        execution_target_label.grid(column=0, row=0, sticky=(N, W), pady=(10, shared_pad_y))
        self.execution_target = StringVar()
        self.execution_target.set("debugger")
        debugger_radiobutton = Radiobutton(option_frame, text="Debugger", variable=self.execution_target, value="debugger")
        debugger_radiobutton.grid(column=0, row=1, sticky=(N, W))
        python_radiobutton = Radiobutton(option_frame, text="Python", variable=self.execution_target, value="python")
        python_radiobutton.grid(column=0, row=2, sticky=(N, W))
        state_label = Label(option_frame, text="State")
        state_label.grid(column=0, row=3, sticky=(N, W), pady=(10, shared_pad_y))

        active_checkbutton = Checkbutton(option_frame, text="Enabled")
        active_checkbutton.grid(column=0, row=4, sticky=(N, W))
        option_frame.grid(column=0, row=3, sticky=(N, S, E, W), pady=5)

        button_frame = Frame(main_frame)
        add_button = Button(button_frame, text="Add")
        add_button.grid(column=0, row=0, sticky=(E))
        update_button = Button(button_frame, text="Update")
        update_button.grid(column=1, row=0, sticky=(E))
        delete_button = Button(button_frame, text="Delete")
        delete_button.grid(column=2, row=0, sticky=(E))
        button_frame.grid(column=0, row=4, columnspan=2, sticky=(E), padx=shared_pad_x, pady=shared_pad_y)

        close_frame = Frame(main_frame, bg="pink")
        close_button = Button(close_frame, text="Close")
        close_button.grid(column=0, row=0, sticky=(S, E))
        close_frame.grid(column=0, row=5, columnspan=2, sticky=(S, E), padx=shared_pad_x, pady=(15, shared_pad_y))





        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=0)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        condition_list.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)

    def up_pressed(self):
        print "Up"

    def down_pressed(self):
        print "Down"

    def condition_list_scroll(self, *args):
        self.state_listbox.yview(*args)
        self.condition_listbox.yview(*args)
        self.execution_target_listbox.yview(*args)
        print args

    def other_scroll(self, *args):
        self.condition_list_scrollbar.set(*args)
        # print args



if __name__ == "__main__":
    tt = TreeTest()
    tt.resizable(True, True)
    tt.mainloop()
