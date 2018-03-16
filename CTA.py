from Tkinter import Label, Button, Tk, FALSE, Entry, NE, StringVar, Menu, CENTER, LEFT, W, E, sys, Toplevel, Listbox, END, ACTIVE, Scrollbar, Frame, RIGHT, Y
from PIL import ImageTk, Image
from io import BytesIO
from urllib import urlopen
import webbrowser
import ttk
import time
import mysql.connector
import tkMessageBox
import random
import atexit
config = {'user': 'root','password': '','host': 'localhost','database': 'rcdb','raise_on_warnings': True,}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def search_user_window():
    root.geometry('250x185')
    global userlabel, ranklabel, promlabel, skine, skinl, skinb, lastpromo, currerank, namelabel, promoterl, oldrankla, promotera, oldrankal
    userlabel = Label(root, text="")
    ranklabel = Label(root, text="")
    promlabel = Label(root, text="")
    promotera = Label(root, text="")
    oldrankal = Label(root, text="")
    namelabel = Label(root, text="Username:", font="Arial 9 bold")
    lastpromo = Label(root, text="Last Promo:", font="Arial 9 bold")
    currerank = Label(root, text="Current Rank:", font="Arial 9 bold")
    promoterl = Label(root, text="Promoter:", font="Arial 9 bold")
    oldrankla = Label(root, text="Old Rank:", font="Arial 9 bold")
    namelabel.grid(row=0, sticky=W)
    userlabel.grid(row=0, sticky=E)
    currerank.grid(row=1, sticky=W)
    ranklabel.grid(row=1, sticky=E)
    lastpromo.grid(row=2, sticky=W)
    promlabel.grid(row=2, sticky=E)
    promoterl.grid(row=3, sticky=W)
    promotera.grid(row=3, sticky=E)
    oldrankla.grid(row=4, sticky=W)
    oldrankal.grid(row=4, sticky=E)
    skine = Entry(root)
    skinl = Label(root, text="Type a username")
    skinb = Button(root, text="Search", command=search_user)
    skinl.place(relx=0.72, x=1, y=105, anchor=NE)
    skine.place(relx=0.76, x=1, y=130, anchor=NE)
    skinb.place(relx=0.6, x=1, y=155, anchor=NE)
    skine.focus_set()

def search_user():
    ask = skine.get()
    sql = "SELECT * FROM db_PROMOTIONS WHERE player = '%s'" % (ask)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        username = row[0]
        userrank = row[1]
        oldrank = row[2]
        promoter = row[3]
        lastprom = row[5]
    userlabel.config(text=username, compound=LEFT)
    ranklabel.config(text=userrank, compound=LEFT)
    promlabel.config(text=lastprom, compound=LEFT)
    oldrankal.config(text=oldrank, compound=LEFT)
    promotera.config(text=promoter, compound=LEFT)
    userlabel.grid(row=0, column=1, sticky=E)
    ranklabel.grid(row=1, column=1, sticky=E)
    promlabel.grid(row=2, column=1, sticky=E)
    promotera.grid(row=3, column=1, sticky=E)
    oldrankal.grid(row=4, column=1, sticky=E)

def forget_all():
    noacclabl.place_forget()
    userlabel.grid_forget()
    ranklabel.grid_forget()
    promlabel.grid_forget()
    promotera.grid_forget()
    oldrankal.grid_forget()
    oldrankla.grid_forget()
    promoterl.grid_forget()
    lastpromo.grid_forget()
    currerank.grid_forget()
    namelabel.grid_forget()
    skine.place_forget()
    skinb.place_forget()
    skinl.place_forget()
    box.grid_forget()
    reason.grid_forget()
    promby.grid_forget()
    sellab.grid_forget()
    seluse.grid_forget()
    promot.grid_forget()
    relabl.grid_forget()
    selusr.grid_forget()
    yes.grid_forget()
    manentry.place_forget()
    manlabel.place_forget()
    susbutto.place_forget()
    rembutto.place_forget()
    edpbutto.place_forget()
    edubutto.place_forget()
    addbutto.place_forget()
    image.pack_forget()
    canla.pack_forget()
    canil.place_forget()
    canie.place_forget()
    canib.place_forget()

