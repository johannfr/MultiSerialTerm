#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import Tk, Frame, Button, Label, StringVar, Entry, Scrollbar, \
    Text, Radiobutton, Checkbutton, PhotoImage, Listbox, END, N, S, E, W,  \
    VERTICAL, HORIZONTAL, YES, NO, TOP, FLAT, SUNKEN, LEFT
import os
#from ttk import Treeview

class ConditionalsEditor:
    def __init__(self, my_window, conditionals, close_callback):
        #Tk.__init__(self)
        self.my_window = my_window
        self.my_window.title("Condition Editor")
        self.close_callback = close_callback
        self.conditionals = conditionals

        shared_pad_x = 3
        shared_pad_y = 3

        main_frame = Frame(self.my_window)
        main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        image_path = "images"
        image_files = [f for f in os.listdir(image_path)
            if os.path.isfile(os.path.join(image_path, f)) and
            f.endswith(".png")]
        self.icons = {}
        for image_file in image_files:
            self.icons[os.path.splitext(os.path.basename(image_file))[0]] = PhotoImage(file=os.path.join(image_path, image_file))

        up_down_button_frame = Frame(main_frame)

        self.up_button = Button(
            up_down_button_frame,
            state="disabled",
            text="Move up",
            image=self.icons["gtk-go-up"],
            command=self.up_pressed
        )
        self.up_button.grid(column=0, row=0, sticky=(E))

        self.down_button = Button(
            up_down_button_frame,
            state="disabled",
            text="Move down",
            image=self.icons["gtk-go-down"],
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

        for conditional in self.conditionals:
            self.state_listbox.insert(END, conditional[0])
            self.condition_listbox.insert(END, conditional[1])
            self.execution_target_listbox.insert(END, conditional[2])
        #for i in range(5):
        #    self.state_listbox.insert(END, "Foo %d"%i)
        #    self.condition_listbox.insert(END, "Bar %d"%i)
        #    self.execution_target_listbox.insert(END, "Baz %d"%i)


        if_label = Label(main_frame, text="If:", padx=10)
        if_label.grid(column=0, row=1, sticky=(N, E))
        self.if_text_variable = StringVar()
        if_entry = Entry(main_frame, textvariable=self.if_text_variable)
        if_entry.grid(
            column=1,
            row=1,
            sticky=(E, W),
            padx=shared_pad_x,
            pady=shared_pad_y,
        )

        then_label = Label(main_frame, text="Then:", padx=10)
        then_label.grid(column=0, row=2, sticky=(N, E))
        self.then_entry = Text(main_frame)
        self.then_entry.grid(
            column=1,
            row=2,
            sticky=(N, S, E, W),
            padx=shared_pad_x,
            rowspan=2,
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
        self.execution_target.set("Debugger")
        debugger_radiobutton = Radiobutton(
            option_frame,
            text="Debugger",
            variable=self.execution_target,
            value="Debugger"
        )
        debugger_radiobutton.grid(column=0, row=1, sticky=(N, W))
        python_radiobutton = Radiobutton(
            option_frame,
            text="Python",
            variable=self.execution_target,
            value="Python"
        )
        python_radiobutton.grid(column=0, row=2, sticky=(N, W))
        state_label = Label(option_frame, text="State")
        state_label.grid(
            column=0,
            row=3,
            sticky=(N, W),
            pady=(10, shared_pad_y)
        )

        self.active_checkbutton = StringVar()
        self.active_checkbutton.set("Enabled")
        active_checkbutton = Checkbutton(
            option_frame,
            text="Enabled",
            variable=self.active_checkbutton,
            onvalue="Enabled",
            offvalue="Disabled"
        )
        active_checkbutton.grid(column=0, row=4, sticky=(N, W))
        option_frame.grid(column=0, row=3, sticky=(N, S, E, W), pady=5)

        button_frame = Frame(main_frame)
        self.add_button = Button(
            button_frame,
            state="disabled",
            text="Add",
            image=self.icons["gtk-add"],
            compound=LEFT)
        self.add_button.grid(column=0, row=0, sticky=(E))
        self.update_button = Button(
            button_frame,
            state="disabled",
            text="Update",
            image=self.icons["gtk-edit"],
            compound=LEFT
        )
        self.update_button.grid(column=1, row=0, sticky=(E))
        self.delete_button = Button(
            button_frame,
            state="disabled",
            text="Delete",
            image=self.icons["gtk-remove"],
            compound=LEFT
        )
        self.delete_button.grid(column=2, row=0, sticky=(E))
        button_frame.grid(
            column=0,
            row=4,
            columnspan=2,
            sticky=(E),
            padx=shared_pad_x,
            pady=shared_pad_y
        )

        close_frame = Frame(main_frame)
        close_button = Button(
            close_frame,
            text="Close",
            image=self.icons["gtk-close"],
            compound=LEFT,
            command=self.on_closing
        )
        close_button.grid(column=0, row=0, sticky=(S, E))
        close_frame.grid(
            column=0,
            row=5,
            columnspan=2,
            sticky=(S, E),
            padx=shared_pad_x,
            pady=(15, shared_pad_y)
        )


        self.my_window.grid_columnconfigure(0, weight=1)
        self.my_window.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=0)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        condition_list.grid_columnconfigure(1, weight=1)
        button_frame.grid_rowconfigure(0, weight=1)

        self.my_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if self.close_callback is not None:
            self.close_callback()
        self.my_window.destroy()


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

        self.conditionals.insert(index-1, self.conditionals.pop(index))

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

        self.conditionals.insert(index+1, self.conditionals.pop(index))

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
        self.delete_button.config(state="normal")
        self.then_entry.delete("1.0", END)
        self.then_entry.insert(
            END,
            self.conditionals[self.state_listbox.curselection()[0]][3]
        )
        self.if_text_variable.set(
            self.conditionals[self.state_listbox.curselection()[0]][1]
        )

        self.execution_target.set(
            self.conditionals[self.state_listbox.curselection()[0]][2]
        )

        self.active_checkbutton.set(
            self.conditionals[self.state_listbox.curselection()[0]][0]
        )




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
    conditionals = [
        ["Enabled", "line.startswith(\"foo\")", "Python", "f = ....."],
        ["Disabled", "line.startswith(\"bar\")", "Debugger", "halt\nreset"],
    ]
    tt = ConditionalsEditor(conditionals)
    tt.resizable(True, True)
    tt.mainloop()
