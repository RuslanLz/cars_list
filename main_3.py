import os
import json
import tkinter
from tkinter import *
from tkinter import ttk
import copy

class Car():

    __mainAttrs = {
        "mass": float,
        "color": str,
        "doorCount": int,
        "fuelTankCapacity": float,
        "fuelType": str,
        "lightsIsOn":bool
    }
    def __init__(self, car:dict):
        for key in car:
            self.__setattr__(key, car[key])
    @classmethod
    def enterNewCar(cls, id:int):
        attrDict={}
        attrDict["id"]=id
        for key in cls.__mainAttrs:
            if key == "id":
                continue
            print(f"введите {key}:")
            if cls.__mainAttrs[key]==bool:
                print(key+" (да/нет):")
                while True:
                    inp=input()
                    if inp=="да" or inp=="нет":
                        attrDict[key]=inp
                        break
                    else:
                        print("некорректное значение, введите \"да\" или \"нет\"")
            else:
                while True:
                    try:
                        attrDict[key]=cls.__mainAttrs[key](input())
                        break
                    except:
                        print("некорректное значение, попробуйте снова")
        print("введите доп. информацию:")
        attrDict["extraInfo"]=input()
        return cls(attrDict)
    @classmethod
    def getMainAttrs(cls):
        return cls.__mainAttrs


    def changeProperty(self, property, newValue):
        if property == "id":
            return "нельзя изменять id"
        elif property=="extraInfo":
            self.__setattr__(property, newValue)
            return True
        elif hasattr(self, property):
            if Car.__mainAttrs[property] == bool:
                if newValue == "да" or newValue == "нет":
                    self.__setattr__(property, newValue)
                    return True
                return "некорректный ввод, введите \"да\" или \"нет\""
            try:
                self.__setattr__(property, type(self.__getattribute__(property))(newValue))
                return True
            except:
                return "некорректное значение для свойства"
        else:
            return "такого свойства не существует"


def getNewID(cars) ->int:
    maxID=0
    print(cars)
    for i in cars:
        maxID=max(maxID, i.id)
    return maxID+1


def getCarsIndexById(id:int, cars):
    for i in range(len(cars)):

        if cars[i].id==id:
            print(i, cars[i].id, 222)
            return i
    return "False"


def showCars(cars):
    for i in cars:
        print(vars(i))
"""
def addCar():
    def add():
        for i in fields:
            i[2].grid_forget()
        newCar={}
        newCar["id"]=getNewID(cars)
        isSuccess=True
        attrs=list(Car.getMainAttrs().values())

        for i in range(len(attrs)):
            if fields[i][1].get()=="":
                isSuccess=False
                fields[i][2].grid(row=i + 1, column=3)
                continue
            if attrs[i]==bool:
                if fields[i][1].get()=="да" or fields[i][1].get()=="нет":
                    newCar[fields[i][0].cget('text')]=fields[i][1].get()
                    continue
                else:
                    isSuccess=False
                    fields[i][2].grid(row=i + 1, column=3)
                    continue
            try:
                newCar[fields[i][0].cget('text')]=attrs[i](fields[i][1].get())
            except:
                print(attrs[i], fields[i][1].get())
                isSuccess=False
                fields[i][2].grid(row=i+1,column=3)
        newCar["extraInfo"]=fields[len(fields)-1][1].get()
        if isSuccess==True:
            cars.append(Car(newCar))
            updateTable()
            open("cars.txt", "w").write(json.dumps([vars(i) for i in cars]))
            changeWindow.destroy()

    changeWindow=Tk()
    fields = []
    for i in Car.getMainAttrs():
        if i == "id":
            continue
        field = []
        fields.append(field)
        field.append(Label(changeWindow, text=i))
        field[0].grid(in_=changeWindow, row=len(fields), column=1)
        field.append(Entry(changeWindow))
        field[1].grid(in_=changeWindow, row=len(fields), column=2)
        field.append(Label(changeWindow, text="-некорректное значение", fg='red'))
    fields.append([Label(changeWindow,text="extraInfo"),Entry(changeWindow),Label(changeWindow,text="-некорректное значение",fg='red')])
    print(fields)
    fields[len(fields)-1][0].grid(in_=changeWindow,row=len(fields),column=1)
    fields[len(fields) - 1][1].grid(in_=changeWindow,row=len(fields), column=2)
    fields[len(fields) - 1][2].grid_forget()

    Button(changeWindow, text="добавить", command=add).grid(row=1, column=4)
    Button(changeWindow, text="отмена").grid(row=2, column=4)
    changeWindow.mainloop()

def changeCar(a):
    def close():
        changeWindow.destroy()
    def deleteCar():
        cars.pop(carId)
        open("cars.txt", "w").write(json.dumps([vars(i) for i in cars]))
        updateTable()
        changeWindow.destroy()
    def acceptChanges():
        nonlocal carObj
        print(carObj,cars[getCarsIndexById(table.item(table.focus())["values"][0],cars)])
        for i in fields:
            i[2].grid_forget()
        testCar=copy.deepcopy(carObj)
        isSuccess=True
        for i in fields:
            result=testCar.changeProperty(i[0].cget('text'),i[1].get())
            if result!=True:
                isSuccess=False
                i[2].config(text="-"+result)
                i[2].grid(row=fields.index(i)+1,column=3)
        if isSuccess==True:
            cars[cars.index(carObj)]=testCar
            open("cars.txt", "w").write(json.dumps([vars(i) for i in cars]))
            updateTable()
            changeWindow.destroy()

    changeWindow=Tk()
    carId=getCarsIndexById(table.item(table.focus())["values"][0],cars)
    carObj=cars[carId]
    car=vars(carObj)
    fields=[]
    for i in car:
        if i=="id":
            continue
        field=[]
        fields.append(field)
        field.append(Label(changeWindow,text=i))
        field[0].grid(in_=changeWindow, row=len(fields), column=1)
        field.append(Entry(changeWindow))
        field[1].insert(0,str(car[i]))
        field[1].grid(in_=changeWindow,row=len(fields),column=2)
        field.append(Label(changeWindow,text="-некорректное значение", fg='red'))
        field[2].grid_forget()

    Button(changeWindow,text="удалить машину",command=deleteCar).grid(row=1,column=4)
    Button(changeWindow,text="принять изменения",command=acceptChanges).grid(row=2, column=4)
    Button(changeWindow,text="отмена",command=close).grid(row=3, column=4)
    changeWindow.mainloop()

def updateTable():
    global table

    table.destroy()
    table = ttk.Treeview(show="headings", selectmode="browse")

    heads = list(Car.getMainAttrs().keys())
    heads.insert(0, 'id')
    heads.append('extraInfo')
    table['columns'] = heads

    table.bind("<Double-1>", changeCar)

    for i in heads:
        table.heading(i, text=i, anchor='center')
        table.column(i, anchor='center', width=1, stretch=True)

    for i in cars:
        table.insert('', tkinter.END, values=list(vars(i).values()))
    table.place(relheight=1, relwidth=0.6, x=300)

"""

