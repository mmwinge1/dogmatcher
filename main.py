from flask import Flask, render_template, request
import mysql.connector
import os
import math
import plotly
import json


import pandas as pd
import plotly.express as px
from decimal import *
getcontext().prec = 2

DOG_PHOTOS = os.path.join('static', 'images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DOG_PHOTOS

connection = mysql.connector.connect(
  host="34.67.216.246",
  user="root",
  password="Pups",
  database="capstone_project"
)

print("Connection Successful!")

mycursor = connection.cursor(buffered=True)

#def get_plot_data():
    #plot_data =

   # data = json.dumps(plot_data, cls=plotly.utils.plotlyJSONEncoder)
    #layout = json.dumps(plot_layout, cls=plotly.utils.plotlyJSONEncoder)

   # return data, layout

idealDog = []
allMatchFactors = []
topNMatchFactors = []
#insert(position, value), remove(value),

@app.route('/')
def display_login():
    return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
def display_login_post():
    un = request.form['u']
    pw = request.form['pw']
    mycursor.execute("SELECT * FROM users WHERE username ='" + un + "' AND password ='" + pw + "'")
    user = mycursor.fetchone()
    if user is None:
        return "The provided login information is incorrect. Please try again."
    else:
        pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'dog1.jpg')
        pic2 = os.path.join(app.config['UPLOAD_FOLDER'], 'dog2.jpg')
        pic3 = os.path.join(app.config['UPLOAD_FOLDER'], 'dog3.jpg')
        return render_template("dogmatcher.html", image_one=pic1, image_two=pic2, image_three=pic3)

#function finished
def create_histogram():
    mycursor.execute("SELECT match_count, id FROM dogs")
    rows = mycursor.fetchall()
    df = pd.DataFrame(rows)
    df.rename(columns={0: 'match_count', 1: 'dog_id'}, inplace=True)
    #match_count = df[0]
    #dogs, bins = np.histogram(rows, bins=range(0, 21, 3))
    #fig = px.histogram(df, x="match_count", nbins=7, y=dogs, labels={'x': 'total_bill', 'y': 'count'}, histnorm='probability density')
    #fig.show()

    #x = one of the columns in test?
    match_histogram = px.histogram(df, nbins=10, x='match_count', color='dog_id', labels={'match_count': 'Number of Matches', 'dog_id': 'Dog ID'}, title="Number of Matches Per Dog")
    match_histogram.show()
    return json.dumps(match_histogram, cls=plotly.utils.PlotlyJSONEncoder)

#function finished
def create_time_and_size():
    mycursor.execute("select COUNT(*) from dogs where size = 'tiny'")
    tinyCount = mycursor.fetchone()
    mycursor.execute("select sum(time_in_shelter) from dogs where size = 'tiny'")
    tinyTotal = mycursor.fetchone()
    tinyAverage = int(tinyTotal[0])/int(tinyCount[0])

    mycursor.execute("select COUNT(*) from dogs where size = 'small'")
    smallCount = mycursor.fetchone()
    mycursor.execute("select sum(time_in_shelter) from dogs where size = 'small'")
    smallTotal = mycursor.fetchone()
    smallAverage = int(smallTotal[0]) / int(smallCount[0])

    mycursor.execute("select COUNT(*) from dogs where size = 'medium'")
    mediumCount = mycursor.fetchone()
    mycursor.execute("select sum(time_in_shelter) from dogs where size = 'medium'")
    mediumTotal = mycursor.fetchone()
    mediumAverage = int(mediumTotal[0]) / int(mediumCount[0])

    mycursor.execute("select COUNT(*) from dogs where size = 'large'")
    largeCount = mycursor.fetchone()
    mycursor.execute("select sum(time_in_shelter) from dogs where size = 'large'")
    largeTotal = mycursor.fetchone()
    largeAverage = int(largeTotal[0]) / int(largeCount[0])

    mycursor.execute("select COUNT(*) from dogs where size = 'extra large'")
    extraLargeCount = mycursor.fetchone()
    mycursor.execute("select sum(time_in_shelter) from dogs where size = 'extra large'")
    extraLargeTotal = mycursor.fetchone()
    extraLargeAverage = int(extraLargeTotal[0]) / int(extraLargeCount[0])

    size_histogram = px.bar(y=[tinyAverage, smallAverage, mediumAverage, largeAverage, extraLargeAverage], x=[1,2,3,4,5], labels={'x': 'Size of Dog (Tiny=1, Small=2, Medium=3, Large=4, Extra Large=5)', 'y': 'Average Time in Shelter (Days)'}, title="Time in Shelter (Days) and Size of Dog")
    size_histogram.show()
    return json.dumps(size_histogram, cls=plotly.utils.PlotlyJSONEncoder)