def manage_admin():
    root.geometry('175x150')
    global manentry, manlabel, susbutto, rembutto, edpbutto, edubutto, addbutto
    manentry = Entry(root)
    manlabel = Label(root, text="Type a username")
    susbutto = Button(root, text="Restrict", command=restrict_admin)
    rembutto = Button(root, text="Remove", command=remove_admin)
    edpbutto = Button(root, text="Edit Password", command=edit_admin_password)
    edubutto = Button(root, text="Edit Username", command=edit_admin_username)
    addbutto = Button(root, text="Add Admin", command=add_admin)
    susbutto.place(relx=0.64, x=1, y=50, anchor=NE)
    rembutto.place(relx=0.82, x=1, y=78, anchor=NE)
    edpbutto.place(relx=0.50, x=1, y=78, anchor=NE)
    addbutto.place(relx=0.92, x=1, y=106, anchor=NE)
    edubutto.place(relx=0.50, x=1, y=106, anchor=NE)
    manlabel.place(relx=0.76, x=1, y=3, anchor=NE)
    manentry.place(relx=0.84, x=1, y=25, anchor=NE)

def edit_admin_password():
    admin = manentry.get()
    sqlq = "SELECT COUNT(1) FROM db_ADMINS WHERE username = '%s'" % (admin)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        global pachentry, win2
        win2 = Toplevel(root)
        win2.resizable(width=FALSE, height=FALSE)
        win2.title("Password change")
        pachlabel = Label(win2, text="New password")
        pachentry = Entry(win2)
        pachbutto = Button(win2, text="Change", command=change_password)
        pachlabel.pack()
        pachentry.pack()
        pachbutto.pack()
    else:
        tkMessageBox.showerror("Error", "Invalid username.")
    cnx.commit()

def change_password():
    admin = manentry.get()
    pas = pachentry.get()
    cursor.execute("""UPDATE db_ADMINS SET `password`='%s', `last_action_by`='%s' WHERE username = '%s'""" % (pas, usern, admin))
    tkMessageBox.showinfo("Success", "Password successfully changed.".format(admin))
    cnx.commit()
    win2.destroy()

def edit_admin_username():
    admin = manentry.get()
    sqlq = "SELECT COUNT(1) FROM db_ADMINS WHERE username = '%s'" % (admin)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        global uschentry, win2
        win2 = Toplevel(root)
        win2.resizable(width=FALSE, height=FALSE)
        win2.title("Username change")
        uschlabel = Label(win2, text="New username")
        uschentry = Entry(win2)
        uschbutto = Button(win2, text="Change", command=change_username)
        uschlabel.pack()
        uschentry.pack()
        uschbutto.pack()
    else:
        tkMessageBox.showerror("Error", "Invalid username.")
    cnx.commit()

def change_username():
    admin = manentry.get()
    user = uschentry.get()
    cursor.execute("""UPDATE db_ADMINS SET `username`='%s', `last_action_by`='%s' WHERE username = '%s'""" % (user, usern, admin))
    tkMessageBox.showinfo("Success", "Username successfully changed.".format(admin))
    cnx.commit()
    win2.destroy()

def restrict_admin():
    admin = manentry.get()
    sqlq = "SELECT COUNT(1) FROM db_ADMINS WHERE username = '%s'" % (admin)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        sql = "SELECT * FROM db_ADMINS WHERE username = '%s'" % (admin)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            res = int(row[3])
        if (res == 0):
            cursor.execute("""UPDATE db_ADMINS SET `restricted`=1, `last_action_by`='%s' WHERE username = '%s'""" % (usern, admin))
            tkMessageBox.showinfo("Success", "Admin {} is now restricted.".format(admin))
        else:
            cursor.execute("""UPDATE db_ADMINS SET `restricted`=0, `last_action_by`='%s' WHERE username = '%s'""" % (usern, admin))
            tkMessageBox.showinfo("Success", "Admin {} is no longer restricted.".format(admin))
    else:
        tkMessageBox.showerror("Error", "Invalid username.")
    cnx.commit()

def add_admin():
    admin = manentry.get()
    sqlq = "SELECT COUNT(1) FROM db_ADMINS WHERE username = '%s'" % (admin)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        tkMessageBox.showerror("Error", "Username already exists.")
    else:
        pas = random.randint(10000000,99999999)
        str(pas)
        cursor.execute('''INSERT INTO `db_ADMINS`(`username`, `password`, `added_by`, `restricted`, `suspended`, `last_action_by`)
              VALUES (%s,%s,%s,%s,%s,%s)''',
            (admin, pas, usern, 0, 0, usern))
        tkMessageBox.showinfo("Success!", "New admin account created. \nDon't forget to change the password of the account!")
    cnx.commit()

