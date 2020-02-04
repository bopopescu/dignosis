from flask import Flask,render_template,request
import mysql.connector
import numpy as np
from numpy import genfromtxt
from sklearn import linear_model

lr=linear_model.LogisticRegression()
dic={}
val=''



app = Flask(__name__)


@app.route('/')
def diag():
    return render_template("index.html")
@app.route('/loadm')
def diag1():
    return render_template("logadmin.html")
@app.route('/regpat')
def diag2():
    return render_template("regpatient.html")
@app.route('/logpat')
def diag3():
    return render_template("logpatient.html")

@app.route('/inppat')
def diag4():
    return render_template("panel1.html")

@app.route('/inppat1')
def diag10():
    return render_template("panel2.html")

@app.route('/final1')
def diag12():
    return render_template("final.html")





@app.route('/regpatient',methods=["POST"])
def diag5():
    name = str(request.form['name'])
    email = str(request.form['email'])
    Pass = str(request.form['pwd'])
    Repe = str(request.form['pwdrep'])


    con = mysql.connector.connect(host="localhost",user="root",password="",db="didb")

    cur = con.cursor()
    cur.execute("insert into 1table values ('"+name+"','"+email+"','"+Pass+"','"+Repe+"')")
    con.commit()

    return render_template("index.html")

@app.route('/logpatient',methods=["POST"])
def diag6():
    Email = request.form['email']
    Pass = request.form['pwd']
    print(Email,Pass)

    con = mysql.connector.connect(host="localhost",user="root",password="",db="didb")

    cursor = con.cursor()
    cursor.execute("select * from 1table where email = '"+Email+"' and pass = '"+Pass+"'  ")
    if cursor.fetchone():
        return render_template("panel2.html")
    else:
        return render_template("index.html")

@app.route('/logadm',methods=["POST"])
def diag8():
    name = request.form['email']
    Pass = request.form['pwd']

    if name=="navneet" and Pass =="agarwal":
        return render_template("panel1.html")
    else:
        return render_template("index.html")

@app.route('/panelpat',methods=["POST"])
def diag7():
    pulserate = str(request.form['pul'])
    minimumbp = str(request.form['minbp'])
    maximumbp = str(request.form['maxbp'])
    cc = str(request.form['cc'])
    headache = str(request.form['headache'])
    disease = str(request.form['disease'])


    con = mysql.connector.connect(host="localhost",user="root",password="",db="didb")

    cur = con.cursor()
    cur.execute("insert into 2table values ('"+pulserate+"','"+minimumbp+"','"+maximumbp+"','"+cc+"','"+headache+"','"+disease+"')")
    con.commit()

    import csv

    csvData = [(pulserate , minimumbp , maximumbp , cc , headache , disease)]
    with open('hospital.csv','a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)

    csvFile.close()
    return render_template("panel1.html")

'''@app.route('/panelpat1',methods=["POST"])
def diag11():
    pulserate = str(request.form['pul'])
    minimumbp = str(request.form['minbp'])
    maximumbp = str(request.form['maxbp'])
    cc = str(request.form['cc'])
    headache = str(request.form['headache'])


    con = mysql.connector.connect(host="localhost",user="root",password="",db="didb")

    cur = con.cursor()
    cur.execute("insert into 2table values ('"+pulserate+"','"+minimumbp+"','"+maximumbp+"','"+cc+"','"+headache+"')")
    con.commit()
'''
@app.route('/datatrain')
def datatrain():
    print("hi")
    file=(genfromtxt("hospital.csv",delimiter=',',dtype='str'))
    global lr
    global dict
    print("hi")

    count=0
    for val in file:
        if val[5] not in dic:
            dic[val[5]]=count
            count+=1
    print("hi")
    for val in file:
        val[5]=dic[val[5]]

    print(file)

    trainingset=file
    testingset=file[1:]

    trainingx=trainingset[:,[0,1,2,3,4]]
    trainingx=trainingx.astype(float)
    trainingy=trainingset[:,[5]]
    lr.fit(trainingx,trainingy)
    print("prediction successfull")

@app.route('/final',methods=["POST"])
def checkpge():
    print("hi")
    lis = []
    lis.insert(0,  int(request.form["pul"]))
    lis.insert(1, int(request.form["minbp"]))
    lis.insert(2, int(request.form["maxbp"]))
    lis.insert(3, int(request.form["cc"]))
    lis.insert(4, int(request.form["headache"]))
    datatrain()
    print("jj")
    global lr
    global dic
    a=int(lr.predict([lis]))
    print("hh2")
    global val
    z=0
    for x in dic:
        if(dic[x] == a):
            print("you might suffering from %s" %x)
            z=x
    print(z)

    return render_template("final.html",val1=z)

if __name__ == '__main__':
    app.run()




