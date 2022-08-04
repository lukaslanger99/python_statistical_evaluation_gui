from datetime import datetime
import tkinter as tk
from tkcalendar import DateEntry
from FileHandler import FileHandler as fh
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import randint

class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.labels = fh.read_json_file_to_dict_list(fh, "labels.json")
        self.events = fh.read_json_file_to_dict_list(fh, "events.json")

        self.init_date_picker()
        self.init_event_picker()
        self.init_filter_list()
        self.init_config_buttons()
        
        self.init_graph()

    def addLabel(self, name, type):
        self.labels.append({"name": name.replace(" ", "_"), "type": type})
        fh.write_dict_list_to_json_file(fh, "labels.json", self.labels)

    def addEvent(self, description, date, label_entry_list):
        event_labels = {}
        id = 0
        if self.events:
            id = (self.events[-1]["id"] + 1)
        for entry in label_entry_list:
            try:
                event_labels[entry["name"]] = int(entry["entry_widget"].get())
            except:
                event_labels[entry["name"]] = entry["entry_widget"].get()
        self.events.append({"id": id, "description": description, "date": date, "event_labels": event_labels})
        fh.write_dict_list_to_json_file(fh, "events.json", self.events)

    def init_date_picker(self):
        tk.Label(self.parent, text="from").grid(row=0, column=0)
        dateentry_from = DateEntry(self.parent,width=30,bg="darkblue",fg="white")
        dateentry_from.grid(row=0, column=1)
        tk.Label(self.parent, text="to").grid(row=0, column=2)
        dateentry_to = DateEntry(self.parent,width=30,bg="darkblue",fg="white")
        dateentry_to.grid(row=0, column=3)
        def datepicker_submit():
            self.event_list.delete(0, tk.END)
            for event in self.events:
                if datetime.strptime(dateentry_from.get(), "%d.%m.%y") <= datetime.strptime(event["date"], "%d.%m.%y") <= datetime.strptime(dateentry_to.get(), "%d.%m.%y"):
                    self.event_list.insert(tk.END, '{}: {} [{}]'.format(event["date"], event["description"], event["id"]))
        tk.Button(self.parent, text="Select Range", command=datepicker_submit).grid(row=0, column=4)

    def init_event_picker(self):
        self.event_list = tk.Listbox(self.parent, height=6, selectmode="extended")
        self.event_list.grid(row=1, column=0)

        def eventpicker_submit():
            for i in self.event_list.curselection():
                print(self.event_list.get(i))
        tk.Button(self.parent, text="Select Events", command=eventpicker_submit).grid(row=1, column=1)

    def init_filter_list(self):
        filter_frame = tk.Frame(self.parent, bg="white")
        filter_frame.grid(row=2, column=0)
        filter_checkboxes = []

        def checkbox_select_all_clicked():
            for checkbox in filter_checkboxes:
                checkbox["value"].set(cb.get())
        cb = tk.IntVar()
        checkbox = tk.Checkbutton(filter_frame, text="Select All", variable=cb, command=checkbox_select_all_clicked)
        checkbox.pack()
        for label in self.labels:
            if label["type"] == "Integer":
                checkbox_var = tk.IntVar()
                checkbox = tk.Checkbutton(filter_frame, variable=checkbox_var, text=label["name"])
                checkbox.pack()
                filter_checkboxes.append({"checkbox": checkbox, "value": checkbox_var})
        def submit_filters():
            print("filters")
        tk.Button(self.parent, text="Update", command=submit_filters).grid(row=3, column=0)

    def init_config_buttons(self):
        tk.Button(self.parent, text="New Event", command=self.listener_new_event_button_submit).grid(row=0, column=8)
        tk.Button(self.parent, text="Configure Labels", command=self.listener_config_button_submit).grid(row=1, column=8)

    def init_graph(self):
        colors = []
        for i in range(12):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
        figure1 = Figure(figsize=(4,3), dpi=100)
        subplot1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, self.parent)
        bar1.name='latheesh'
        bar1.get_tk_widget().grid(row=3, column=1)

        i = 0
        for label in self.labels:
            if label["type"] == "Integer":
                dates = []
                values = []
                for event in self.events:
                    dates.append(event["date"])
                    values.append(event["event_labels"][label["name"]])
                subplot1.plot(dates, values, color=colors[i+1], linestyle='dashed', linewidth = 1, marker='o', markerfacecolor=colors[i+1], markersize=5, label=label["name"])
                i = i + 1
        subplot1.legend()

    def listener_new_event_button_submit(self):
        new_event_window = tk.Toplevel(self.parent)
        new_event_window.title("New Event")

        # event description
        tk.Label(new_event_window, text="Event Description").grid(row=0, column=0)
        event_description = tk.Entry(new_event_window)
        event_description.grid(row=0, column=1)

        # event date
        tk.Label(new_event_window, text="Event Date").grid(row=1, column=0)
        event_date = DateEntry(new_event_window,width=30,bg="darkblue",fg="white")
        event_date.grid(row=1, column=1)

        # dynamic labels
        rowCount = 2
        label_entry_list = []
        for label in self.labels:
            label_text = '{} ({}):'.format(label["name"], label["type"])
            tk.Label(new_event_window, text=label_text).grid(row=rowCount, column=0)
            label_entry = tk.Entry(new_event_window)
            label_entry.grid(row=rowCount, column=1)
            label_entry_list.append({"name": label["name"], "entry_widget": label_entry})
            rowCount = rowCount + 1

        def create_new_event_button_submit():
            self.addEvent(event_description.get(), event_date.get(), label_entry_list)
            new_event_window.destroy()
        # submit
        tk.Button(new_event_window, text="Create", command=create_new_event_button_submit).grid(row=rowCount, column=0)

    def listener_config_button_submit(self):
        config_window = tk.Toplevel(self.parent)
        config_window.title("Configure Labels")

        row_counter = 0
        for label in self.labels:
            tk.Label(config_window, text =label["name"]).grid(row=row_counter, column=0)
            row_counter = row_counter + 1
        def new_label_button_submit():
            # window data
            new_label_window = tk.Toplevel(self.parent)
            new_label_window.title("New Label")

            # label text
            tk.Label(new_label_window, text="Label Name").grid(row=0, column=0)
            label_text = tk.Entry(new_label_window)
            label_text.grid(row=1, column=0)

            # label type
            tk.Label(new_label_window, text="Label Type").grid(row=2, column=0)
            label_types = ['Integer', 'String']
            selected_label_type = tk.StringVar(new_label_window)
            selected_label_type.set(label_types[0])
            new_label_window.option_var = tk.StringVar(new_label_window)
            label_type = tk.OptionMenu(new_label_window, selected_label_type, *label_types)
            label_type.grid(row=3, column=0)
            def create_new_label_button_submit():
                self.addLabel(label_text.get(), selected_label_type.get())
                new_label_window.destroy()
            # submit
            tk.Button(new_label_window, text="Create", command=create_new_label_button_submit).grid(row=4, column=0)
        tk.Button(config_window, text="New Label", command=new_label_button_submit).grid(row=row_counter, column=0)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