def remove_admin():
    admin = manentry.get()
    sqlq = "SELECT COUNT(1) FROM db_ADMINS WHERE username = '%s'" % (admin)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        delstatmt = "DELETE FROM `db_ADMINS` WHERE username = '%s'" % (admin)
        cursor.execute(delstatmt)
        tkMessageBox.showinfo("Done", "Admin {} has been removed.".format(admin),)
    else:
        tkMessageBox.showerror("Error", "That username was not found in the database.")
    cnx.commit()

def menu_press_prom():
    forget_all()
    rank_choose()

def menu_press_manage_admin():
    forget_all()
    manage_admin()

def menu_press_can_I():
    forget_all()
    can_I()

def menu_press_user():
    forget_all()
    search_user_window()

def onselect(evt):
    global selected
    value = listbox.curselection()
    value = str(value).translate(None, '(),')
    selected = int(float(value))
    print selected

def menu_press_acc_reqs():
    global row, listbox, lab
    root.geometry('220x170')
    F1 = Frame()
    lab = Label(root)
    s = Scrollbar(F1)
    listbox = Listbox(F1)
    s.pack(side=RIGHT, fill=Y)
    listbox.bind('<<ListboxSelect>>', onselect)
    listbox.pack(side=LEFT, fill=Y)
    F1.grid(column=0, row=0)
    s['command'] = listbox.yview
    listbox['yscrollcommand'] = s.set
    apprbtt = Button(root, text="Approved", command=app_acc)
    denybtt = Button(root, text="Denied")
    lab.place(relx=0.77, x=1, y=30, anchor=W)
    apprbtt.place(relx=0.67, x=1, y=60, anchor=W)
    denybtt.place(relx=0.7, x=1, y=100, anchor=W)
    forget_all()
    cursor.execute('''SELECT `username` FROM db_REQ''')
    while row is not None:
        for item in [row]:
            listbox.insert(END, row)
        row = cursor.fetchone()

def app_acc():
    name = listbox.get(listbox.curselection())
    delstatmt = "DELETE FROM `db_REQ` WHERE `username` = '%s'" % (name)
    cursor.execute(delstatmt)

def can_I():
    global canla, canie, canil, canib
    root.geometry('200x125')
    canla = Label(root, text="", font="Arial 28 bold ")
    canie = Entry(root)
    canil = Label(root, text="Type a username")
    canib = Button(root, text="Can I promote them?", command=can_I_prom)
    canla.pack()
    canie.place(relx=0.8, x=1, y=75, anchor=NE)
    canib.place(relx=0.792, x=1, y=96, anchor=NE)
    canil.place(relx=0.73, x=1, y=53, anchor=NE)

def can_I_prom():
    num = arank - 7
    pentry = canie.get()
    sqlq = "SELECT COUNT(1) FROM db_PROMOTIONS WHERE player = '%s'" % (pentry)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        sql = "SELECT * FROM db_PROMOTIONS WHERE player = '%s'" % (pentry)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            prank = row[1]
        sql = "SELECT * FROM db_RANKS WHERE rank = '%s'" % (prank)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            prank = int(row[1])
    else:
        prank = 0
    if prank >= arank:
        canla.config(text="NO")
    elif prank == 0:
        tkMessageBox.showerror("Error", "User doesn't exist")
    elif prank > num:
        canla.config(text="NO")
    else:
        canla.config(text="YES")
    canla.pack()

def check_admin():
    username = userentry.get()
    password = passentry.get()
    sql = "SELECT * FROM db_ADMINS WHERE username = '%s'" % (username)
    cursor.execute(sql)
    results = cursor.fetchall()
    global usern, arank, image, im
    for row in results:
        usern = row[0]
        passw = row[1]
        res = int(row[3])
    sql = "SELECT * FROM db_PROMOTIONS WHERE player = '%s'" % (username)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        arank = row[1]
    sql = "SELECT * FROM db_RANKS WHERE rank = '%s'" % (arank)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        arank = int(row[1])
    if (1 == 1):
        if (res == 0):
            root.geometry('600x450')
            menu = Menu(root)
            root.config(menu=menu)
            sql = "SELECT * FROM db_WELC"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                imgurl = row[0]
            fd = urlopen("{}".format(imgurl))
            imgFile = BytesIO(fd.read())
            im = ImageTk.PhotoImage(Image.open(imgFile))
            image = Label(root, image = im)
            filemenu = Menu(menu, tearoff=False)
            usermenu = Menu(menu, tearoff=False)
            suppmenu = Menu(menu, tearoff=False)
            menu.add_cascade(label="Search", menu=filemenu)
            filemenu.add_command(label="Search User", command=menu_press_user)
            menu.add_cascade(label="Manage", menu=usermenu)
            usermenu.add_command(label="Can I promote them?", command=menu_press_can_I)
            usermenu.add_command(label="Change Rank", command=menu_press_prom)
            loginuser.grid_forget()
            loginpass.grid_forget()
            userentry.grid_forget()
            passentry.grid_forget()
            loginbutt.place_forget()
            image.pack()
            sql = "SELECT * FROM Access"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                access = int(row[0])
            if (arank >= access):
                usermenu.add_command(label="Manage Admin", command=menu_press_manage_admin)
                menu.add_cascade(label="Support", menu=suppmenu)
                suppmenu.add_command(label="Account Requests", command=menu_press_acc_reqs)
        else:
            tkMessageBox.showerror("Access Restricted", "Your account has been restricted!")
    else:
        tkMessageBox.showerror("Access Restricted", "Incorrect password!")

