#import everything from tkinter library
from cProfile import label
from tkinter import * 
from tkinter import messagebox
from datetime import datetime
from tokenize import String
from turtle import up
from wsgiref.simple_server import software_version
import pytz
import requests

# for clock
IST = pytz.timezone('Asia/Kolkata')

software_version = 'v1.1'
app = Tk()

# App geometry and components
app.geometry("700x480+600+300")
app.title("VaccinateMe {software_version}")
app.iconbitmap("Images/vaccine_icon.ico")
app.resizable(False,True)
app.config(background='#293241')

# frame working
topLeft_col = "#5c4ce1"
topRight_col = "#867ae9"
# creating frame1
frame1 = Frame(app, height=120, width=180, bg=topLeft_col, bd=1, relief=FLAT)
# Placing a frame1
frame1.place(x=0, y=0)    #starting point for frame

# creating frame2
frame2 = Frame(app, height=120, width=520, bg=topRight_col, bd=1, relief=FLAT)
# Placing a frame2
frame2.place(x=180, y=0)

# creating frame3
frame3 = Frame(app, height=30, width=700, bg='black', bd=1, relief=RAISED)
# Placing a frame3
frame3.place(x=0, y=120)

# User inputs by entry widget 

#for PINCODE
pincode_var = StringVar()
pincode = Entry(app, width=11, bg="#eaf2ae", fg='black',font='verdana 11', textvariable=pincode_var)
# placing out input box for PINCODE
pincode.place(x=220, y=40)
pincode['textvariable'] = pincode_var

#for date
date_var = StringVar()
date = Entry(app, width=11, bg="#eaf2ae", fg='black',font='verdana 11', textvariable=date_var)
# placing out input box for date
date.place(x=380, y=40)
date['textvariable'] = date_var

# creating labels
label_Currdate = Label(text = "Current Date", bg=topLeft_col, font='verdana 12 bold')
label_Currdate.place(x=20, y=40)

label_time = Label(text = "Current Time", bg=topLeft_col, font='verdana 12 bold')
label_time.place(x=20, y=60)

label_pin = Label(text = "PINCODE", bg=topRight_col, font='verdana 11 bold')
label_pin.place(x=220, y=15)

label_date = Label(text = "Date", bg=topRight_col, font='verdana 11 bold')
label_date.place(x=380, y=15)

label_dateFormat = Label(text = "[dd-mm-yyyy]", bg=topRight_col, font='verdana 7 bold')
label_dateFormat.place(x=420, y=18)

label_searchVC = Label(text = "  Search \nAvailable Vaccines", bg=topRight_col, font='verdana 8 bold')
label_searchVC.place(x=572, y=70)

label_head_result = Label(text=" Status       \tCentre-Name\t              Age-Group    Vaccine       Dose_1     Dose_2     Total", bg = 'black', fg='white', font = 'Verdana 8 bold')
label_head_result.place(x=10, y=125)


# Create Text box for displaying the results
# 7 different boxes for different columns

