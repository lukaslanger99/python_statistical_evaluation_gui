from tabnanny import check
from tkinter import *
from tkcalendar import Calendar,DateEntry
from FileHandler import FileHandler as fh

labels = fh.read_json_file_to_dict_list(fh, "labels.json")
events = fh.read_json_file_to_dict_list(fh, "events.json")

def addLabel(name, type):
    labels.append({"name": name, "type": type})
    fh.write_dict_list_to_json_file(fh, "labels.json", labels)

def addEvent(description, date, label_entry_list):
    event_labels = {}
    id = 0
    if events:
        id = (events[-1]["id"] + 1)
    for entry in label_entry_list:
        event_labels[entry["name"]] = entry["entry_widget"].get()
    events.append({"id": id, "description": description, "date": date, "event_labels": event_labels})
    fh.write_dict_list_to_json_file(fh, "events.json", events)

def new_event_button_submit():
    new_event_window = Toplevel(root)
    new_event_window.title("New Event")

    # event description
    Label(new_event_window, text="Event Description").grid(row=0, column=0)
    event_description = Entry(new_event_window)
    event_description.grid(row=0, column=1)

    # event date
    Label(new_event_window, text="Event Date").grid(row=1, column=0)
    event_date = DateEntry(new_event_window,width=30,bg="darkblue",fg="white")
    event_date.grid(row=1, column=1)

    # dynamic labels
    rowCount = 2
    label_entry_list = []
    for label in labels:
        label_text = '{} ({}):'.format(label["name"], label["type"])
        Label(new_event_window, text=label_text).grid(row=rowCount, column=0)
        label_entry = Entry(new_event_window)
        label_entry.grid(row=rowCount, column=1)
        label_entry_list.append({"name": label["name"], "entry_widget": label_entry})
        rowCount = rowCount + 1

    def create_new_event_button_submit():
        addEvent(event_description.get(), event_date.get(), label_entry_list)
        new_event_window.destroy()
    # submit
    Button(new_event_window, text="Create", command=create_new_event_button_submit).grid(row=rowCount, column=0)
    #todo


def config_button_submit():
    config_window = Toplevel(root)
    config_window.title("Configure Labels")

    row_counter = 0
    for label in labels:
        Label(config_window, text =label["name"]).grid(row=row_counter, column=0)
        row_counter = row_counter + 1
    def new_label_button_submit():
        # window data
        new_label_window = Toplevel(root)
        new_label_window.title("New Label")

        # label text
        Label(new_label_window, text="Label Name").grid(row=0, column=0)
        label_text = Entry(new_label_window)
        label_text.grid(row=1, column=0)

        # label type
        Label(new_label_window, text="Label Type").grid(row=2, column=0)
        label_types = ['Integer', 'String']
        selected_label_type = StringVar(new_label_window)
        selected_label_type.set(label_types[0])
        new_label_window.option_var = StringVar(new_label_window)
        label_type = OptionMenu(new_label_window, selected_label_type, *label_types)
        label_type.grid(row=3, column=0)
        def create_new_label_button_submit():
            addLabel(label_text.get(), selected_label_type.get())
            new_label_window.destroy()
        # submit
        Button(new_label_window, text="Create", command=create_new_label_button_submit).grid(row=4, column=0)
    Button(config_window, text="New Label", command=new_label_button_submit).grid(row=row_counter, column=0)


root = Tk()

# pick date range
Label(root, text="from").grid(row=0, column=0)
dateentry_from = DateEntry(root,width=30,bg="darkblue",fg="white")
dateentry_from.grid(row=0, column=1)
Label(root, text="to").grid(row=0, column=2)
dateentry_to = DateEntry(root,width=30,bg="darkblue",fg="white")
dateentry_to.grid(row=0, column=3)
def datepicker_submit():
    print(dateentry_from.get())
    print(dateentry_to.get())
Button(root, text="Select Range", command=datepicker_submit).grid(row=0, column=4)

# event list
event_list = Listbox(root, height=6, selectmode="extended")
event_list.grid(row=1, column=0)
for entry in events:
    event_list.insert(END, '{}: {} [{}]'.format(entry["date"], entry["description"], entry["id"]))

def eventpicker_submit():
    for i in event_list.curselection():
        print(event_list.get(i))
Button(root, text="Select Events", command=eventpicker_submit).grid(row=1, column=1)

# config buttons
Button(root, text="New Event", command=new_event_button_submit).grid(row=0, column=8)
Button(root, text="Configure Labels", command=config_button_submit).grid(row=1, column=8)

filter_frame = Frame(root, bg="white")
filter_frame.grid(row=2, column=0)
filter_checkboxes = []

def checkbox_select_all_clicked():
    for checkbox in filter_checkboxes:
        checkbox["value"].set(cb.get())
cb = IntVar()
checkbox = Checkbutton(filter_frame, text="Select All", variable=cb, command=checkbox_select_all_clicked)
checkbox.pack()
for label in labels:
    if label["type"] == "Integer":
        checkbox_var = IntVar()
        checkbox = Checkbutton(filter_frame, variable=checkbox_var, text=label["name"])
        checkbox.pack()
        filter_checkboxes.append({"checkbox": checkbox, "value": checkbox_var})
def submit_filters():
    print("filters")
Button(root, text="Submit", command=submit_filters).grid(row=3, column=0)

root.mainloop()