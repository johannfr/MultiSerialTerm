#!/usr/bin/env python
# -*- coding: utf-8 -*-

APPLICATION = "MultiSerialTerm"
VERSION = "0.1"
COMPANY = "FossAnalytical"
AUTHOR = "JOFR"

from Tkinter import Tk, Frame, Button, Label, StringVar, IntVar, Entry, Scrollbar, Listbox, Text, Menu, END, N, S, E, W, VERTICAL, HORIZONTAL, NONE
from Tkinter import Toplevel
from ttk import Combobox
import tkFileDialog
import tkMessageBox
import Queue

import serial.tools.list_ports

from SerialThread import SerialThread

from ConditionalsEditor import ConditionalsEditor

class SerialTerm(Tk):
    def __init__(self, serial_queue, serial_thread):
        Tk.__init__(self)
        self.title("Foss SerialTerminal for Multi")
        self.serial_queue = serial_queue
        self.serial_thread  = serial_thread

        menu_bar = Menu(self)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.parser_menu = Menu(menu_bar, tearoff=0)
        self.serial_parser_enabled = IntVar()
        self.serial_parser_enabled.set(1)
        self.parser_menu.add_checkbutton(
            label="Serial parser enabled",
            variable=self.serial_parser_enabled
        )
        self.parser_menu.add_command(label="Edit parser rules", command=self.open_conditionals_editor)
        menu_bar.add_cascade(label="Parser", menu=self.parser_menu)


        self.config(menu=menu_bar)
        main_frame = Frame(self)
        output_frame = Frame(main_frame)
        input_frame = Frame(main_frame)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        main_frame.grid(column=0, row=0, padx=3, pady=3, sticky=(N, W, E, S))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)



        output_text_vertical_scrollbar = Scrollbar(output_frame, orient=VERTICAL)
        output_text_horizontal_scrollbar = Scrollbar(output_frame, orient=HORIZONTAL)
        self.output_text = Text(
            output_frame,
            wrap=NONE,
            xscrollcommand=output_text_horizontal_scrollbar.set,
            yscrollcommand=output_text_vertical_scrollbar.set
        )
        self.output_text.configure(bg="white", state="disabled")
        self.output_text.grid(column=0, row=0, sticky=(N, S, E, W))
        output_text_vertical_scrollbar.grid(column=1, row=0, sticky=(N, S))
        output_text_vertical_scrollbar.config(command=self.output_text.yview)
        output_text_horizontal_scrollbar.grid(column=0, row=1, sticky=(E, W))
        output_text_horizontal_scrollbar.config(command=self.output_text.xview)

        output_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=1)


        self.input_string = StringVar()
        input_entry = Entry(input_frame, textvariable=self.input_string)
        input_entry.grid(column=0, row=0, sticky=(E, W))

        line_end_selection_items = ["CR&NL", "NL", "CR", "None"]
        self.line_end_selection = Combobox(
            input_frame,
            values=line_end_selection_items,
            state="readonly",
            width=len(max(line_end_selection_items, key=len))
        )
        self.line_end_selection.current(newindex=0)
        self.line_end_selection.grid(column=1, row=0)

        serial_port_names = ["Port"]
        serial_port_names.extend([s.name for s in serial.tools.list_ports.comports()])
        self.port_name_selection = Combobox(
            input_frame,
            values = serial_port_names,
            state="readonly",
            width=len(max(serial_port_names, key=len))
        )
        self.port_name_selection.current(newindex=0)
        self.port_name_selection_index = 0
        self.port_name_selection.grid(column=2, row=0)


        baudrates = [
            "300 baud",
            "1200 baud",
            "2400 baud",
            "4800 baud",
            "9600 baud",
            "19200 baud",
            "38400 baud",
            "57600 baud",
            "74880 baud",
            "115200 baud",
            "230400 baud",
            "250000 baud"
        ]

        self.baudrate_selection = Combobox(
            input_frame,
            values = baudrates,
            state="readonly",
            width=len(max(baudrates, key=len))
        )
        self.baudrate_selection.current(newindex=9)
        self.baudrate_selection.grid(column=3, row=0)

        input_frame.grid(column=0, row=1, sticky=(E, W))
        input_frame.grid_columnconfigure(0, weight=1)

        self.port_name_selection.bind("<<ComboboxSelected>>", self.port_name_selected)
        self.baudrate_selection.bind("<<ComboboxSelected>>", self.baudrate_selected)

        self.after(100, self.serial_tick)

        # TODO Load from pickle file.
        self.conditionals = [
            ["Enabled", "line.startswith(\"Hello\")", "Python", "print 'Fooobaaaaar. Jibb.'"],
            ["Enabled", "line.startswith(\"Foo\")", "Debugger", "halt\nreset"],
        ]
        self.counter = 0


    def open_conditionals_editor(self):
        self.conditionals_editor = Toplevel(master=self)
        self.parser_menu.entryconfig("Edit parser rules", state="disabled")
        ConditionalsEditor(self.conditionals_editor, self.conditionals, self.closing_conditionals_editor)

    def closing_conditionals_editor(self):
        self.parser_menu.entryconfig("Edit parser rules", state="normal")


    def update_output_text(self, line):
        self.output_text.configure(state="normal")
        self.output_text.insert(END, line)
        self.output_text.configure(state="disabled")
        self.output_text.see(END)

    def evaluate_conditionals(self, line):
        if self.serial_parser_enabled.get() == 1:
            for condition in self.conditionals:
                if condition[0] == "Enabled":
                    if eval(condition[1]):
                        if condition[2] == "Python":
                            exec(condition[3], locals())
                        elif condition[2] == "Debugger":
                            print "Send to debugger: %s"%condition[3]



    def serial_tick(self):
        while True:
            try:
                line = self.serial_queue.get_nowait()
                self.update_output_text(line)
                self.evaluate_conditionals(line)
            except Queue.Empty:
                break
        self.after(100, self.serial_tick)

    def port_name_selected(self, event):
        port_name = event.widget.selection_get()
        if port_name == "Port":
            event.widget.current(newindex=self.port_name_selection_index)
            return
        self.port_name_selection_index = event.widget.current()
        self.serial_thread.set_port(port_name)

    def baudrate_selected(self, event):
        self.serial_thread.set_baudrate(event.widget.selection_get())



if __name__ == "__main__":
    serial_queue = Queue.Queue()
    serial_thread = SerialThread(serial_queue)
    serial_thread.start()
    serial_term = SerialTerm(serial_queue, serial_thread)
    serial_term.resizable(True, True)

    serial_term.mainloop()
    serial_thread.close()