result_box_avl = Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_avl.place(x= 3 , y= 152)
result_box_cent = Text(app, height = 20, width = 30, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_cent.place(x= 75 , y= 152)
result_box_age = Text(app, height = 20, width = 8, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_age.place(x= 330 , y= 152)
result_box_vacc = Text(app, height = 20, width = 10, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_vacc.place(x= 400 , y= 152)
result_box_D1 = Text(app, height = 20, width = 7, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D1.place(x= 490 , y= 152)
result_box_D2 = Text(app, height = 20, width = 7, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D2.place(x= 555 , y= 152)
result_box_D1_D2 = Text(app, height = 20, width = 7, bg='#293241',fg='#ecfcff', relief=FLAT, font='verdana 10')
result_box_D1_D2.place(x= 630 , y= 152)

# function to update the clock (Date and Time) regularly
def update_clock():
    raw_TS = datetime.now(IST)
    date_now = raw_TS.strftime("%d %b %Y")
    time_now = raw_TS.strftime("%H:%M:%S %p")
    # formatted_now, we will need this for current date fatching
    formatted_now = raw_TS.strftime("%d-%m-%Y")
    # label_date_now.after(500, update_clock)
    # updating text label of Currdate and time
    label_Currdate.config(text = date_now)
    label_time.config(text = time_now)
    label_time.after(1000, update_clock)
    return formatted_now

# function to fetch current date
def insert_today_date():
    formatted_now = update_clock()
    #used .set() method to put this collected date into that date entry field.
    date_var.set(formatted_now)
    tomorrow_date_chkbox['state'] = DISABLED


# To detect automatic Pincode based on ISP location service
url = 'https://ipinfo.io/postal'
def fill_pincode_with_radio():
    curr_pincode = get_pincode_ip_service(url)
    pincode_var.set(curr_pincode)

# we can detect PIN because of internet service provider ipinfo
def get_pincode_ip_service(url):
    response_pincode = requests.get(url).text
    return response_pincode

# Refresh API call and clear the search result area
def refresh_api_call(PINCODE, DATE):
    header = {'User-Agent': 'Chrome/84.0.4147.105 Safari/537.36'}
    request_link = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={PINCODE}&date={DATE}"
    response = requests.get(request_link, headers = header)
    resp_JSON = response.json()
    return resp_JSON

# below function will clear all the boxes ( results boxed that we have made earlier )
def clear_result_box():
    result_box_avl.delete('1.0', END)
    result_box_cent.delete('1.0', END)
    result_box_age.delete('1.0', END)
    result_box_vacc.delete('1.0', END)
    result_box_D1.delete('1.0', END)
    result_box_D2.delete('1.0', END)
    result_box_D1_D2.delete('1.0', END)

# Code when search button is pressed
def search_vaccine_avl():
    clear_result_box()
    PINCODE = pincode_var.get().strip()
    DATE = date_var.get()
    resp_JSON = refresh_api_call(PINCODE, DATE)

    try:
        if len(resp_JSON['sessions']) == 0:
            messagebox.showinfo("INFO","Vaccine not yet arrived for the given date")

        for sess in resp_JSON['sessions']:
            age_limit           = sess['min_age_limit']
            center_name         = sess['name']
            pincode             = sess['pincode']
            vaccine_name        = sess['vaccine']
            available_capacity  = sess['available_capacity']
            qnty_dose_1         = sess['available_capacity_dose1']
            qnty_dose_2         = sess['available_capacity_dose2']
            slot_date           = sess['date']

            if available_capacity > 0:
                curr_status = 'Available'
            else:
                curr_status = 'NA'
            
            if age_limit == 45:
                age_grp = '45+'
            else:
                age_grp = '18-44'

            # data_msg = "{0:<12}{1:<40}{2:<10}{3:<10}{4:<5}{5:<5}\n".format(curr_status,center_name,age_grp,vaccine_name,qnty_dose_1,qnty_dose_2)
            # result_box.insert(END, " {0:<10s} {1:<30.28s}    {2:<10s} {3:<14s}  {4:<5} {5:<5} {6:^8}\n".format(curr_status,center_name,str(age_grp),vaccine_name,str(qnty_dose_1),str(qnty_dose_2), available_capacity))
            # result_box.insert(END, str.rjust(age_grp, 8))
            result_box_avl.insert(END, f"{curr_status:^6s}")
            result_box_avl.insert(END,"\n")
            result_box_cent.insert(END, f"{center_name:<30s}")
            result_box_cent.insert(END,"\n")
            result_box_age.insert(END, f"{age_grp:<6s}")
            result_box_age.insert(END,"\n")
            result_box_vacc.insert(END, f"{vaccine_name:<8s}")
            result_box_vacc.insert(END,"\n")
            result_box_D1.insert(END, f"{qnty_dose_1:>5}")
            result_box_D1.insert(END,"\n")
            result_box_D2.insert(END, f"{qnty_dose_2:>5}")
            result_box_D2.insert(END,"\n")
            result_box_D1_D2.insert(END, f"{available_capacity:<5}")
            result_box_D1_D2.insert(END,"\n")
            
    except KeyError as KE:
        messagebox.showerror("ERROR","No Available center(s) for the given Pincode and date")
        print (pincode_var.get())


# All buttons present in application
# Radio Buttons for PINCODE
curr_loc_var = StringVar()
# here app parameter defines the parent/root window for the object
radio_location = Radiobutton(app, text="Current location", bg= topRight_col, variable= curr_loc_var, value = curr_loc_var, command = fill_pincode_with_radio) #state=DISABLED
radio_location.place(x=215, y=65)

# Check Box 
chkbox_today_var = IntVar()
today_date_chkbox = Checkbutton(app, text='Today', bg= topRight_col, variable=chkbox_today_var, onvalue= 1, offvalue=0, command = insert_today_date)
today_date_chkbox.place(x= 375, y= 65)

chkbox_tomorrow_var = IntVar()
tomorrow_date_chkbox = Checkbutton(app, text='Tomorrow', bg= topRight_col, variable=chkbox_tomorrow_var, onvalue= 1, offvalue=0, state = DISABLED)
# tomorrow_date_chkbox.place(x= 435, y= 65)

# creating button (search button)
search_btn = Button(app, text='search', width=10,height=1 ,bd='4', command=search_vaccine_avl)
search_btn.place(x=595, y=25)

# calling clock fun to update time regularly
update_clock()

app.mainloop()