#function finished
def create_scatter_time_and_age():
    mycursor.execute("SELECT time_in_shelter, age FROM dogs")
    rows = mycursor.fetchall()
    df = pd.DataFrame(rows)
    df.rename(columns={0: 'time_in_shelter', 1: 'age'})
    age_scatter = px.scatter(df, x=0, y=1, labels={'0': 'Time in Shelter (Days)', '1': 'Age of Dog'}, title="Time in Shelter (Days) and Age of Dog")
    age_scatter.show()
    return json.dumps(age_scatter, cls=plotly.utils.PlotlyJSONEncoder)


@app.route('/dogmatcher', methods=['GET', 'POST'])
def display_dogmatcher():
    find_match_factors()
    bestMatchId = allMatchFactors[9][1]
    mycursor.execute("SELECT * from dogs where id = " + str(bestMatchId))
    bestMatchData = mycursor.fetchall()
    for row in bestMatchData:
        dogNameMatch = row[1]
        genderMatch = row[2]
        sizeMatch = row[3]
        ageMatch = row[4]
        activityMatch = row[5]
        specialNeedsMatch = row[6]
        goodWithMatch = row[7]
        housetrainedMatch = row[8]
        independenceMatch = row[9]
        furColorMatch = row[10]
        eyeColorMatch = row[11]
        furTypeMatch = row[12]
        timeInShelterMatch = row[13]
        imageMatch = row[14]


    if specialNeedsMatch == 'Both':
        specialNeedsMatch = 'Medical and Behavioral'

    if goodWithMatch == 'cats':
        goodWithMatch = 'Cats'
    elif goodWithMatch == 'dogs':
        goodWithMatch = 'Other Dogs'
    elif goodWithMatch == 'catsanddogs':
        goodWithMatch = 'Cats and Dogs'
    elif goodWithMatch == 'kidsandpets':
        goodWithMatch = 'Kids and Other Pets'
    elif goodWithMatch == 'youngerkids':
        goodWithMatch = 'Kids of All Ages'
    elif goodWithMatch == 'olderkids':
        goodWithMatch = 'Older Kids Only'
    else:
        print("Good With Match Failure")

    if independenceMatch == 1:
        independenceMatch = 'I like my space'
    elif independenceMatch == 2:
        independenceMatch = 'I like a little space'
    elif independenceMatch == 3:
        independenceMatch = 'Average Independence'
    elif independenceMatch == 4:
        independenceMatch = 'I love being around you!'
    elif independenceMatch == 5:
        independenceMatch = 'I want to be with you at all times!'
    else:
        print("Independence Match Failure")


    image1 = ''
    if str(imageMatch) == 'dog1.jpg':
        image1 = 'dog1.jpg'
    elif str(imageMatch) == 'dog2.jpg':
        image1 = 'dog2.jpg'
    elif str(imageMatch) == 'dog3.jpg':
        image1 = 'dog3.jpg'
    elif str(imageMatch) == 'Bartleby.jpeg':
        image1 = 'Bartleby.jpeg'
    elif str(imageMatch) == 'Padme.jpeg':
        image1 = 'Padme.jpeg'
    elif str(imageMatch) == 'Paploo.jpeg':
        image1 = 'Paploo.jpeg'
    else:
        print("failed")
    imageMatch = os.path.join(app.config['UPLOAD_FOLDER'], image1)

    mycursor.execute("DROP TABLE IF EXISTS top_ten")
    mycursor.execute("CREATE TABLE top_ten (matchFactor decimal(10,2) not null, id int not null primary key)")
    print("Created top_ten table")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[0][0]) + ", " + str(allMatchFactors[0][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[1][0]) + ", " + str(allMatchFactors[1][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[2][0]) + ", " + str(allMatchFactors[2][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[3][0]) + ", " + str(allMatchFactors[3][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[4][0]) + ", " + str(allMatchFactors[4][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[5][0]) + ", " + str(allMatchFactors[5][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[6][0]) + ", " + str(allMatchFactors[6][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[7][0]) + ", " + str(allMatchFactors[7][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[8][0]) + ", " + str(allMatchFactors[8][1]) + ")")
    mycursor.execute("INSERT INTO top_ten (matchFactor, id) values (" + str(allMatchFactors[9][0]) + ", " + str(allMatchFactors[9][1]) + ")")
    mycursor.execute("update dogs set match_count = match_count + 1 where id = " + str(bestMatchId))
    connection.commit()
    print("Top ten matches added to top_ten table")

    return render_template("bff.html", bffPic=imageMatch, dogName=dogNameMatch, genderIdeal=genderMatch, sizeIdeal=sizeMatch, ageIdeal=ageMatch, activityLevelIdeal=activityMatch, specialNeedsIdeal=specialNeedsMatch, goodWithIdeal=goodWithMatch, housetrainedIdeal=housetrainedMatch, independenceIdeal=independenceMatch, furColorIdeal=furColorMatch, eyeColorIdeal=eyeColorMatch, furTypeIdeal=furTypeMatch, timeInShelter=timeInShelterMatch)
    #return render_template("bff.html")
    #redirect(url_for('get_bff'))

#gets the match factor and ID for all dogs in dog table and adds all match factors to allMatchFactors list
def find_match_factors():
    mycursor.execute("select * from dogs")
    allDogs = mycursor.fetchall()
    print("Total dogs in shelter:  ", len(allDogs))
    gender1 = request.form.get('genderHTML')
    print("Ideal Gender: " + str(gender1))
    genderSliderFactor = request.form.get('genderSlider')
    print("Gender Slider: " + str(genderSliderFactor))
    size1 = request.form.get('size')
    sizeStr = str(size1)
    print("Ideal Size: " + sizeStr)
    sizeSliderFactor = request.form.get('sizeSlider')
    print("Size Slider: " + str(sizeSliderFactor))
    age1 = request.form.get('age')
    print("Ideal Age: " + age1)
    ageSliderFactor = request.form.get('ageSlider')
    print("Age Slider: " + str(ageSliderFactor))
    activityLevel1 = request.form.get('activityLevel')
    activityLevelStr = str(activityLevel1)
    print("Ideal Activity Level: " + activityLevelStr)
    activitySliderFactor = request.form.get('activitySlider')
    print("Activity Level Slider: " + str(activitySliderFactor))
    specialNeeds1 = request.form.get('specialNeeds')
    print("Ideal Special Needs: " + specialNeeds1)
    specialNeedsSliderFactor = request.form.get('specialNeedsSlider')
    print("Special Needs Slider: " + str(specialNeedsSliderFactor))
    goodWith1 = request.form.get('goodWith')
    print("Ideal Good With: " + goodWith1)
    goodWithSliderFactor = request.form.get('goodWithSlider')
    print("Good With Slider: " + str(goodWithSliderFactor))
    housetrained1 = request.form.get('housetrained')
    print("Ideal Housetrained: " + housetrained1)
    housetrainedSliderFactor = request.form.get('housetrainedSlider')
    print("Housetrained Slider: " + str(housetrainedSliderFactor))
    independence1 = request.form.get('independenceLevel')
    independenceStr = str(independence1)
    print("Ideal Independence Level: " + independence1)
    independenceSliderFactor = request.form.get('independenceSlider')
    print("Independence Slider: " + str(independenceSliderFactor))
    furColor1 = request.form.get('furColor')
    print("Ideal Fur Color: " + furColor1)
    furColorSliderFactor = request.form.get('furColorSlider')
    print("Fur Color Slider: " + str(furColorSliderFactor))
    eyeColor1 = request.form.get('eyeColor')
    print("Ideal Eye Color: " + eyeColor1)
    eyeColorSliderFactor = request.form.get('eyeColorSlider')
    print("Eye Color Slider: " + str(eyeColorSliderFactor))
    furType1 = request.form.get('furType')
    print("Ideal Fur Type: " + furType1)
    furTypeSliderFactor = request.form.get('furTypeSlider')
    print("Fur Type Slider: " + str(furTypeSliderFactor))
    for row in allDogs:
        matchFactor = 0
        dogId = row[0]
        genderValue = row[2]
        sizeValue = row[3]
        ageValue = row[4]
        activityValue = row[5]
        specialNeedsValue = row[6]
        goodWithValue = row[7]
        housetrainedValue = row[8]
        independenceValue = row[9]
        furColorValue = row[10]
        eyeColorValue = row[11]
        furTypeValue = row[12]
        timeInShelterValue = row[13]

   #gender algorithm complete
        if gender1 == 'dm':
            matchFactor = matchFactor + 10
        elif gender1 == genderValue:
            matchFactor = matchFactor + (10 * int(genderSliderFactor))
            #matchFactor = matchFactor + 10
            #print(genderSliderFactor)

    #size algorithm complete
        if size1 == 'dm':
            matchFactor = matchFactor + 10
        elif size1 == sizeValue:
            matchFactor = matchFactor + (10 * int(sizeSliderFactor))
        elif size1 == 'Tiny':
            if sizeValue == 'Small':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Medium':
                matchFactor = matchFactor + (2 * int(sizeSliderFactor))
        elif size1 == 'Small':
            if sizeValue == 'Tiny':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Medium':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Large':
                matchFactor = matchFactor + (2 * int(sizeSliderFactor))
        elif size1 == 'Medium':
            if sizeValue == 'Small':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Large':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
        elif size1 == 'Large':
            if sizeValue == 'Extra Large':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Medium':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Small':
                matchFactor = matchFactor + (2 * int(sizeSliderFactor))
        elif size1 == 'Extra Large':
            if sizeValue == 'Large':
                matchFactor = matchFactor + (5 * int(sizeSliderFactor))
            elif sizeValue == 'Medium':
                matchFactor = matchFactor + (2 * int(sizeSliderFactor))
        else:
            print("Size Type: Error")

    #age algorithm complete
        if age1 == 'dm':
            matchFactor = matchFactor + 10
        elif int(age1) == ageValue:
            matchFactor = matchFactor + (10 * int(ageSliderFactor))
        else:
            difference = int(age1) - ageValue
            difference = difference * difference
            difference = math.sqrt(difference)
            if difference <= 1:
                matchFactor = matchFactor + (7 * int(ageSliderFactor))
            elif difference <= 2:
                matchFactor = matchFactor + (5 * int(ageSliderFactor))
            elif difference <= 3:
                matchFactor = matchFactor + (2 * int(ageSliderFactor))
            elif difference <= 4:
                matchFactor = matchFactor + (1 * int(ageSliderFactor))


    #activityLevel algorithm complete
        if activityLevel1 == 'dm':
            matchFactor = matchFactor + 10
        elif activityLevel1 == activityValue:
            matchFactor = matchFactor + (10 * int(activitySliderFactor))
        elif activityLevel1 == 'Low':
            if activityValue == 'Medium':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
        elif activityLevel1 == 'Medium':
            if activityValue == 'Low':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
            elif activityValue == 'High':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
        elif activityLevel1 == 'High':
            if activityValue == 'Medium':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
        else:
            print("Activity Level: Error")

    #specialNeeds algorithm complete
        if specialNeeds1 == 'dm':
            matchFactor = matchFactor + 10
        elif specialNeeds1 == specialNeedsValue:
            matchFactor = matchFactor + (10 * int(specialNeedsSliderFactor))
        elif specialNeedsValue == 'None':
            matchFactor = matchFactor + (10 * int(specialNeedsSliderFactor))

    #goodWith algorithm complete
        if goodWith1 == 'dm':
            matchFactor = matchFactor + 10
        elif goodWith1 == goodWithValue:
            matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
        elif goodWith1 == 'olderkids':
            if goodWithValue == 'youngerkids':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
            elif goodWithValue == 'kidsandpets':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
        elif goodWith1 == 'youngerkids':
            if goodWithValue == 'kidsandpets':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
            if goodWithValue == 'olderkids':
                matchFactor = matchFactor + (4 * int(goodWithSliderFactor))
        elif goodWith1 == 'cats':
            if goodWithValue == 'kidsandpets':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
            elif goodWithValue == 'catsanddogs':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
        elif goodWith1 == 'dogs':
            if goodWithValue == 'kidsandpets':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
            elif goodWithValue == 'catsanddogs':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))
        elif goodWith1 == 'catsanddogs':
            if goodWithValue == 'kidsandpets':
                matchFactor = matchFactor + (10 * int(goodWithSliderFactor))

    #housetrained algorithm complete
        if housetrained1 == 'dm':
            matchFactor = matchFactor + 10
        elif housetrained1 == housetrainedValue:
            matchFactor = matchFactor + (10 * int(housetrainedSliderFactor))

    #independence algorithm complete
        if independence1 == 'dm':
            matchFactor = matchFactor + 10
        elif int(independence1) == independenceValue:
            matchFactor = matchFactor + (10 * int(independenceSliderFactor))
        else:
            difference = int(independence1) - independenceValue
            difference = difference * difference
            difference = math.sqrt(difference)
            if difference <= 1:
                matchFactor = matchFactor + (7 * int(independenceSliderFactor))
            elif difference <= 2:
                matchFactor = matchFactor + (5 * int(independenceSliderFactor))
            elif difference <= 3:
                matchFactor = matchFactor + (1 * int(independenceSliderFactor))

    #furColor algorithm complete
        if furColor1 == 'dm':
            matchFactor = matchFactor + 10
        elif furColor1 == furColorValue:
            matchFactor = matchFactor + (10 * int(furColorSliderFactor))

    #eyeColor algorithm complete
        if eyeColor1 == 'dm':
            matchFactor = matchFactor + 10
        elif eyeColor1 == eyeColorValue:
            matchFactor = matchFactor + (10 * int(eyeColorSliderFactor))

    #furtype algorithm complete
        if furType1 == 'dm':
            matchFactor = matchFactor + 10
        elif furType1 == furTypeValue:
            matchFactor = matchFactor + (10 * int(furTypeSliderFactor))
        elif furType1 == 'Short':
            if furTypeValue == 'Medium':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
        elif furType1 == 'Medium':
            if furTypeValue == 'Short':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
            elif furTypeValue == 'Long':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
        elif furType1 == 'Long':
            if furTypeValue == 'Medium':
                matchFactor = matchFactor + (5 * int(furTypeSliderFactor))
        else:
            print("Fur Type: Error")

        timeInShelterBuff = int(timeInShelterValue)/100
        #timeInShelterBuff = Decimal(timeInShelterBuff)
        #matchFactor = Decimal(matchFactor)
        matchFactor = matchFactor + timeInShelterBuff
        #matchFactor = float(matchFactor)
        allMatchFactors.insert(0, [matchFactor, dogId])
    allMatchFactors.sort()
    while len(allMatchFactors) > 10:
        allMatchFactors.pop(0)
    print(allMatchFactors)
    return allMatchFactors


@app.route('/tryagain', methods=['POST'])
def try_again():
    topTenList = []
    mycursor.execute("SELECT * from top_ten")
    topTen = mycursor.fetchall()
    for row in topTen:
        matchFactor = row[0]
        dogId = row[1]
        #insert(position, value)
        topTenList.insert(0, [matchFactor, dogId])
    topTenList.sort()
    topTenList.reverse()
    mycursor.execute("DELETE from top_ten where id = " + str(topTenList[0][1]))
    connection.commit()
    print("Top dogs: " + str(topTenList))
    topTenList.pop(0)
    print("New top dogs: " + str(topTenList))

    mycursor.execute("select exists(select 1 from top_ten) as Output")
    topTenCount = mycursor.fetchone()
    topTenCount = str(topTenCount)
    print(topTenCount)
    if topTenCount == "(0,)":
        return "It doesn't look like we have what you're searching for! Try updating your requirements on the Dog Matcher page, or check back in a few days. New dogs are added regularly."
    else:
        bestMatchId = topTenList[0][1]
        mycursor.execute("SELECT * from dogs where id = " + str(bestMatchId))
        bestMatchData = mycursor.fetchall()
        for row in bestMatchData:
            dogNameMatch = row[1]
            genderMatch = row[2]
            sizeMatch = row[3]
            ageMatch = row[4]
            activityMatch = row[5]
            specialNeedsMatch = row[6]
            goodWithMatch = row[7]
            housetrainedMatch = row[8]
            independenceMatch = row[9]
            furColorMatch = row[10]
            eyeColorMatch = row[11]
            furTypeMatch = row[12]
            timeInShelterMatch = row[13]
            imageMatch = row[14]

        mycursor.execute("update dogs set match_count = match_count + 1 where id = " + str(bestMatchId))
        connection.commit()

        if goodWithMatch == 'cats':
            goodWithMatch = 'Cats'
        elif goodWithMatch == 'dogs':
            goodWithMatch = 'Other Dogs'
        elif goodWithMatch == 'catsanddogs':
            goodWithMatch = 'Cats and Dogs'
        elif goodWithMatch == 'kidsandpets':
            goodWithMatch = 'Kids and Other Pets'
        elif goodWithMatch == 'youngerkids':
            goodWithMatch = 'Kids of All Ages'
        elif goodWithMatch == 'olderkids':
            goodWithMatch = 'Older Kids Only'
        else:
            print("Good With Match Failure")

        if specialNeedsMatch == 'Both':
            specialNeedsMatch = 'Medical and Behavioral'

        if independenceMatch == 1:
            independenceMatch = 'I like my space'
        elif independenceMatch == 2:
            independenceMatch = 'I like a little space'
        elif independenceMatch == 3:
            independenceMatch = 'Average Independence'
        elif independenceMatch == 4:
            independenceMatch = 'I love being around you!'
        elif independenceMatch == 5:
            independenceMatch = 'I want to be with you at all times!'
        else:
            print("Independence Match Failure")

        image1 = ''
        if str(imageMatch) == 'dog1.jpg':
            image1 = 'dog1.jpg'
        elif str(imageMatch) == 'dog2.jpg':
            image1 = 'dog2.jpg'
        elif str(imageMatch) == 'dog3.jpg':
            image1 = 'dog3.jpg'
        elif str(imageMatch) == 'Bartleby.jpeg':
            image1 = 'Bartleby.jpeg'
        elif str(imageMatch) == 'Padme.jpeg':
            image1 = 'Padme.jpeg'
        elif str(imageMatch) == 'Paploo.jpeg':
            image1 = 'Paploo.jpeg'
        else:
            print("failed")
        imageMatch = os.path.join(app.config['UPLOAD_FOLDER'], image1)
        return render_template("bff.html", bffPic=imageMatch, dogName=dogNameMatch, genderIdeal=genderMatch,
                               sizeIdeal=sizeMatch, ageIdeal=ageMatch, activityLevelIdeal=activityMatch,
                               specialNeedsIdeal=specialNeedsMatch, goodWithIdeal=goodWithMatch,
                               housetrainedIdeal=housetrainedMatch, independenceIdeal=independenceMatch,
                               furColorIdeal=furColorMatch, eyeColorIdeal=eyeColorMatch, furTypeIdeal=furTypeMatch,
                               timeInShelter=timeInShelterMatch)




@app.route('/bff', methods=['GET', 'POST'])
def get_bff():
        mycursor.execute("SELECT image FROM dogs WHERE id = 98615")
        image = mycursor.fetchone()
        image1 = ''
        if str(image) == "('dog1.jpg',)":
            image1 = 'dog1.jpg'
        elif str(image) == "('dog2.jpg',)":
            image1 = 'dog2.jpg'
        elif str(image) == "('dog3.jpg',)":
            image1 = 'dog3.jpg'
        else:
            print("failed")

        bffPic1 = os.path.join(app.config['UPLOAD_FOLDER'], image1)
        mycursor.execute("SELECT gender FROM idealdog WHERE id = 1")
        genderIdeal1 = mycursor.fetchone()
        print("Gender Ideal: " + genderIdeal1)
        return render_template("bff.html", bffPic=bffPic1, genderIdeal=genderIdeal1)

@app.route('/employeeLogin')
def display_employee_login():
    return render_template("employeeLogin.html")

@app.route('/employeeLogin', methods=['GET', 'POST'])
def display_employee_login_post():
    eun = request.form['eu']
    epw = request.form['epw']
    mycursor.execute("SELECT * FROM users WHERE username ='" + eun + "' AND password ='" + epw + "' AND type = 'Employee'")
    euser = mycursor.fetchone()
    if euser is None:
        return "The provided login information is incorrect. Please try again."
    else:
        return render_template("dashboard.html")

@app.route('/dashboard', methods=['GET', 'POST'])
def display_dashboard():
    return render_template("dashboard.html")

@app.route('/adopt', methods=['GET', 'POST'])
def display_adopt():
    return render_template("adopt.html")

@app.route('/matchesPerDog', methods=['GET', 'POST'])
def display_matches_per_dog():
    fig = create_histogram()
    return render_template("matchesPerDog.html", fig=fig)

@app.route('/timeAndSize', methods=['GET', 'POST'])
def display_time_and_size():
    fig = create_time_and_size()
    return render_template("timeAndSize.html", fig=fig)

@app.route('/timeAndAge', methods=['GET', 'POST'])
def display_time_and_age():
    fig = create_scatter_time_and_age()
    return render_template("timeAndAge.html", fig=fig)

if __name__ == "__main__":
    app.run(debug=True)
    print("print")