cars=[]
if os.path.exists("cars.txt") == True :
    if open("cars.txt","r").read()!="":
        cars=[Car(i) for i in json.load(open("cars.txt", "r"))]
else:
    open("cars.txt", "x")
"""
window = Tk()
window.resizable(width=True, height=True)
window.minsize(width=1000,height=400)
table=ttk.Treeview()
updateTable()

buttons_frame=Frame()
buttons_frame.place(relx=0,width=300)
Button(buttons_frame,text="добавить",font="Times 12",command=addCar).grid(row=0,pady=15,column=1)
Button(buttons_frame,text="найти",font="Times 12").grid(row=0,column=2)
Label(buttons_frame,text="двойное нажатие по элементу\n для изменения/удаления",font="Times 17").grid(row=1,column=1,columnspan=2)



window.mainloop()
"""
while True:

    showCars(cars)
    print("напишите \"добавить\"/\"удалить\"/\"изменить\" машину в списке или \"завершить\"")
    inp = input()
    if inp == "добавить":
        cars.append(Car.enterNewCar(getNewID(cars)))

    elif inp == "удалить":
        while True:
            print("введите id удаляемой машины или \"отмена\":")
            value=input()
            if value=="отмена":
                break
            elif getCarsIndexById(int(value), cars) != "False":
                cars.pop(getCarsIndexById(int(value), cars))
                print("готово!")
                break
            else:
                print("несуществующий id или некорректный ввод, попробуйте ещё")
    elif inp=="завершить":
        break
    elif inp=="изменить":
        while True:
            print("введите id измениемой машины, название изменяемого свойства и его новое значение через пробел или \"отмена\":")
            changeInput=input()

            if changeInput=="отмена":
                break
            changeInput=changeInput.split()
            try:
                int(changeInput[0])
            except:
                print("некрорректный ввод, попробуйте снова", 2)
                continue
            if len(changeInput)==3 and getCarsIndexById(int(changeInput[0]), cars) != "False":
                result = cars[getCarsIndexById(int(changeInput[0]), cars)].changeProperty(changeInput[1],changeInput[2])
                if result == True:
                    print("готово!")
                    break
                else:
                    print(result+", попробуйте снова")
            else:
                print("некорректный ввод, попробуйте снова")


    open("cars.txt", "w").write(json.dumps([vars(i) for i in cars]))


mainloop()