def rank_choose():
    root.geometry('465x65')
    global selus, reason, promby, sellab, selusr, promot, relabl, yes, box, seluse
    seluse = Entry(root)
    reason = Entry(root)
    promby = Label(root, text=usern, compound=CENTER)
    value = StringVar()
    sellab = Label(root, text='Select Rank', font="Arial 8 bold italic")
    selusr = Label(root, text='Username', font="Aria 8 bold italic")
    promot = Label(root, text='Promoter', font="Arial 8 bold italic")
    relabl = Label(root, text='Reason', font="Arial 8 bold italic")
    yes = Button(root, text="Done", command=insert_new)
    box = ttk.Combobox(root, textvariable=value, state='readonly')
    #box['values'] = ('Cadet','')
    box.current(0)
    promot.grid(column=2, row=0)
    selusr.grid(column=0, row=0)
    sellab.grid(column=1, row=0)
    seluse.grid(column=0, row=1)
    box.grid(column=1, row=1)
    promby.grid(column=2, row=1)
    reason.grid(column=3, row=1)
    relabl.grid(column=3, row=0)
    yes.grid(column=1, row=2)

def insert_new():
    global crank
    sql = "SELECT * FROM db_PROMOTIONS WHERE player = '%s'" % (usern)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        arank = row[1]
    sql = "SELECT * FROM db_RANKS WHERE rank = '%s'" % (arank)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        arank = int(row[1])
    player = seluse.get()
    rank = box.get()
    reaso = reason.get()
    timee = time.strftime("%d/%m/%y")
    sqlq = "SELECT COUNT(1) FROM db_PROMOTIONS WHERE player = '%s'" % (player)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        sql = "SELECT * FROM db_PROMOTIONS WHERE player = '%s'" % (player)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            prank = row[1]
        sql = "SELECT * FROM db_RANKS WHERE rank = '%s'" % (prank)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            prank = int(row[1])
    else:
        prank = 0
    sql = "SELECT * FROM db_RANKS WHERE rank = '%s'" % (rank)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        crank = int(row[1])
    arank = arank - 7
    cursor.execute(sqlq)
    if crank < arank:
        arank = arank + 7
        if prank < arank:
            if cursor.fetchone()[0]:
                sql = "SELECT * FROM db_PROMOTIONS WHERE player = '%s'" % (player)
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    old_ran = row[1]
                cursor.execute('''UPDATE `db_PROMOTIONS` SET `player`=%s,`new_rank`=%s,`old_rank`=%s,`promoter`=%s,`reason`=%s,`date`=%s WHERE player = %s''', (player, rank, old_ran, usern, reaso, timee, player))
                tkMessageBox.showinfo("Done", "User {} has been modified.".format(player),)
                cnx.commit()
            else:
                cursor.execute('''INSERT into db_PROMOTIONS (player, new_rank, old_rank, promoter, reason, date)
                                values (%s, %s, %s, %s, %s, %s)''',
                                (player, rank, "None", usern, reaso, timee))
                tkMessageBox.showinfo("Done", "User {} has been added.".format(player),)
                cnx.commit()
        else:
            tkMessageBox.showerror("Error", "This user is a higher rank than you.",)
    else:
        tkMessageBox.showerror("Error", "You cannot promote this user. (Rank too low)",)

