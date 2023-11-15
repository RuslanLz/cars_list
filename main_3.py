import os
import json


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

cars=[]
if os.path.exists("cars.txt") == True :
    if open("cars.txt","r").read()!="":
        cars=[Car(i) for i in json.load(open("cars.txt", "r"))]
else:
    open("cars.txt", "x")

while True:

    showCars(cars)
    print("напишите \"добавить\"/\"удалить\"/\"изменить\" машину в списке или \"завершить\"!")
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

