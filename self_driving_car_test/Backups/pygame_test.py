import os

countFolder = 0

myDirectory = os.path.join(os.getcwd(), 'DataCollected')
while os.path.exists(os.path.join(myDirectory,f'IMG{str(countFolder)}')):
        countFolder += 1
newPath = myDirectory +"/IMG"+str(countFolder)
os.makedirs(newPath)
print(myDirectory)