def no_acc():
    global win2, habusrenr
    win2 = Toplevel(root)
    win2.geometry('250x50')
    win2.iconbitmap('Logo.ico')
    win2.resizable(width=FALSE, height=FALSE)
    win2.title("Support")
    habusrlab = Label (win2, text="Full Name")
    habusrenr = Entry (win2)
    habusrbtt = Button (win2, text="Send", command=send_acc_req)
    habusrlab.grid(column=0, row=0)
    habusrenr.grid(column=1, row=0)
    habusrbtt.place(relx=0.6, x=1, y=22.5, anchor=NE)

def send_acc_req():
    timee = time.strftime("%Y-%m-%d")
    acc = habusrenr.get()
    win2.destroy()
    sqlq = "SELECT COUNT(1) FROM db_REQ WHERE username = '%s'" % (acc)
    cursor.execute(sqlq)
    if cursor.fetchone()[0]:
        tkMessageBox.showerror("Error", "Account already requested.")
    else:
        sql = "SELECT COUNT(1) FROM db_REQ ORDER BY `username` DESC LIMIT 1"
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            idd = int(row[0])
        idd = idd + 1
        cursor.execute('''INSERT INTO `db_REQ`(`id`, `username`, `handled`, `date`)
              VALUES (%s,%s,%s,%s)''',
            (idd, acc, 0, timee))
        tkMessageBox.showinfo("Success!", "Account request send successfully. \nPlease be patient.")
    cnx.commit()

root = Tk()
root.wm_title("LSPD: Database")
root.resizable(width=FALSE, height=FALSE)
root.geometry('183x80')
root.iconbitmap('Logo.ico')
loginuser = Label(root, text="Username")
loginpass = Label(root, text="Password")
noacclabl = Label(root, text="No account?", font = "Arial 8 italic")
userentry = Entry(root)
passentry = Entry(root, show="*")
loginbutt = Button(root, text="Login", command=check_admin)
loginuser.grid(row=0)
loginpass.grid(row=1)
userentry.grid(row=0, column=1)
passentry.grid(row=1, column=1)
noacclabl.place(relx=1, x=1, y=48, anchor=E)
loginbutt.place(relx=0.6, x=1, y=54, anchor=NE)
noacclabl.bind("<Button-1>",lambda e:no_acc())

image = Label(root, text="")
userlabel = Label(root, text="")
ranklabel = Label(root, text="")
promlabel = Label(root, text="")
promotera = Label(root, text="")
oldrankal = Label(root, text="")
skine = Entry(root)
skinl = Label(root, text="Type a username")
skinb = Button(root, text="Search", command=search_user)
seluse = Entry(root)
reason = Entry(root)
promby = Label(root, text="")
value = StringVar()
sellab = Label(root, text='Select Rank')
selusr = Label(root, text='Username')
promot = Label(root, text='Promoter')
relabl = Label(root, text='Reason')
value = StringVar()
yes = Button(root, text="Done", command=insert_new)
box = ttk.Combobox(root, textvariable=value, state='readonly')
namelabel = Label(root, text="Username:", font="Arial 9 bold")
lastpromo = Label(root, text="Last Promo:", font="Arial 9 bold")
currerank = Label(root, text="Current Rank:", font="Arial 9 bold")
promoterl = Label(root, text="Promoter:", font="Arial 9 bold")
oldrankla = Label(root, text="Old Rank:", font="Arial 9 bold")
manentry = Entry(root)
manlabel = Label(root, text="Type a username")
resbutto = Button(root, text="Restrict")
susbutto = Button(root, text="Suspend")
rembutto = Button(root, text="Remove")
edpbutto = Button(root, text="Edit Password")
edubutto = Button(root, text="Edit Username")
manentry = Entry(root)
manlabel = Label(root, text="Type a username")
susbutto = Button(root, text="Suspend")
rembutto = Button(root, text="Remove", command=remove_admin)
edpbutto = Button(root, text="Edit Password", command=edit_admin_password)
edubutto = Button(root, text="Edit Username", command=edit_admin_username)
addbutto = Button(root, text="Add Admin", command=add_admin)
canla = Label(root, text="", font="Arial 100 bold ")
canie = Entry(root)
canil = Label(root, text="Type a username")
canib = Button(root, text="Can I promote them?", command=can_I_prom)
row = '---Account Requests---'

version = '1'

sql = "SELECT * FROM db_VERSION"
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
    versioon = row[0]
    urll = row[1]

atexit.register(cnx.close)

#if (version < versioon):
    #if tkMessageBox.askokcancel("Update Notice", 'This version of the program is out-dated. \nClick "OK" to be redirected to the download page.'):
        #new = 2
        #url = urll
        #webbrowser.open(url,new=new)
        #sys.exit()
    #else:
        #sys.exit()
root.mainloop()
