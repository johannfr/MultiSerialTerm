#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Label, StringVar, Entry, Scrollbar, \
    Text, Radiobutton, Checkbutton, PhotoImage, Listbox, END, N, S, E, W,  \
    VERTICAL, HORIZONTAL, YES, NO, TOP, FLAT, SUNKEN
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

        self.up_icon = PhotoImage(file="images/gtk-go-up.png")
        self.up_button = Button(
            up_down_button_frame,
            state="disabled",
            text="Move up",
            image=self.up_icon,
            command=self.up_pressed
        )
        self.up_button.grid(column=0, row=0, sticky=(E))

        self.down_icon = PhotoImage(file="images/gtk-go-down.png")
        self.down_button = Button(
            up_down_button_frame,
            state="disabled",
            text="Move down",
            image=self.down_icon,
            command=self.down_pressed
        )
        self.down_button.grid(column=0, row=1, sticky=(E))


        up_down_button_frame.grid(column=0, row=0, sticky=(E))


        condition_list = Frame(main_frame, relief=SUNKEN, borderwidth=1)
        condition_list.grid(
            column=1,
            row=0,
            sticky=(N, S, E, W),
            padx=shared_pad_x,
            pady=shared_pad_y,
            columnspan=1
        )
        self.condition_list_scrollbar = Scrollbar(condition_list)

        self.state_listbox = Listbox(
            condition_list,
            relief=FLAT,
            exportselection=False,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=self.state_listbox_scroll,
            activestyle="none"
        )
        self.state_listbox.grid(column=0, row=0, padx=0, sticky=(N, S))
        self.state_listbox.bind(
            "<<ListboxSelect>>",
            self.state_listbox_selected
        )

        self.condition_listbox = Listbox(
            condition_list,
            relief=FLAT,
            exportselection=False,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=self.condition_listbox_scroll,
            activestyle="none"
        )
        self.condition_listbox.grid(column=1, row=0, sticky=(N, S, E, W), padx=0)
        self.condition_listbox.bind(
            "<<ListboxSelect>>",
            self.condition_listbox_selected
        )

        self.execution_target_listbox = Listbox(
            condition_list,
            relief=FLAT,
            exportselection=False,
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=self.execution_target_listbox_scroll,
            activestyle="none"
        )
        self.execution_target_listbox.grid(column=2, row=0, padx=0, sticky=(N, S))
        self.execution_target_listbox.bind(
            "<<ListboxSelect>>",
            self.execution_target_listbox_selected
        )

        self.condition_list_scrollbar.grid(column=3, row=0, sticky=(N, S))
        self.condition_list_scrollbar.config(
            command=self.condition_list_scrollbar_callback
        )
        condition_list.grid_rowconfigure(0, weight=1)


        for i in range(5):
            self.state_listbox.insert(END, "Foo %d"%i)
            self.condition_listbox.insert(END, "Bar %d"%i)
            self.execution_target_listbox.insert(END, "Baz %d"%i)


        if_label = Label(main_frame, text="If:", padx=10)
        if_label.grid(column=0, row=1, sticky=(N, E))
        if_text_variable = StringVar()
        if_entry = Entry(main_frame, textvariable=if_text_variable)
        if_entry.grid(
            column=1,
            row=1,
            sticky=(E, W),
            padx=shared_pad_x,
            pady=shared_pad_y
        )

        then_label = Label(main_frame, text="Then:", padx=10)
        then_label.grid(column=0, row=2, sticky=(N, E))
        then_entry = Text(main_frame)
        then_entry.grid(
            column=1,
            row=2,
            sticky=(N, S, E, W),
            padx=shared_pad_x,
            rowspan=2
        )

        option_frame = Frame(main_frame)
        execution_target_label = Label(option_frame, text="Execution target:")
        execution_target_label.grid(
            column=0,
            row=0,
            sticky=(N, W),
            pady=(10, shared_pad_y)
        )
        self.execution_target = StringVar()
        self.execution_target.set("debugger")
        debugger_radiobutton = Radiobutton(
            option_frame,
            text="Debugger",
            variable=self.execution_target,
            value="debugger"
        )
        debugger_radiobutton.grid(column=0, row=1, sticky=(N, W))
        python_radiobutton = Radiobutton(
            option_frame,
            text="Python",
            variable=self.execution_target,
            value="python"
        )
        python_radiobutton.grid(column=0, row=2, sticky=(N, W))
        state_label = Label(option_frame, text="State")
        state_label.grid(
            column=0,
            row=3,
            sticky=(N, W),
            pady=(10, shared_pad_y)
        )

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
        button_frame.grid(
            column=0,
            row=4,
            columnspan=2,
            sticky=(E),
            padx=shared_pad_x,
            pady=shared_pad_y
        )

        close_frame = Frame(main_frame)
        close_button = Button(close_frame, text="Close")
        close_button.grid(column=0, row=0, sticky=(S, E))
        close_frame.grid(
            column=0,
            row=5,
            columnspan=2,
            sticky=(S, E),
            padx=shared_pad_x,
            pady=(15, shared_pad_y)
        )


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
        index = self.state_listbox.curselection()[0]
        state_current = self.state_listbox.get(index)
        condition_current = self.condition_listbox.get(index)
        execution_target_current = self.execution_target_listbox.get(index)
        self.state_listbox.delete(index)
        self.condition_listbox.delete(index)
        self.execution_target_listbox.delete(index)
        self.state_listbox.insert(index-1, state_current)
        self.condition_listbox.insert(index-1, condition_current)
        self.execution_target_listbox.insert(index-1, execution_target_current)

        self.state_listbox.selection_set(index-1)
        self.condition_listbox.selection_set(index-1)
        self.execution_target_listbox.selection_set(index-1)
        self.state_listbox.see(index-1)

        if index-1 == 0:
            self.up_button.config(state="disabled")
        self.down_button.config(state="normal")

    def down_pressed(self):
        index = self.state_listbox.curselection()[0]
        state_current = self.state_listbox.get(index)
        condition_current = self.condition_listbox.get(index)
        execution_target_current = self.execution_target_listbox.get(index)
        self.state_listbox.delete(index)
        self.condition_listbox.delete(index)
        self.execution_target_listbox.delete(index)
        self.state_listbox.insert(index+1, state_current)
        self.condition_listbox.insert(index+1, condition_current)
        self.execution_target_listbox.insert(index+1, execution_target_current)

        self.state_listbox.selection_set(index+1)
        self.condition_listbox.selection_set(index+1)
        self.execution_target_listbox.selection_set(index+1)
        self.state_listbox.see(index+1)

        if index+1 == self.state_listbox.size()-1:
            self.down_button.config(state="disabled")
        self.up_button.config(state="normal")

    def condition_list_scrollbar_callback(self, *args):
        self.state_listbox.yview(*args)
        self.condition_listbox.yview(*args)
        self.execution_target_listbox.yview(*args)

    def state_listbox_scroll(self, *args):
        self.condition_listbox.yview_moveto(args[0])
        self.execution_target_listbox.yview_moveto(args[0])
        self.condition_list_scrollbar.set(*args)

    def condition_listbox_scroll(self, *args):
        self.state_listbox.yview_moveto(args[0])
        self.execution_target_listbox.yview_moveto(args[0])

    def execution_target_listbox_scroll(self, *args):
        self.state_listbox.yview_moveto(args[0])
        self.condition_listbox.yview_moveto(args[0])


    def any_listbox_selected(self):
        self.up_button.config(state="normal")
        self.down_button.config(state="normal")
        if self.state_listbox.curselection()[0] == self.state_listbox.size()-1:
            self.down_button.config(state="disabled")
        if self.state_listbox.curselection()[0] == 0:
            self.up_button.config(state="disabled")


    def state_listbox_selected(self, event):
        index = self.state_listbox.curselection()[0]
        try:
            self.condition_listbox.selection_clear(
                self.condition_listbox.curselection()[0]
            )
        except IndexError:
            pass
        self.condition_listbox.selection_set(index)
        try:
            self.execution_target_listbox.selection_clear(
                self.execution_target_listbox.curselection()[0]
            )
        except IndexError:
            pass
        self.execution_target_listbox.selection_set(index)
        self.any_listbox_selected()

    def condition_listbox_selected(self, event):
        index = self.condition_listbox.curselection()[0]
        try:
            self.state_listbox.selection_clear(
                self.state_listbox.curselection()[0]
            )
        except IndexError:
            pass
        self.state_listbox.selection_set(index)
        try:
            self.execution_target_listbox.selection_clear(
                self.execution_target_listbox.curselection()[0]
            )
        except IndexError:
            pass
        self.execution_target_listbox.selection_set(index)
        self.any_listbox_selected()

    def execution_target_listbox_selected(self, event):
        index = self.execution_target_listbox.curselection()[0]
        try:
            self.state_listbox.selection_clear(
                self.state_listbox.curselection()[0]
            )
        except IndexError:
            pass
        self.state_listbox.selection_set(index)
        try:
            self.condition_listbox.selection_clear(
                self.condition_listbox.curselection()[0]
            )
        except IndexError:
            pass
        self.condition_listbox.selection_set(index)
        self.any_listbox_selected()




if __name__ == "__main__":
    tt = TreeTest()
    tt.resizable(True, True)
    tt.mainloop()
