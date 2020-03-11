import matplotlib.pyplot as plt
import re
import lxml.html as lh
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Set our initial page to open:
url = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
html = urlopen(url)

# Quick explanation of what the user is to expect:
print()
print("FOMC Projections Database.")
print("Enter a year followed by month to view 5 comparison plots.")
print("This will also save one image of each individual plot.")
print()
        
# Let's make a function that asks the user for the date:
def askDate():

    # First we ask for a year input from the user:
    global Year
    Year  = input("What year would you like to search? (eg: 2016): ")

    # A simple check to see if we have a valid input as we can only do the years from 2014 to 2019:
    while(Year!="2019" and Year!="2018" and Year!="2017" and Year!="2016" and Year !="2015" and Year!="2014"):
        print()
        print("Sorry, that is not a valid year.")
        print("Please input a year from 2014 to 2019.")
        print("Please do not add any spaces before or after your input.")
        print()
        Year  = input("What year would you like to search? (eg: 2016): ")

    # Same thing for the month:
    global Month
    Month = input("What month of " + Year + " would you like to search? (03, 06, 09 or 12): ")

    while(Month!="03" and Month!="06" and Month!="09" and Month!="12"):
        print()
        print("Sorry, that is not a valid month.")
        print("Please input a month from the options of 03, 06, 09 or 12.")
        print("Please do not add any spaces before or after your input.")
        print()
        Month = input("What month of " + Year + " would you like to search? (eg: 03, 06, 09 or 12): ")

    # Make a variable that takes both the year and month to create a date:
    global Date
    Date = Year + Month

    # Check against dates which haven't been released yet:
    while(Date=="201906" or Date=="201909" or Date=="201912"):
        print()
        print("Sorry, the projections for that month has not been released yet.")
        print("Please input the month 03 for 2019.")
        print()
        Month = input("What month of " + Year + " would you like to search? (Only 03 is available for 2019): ")
        Date = Year + Month

    # Finally we ask if the input date is correct:
    Correct = input("Is '" + Year + " " + Month  + "' the date you would like to search? (Y/N): ")

    while(Correct!="y" and Correct!="Y" and Correct!="n" and Correct!="N"):
        print()
        print("Sorry, please just enter either Y or N.")
        print("Please do not add any spaces before or after your input.")
        print()
        Correct = input("Is '" + Year + " " + Month  + "' the date you would like to search? (Y/N): ")
            
    # If the user has input a different date, the process starts over:
    if(Correct!="Y" and Correct!="y"):
        print()
        print("Okay, let's start again.")
        print()
        askDate()

# Run our function to get our date from the user to use to search later:
askDate()

soup = BeautifulSoup(html, 'lxml')

# Search for the requested HTML page from the input date: 
dateLink = soup.find("a", text="HTML", href= re.compile("/monetarypolicy/fomcprojtabl" + Date))
dateLink2 = dateLink.get("href")

# This gives us the full url to use:
dateLink3 = "https://www.federalreserve.gov" + dateLink2

# Open and read in our new requested url:
html2 = urlopen(dateLink3)
soup2 = BeautifulSoup(html2, "lxml")
table = soup2.find("table")

# This works and finds all the input data for the table we want:
output_rows = []
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')
    output_row = []
    for column in columns:
        output_row.append(column.text)
    output_rows.append(output_row)

# Time to plot our graph.
# Let's do our X-axis first.
# This is fairly simple as all we do is add the years:
YearInt = int(Year)
x       = [YearInt, YearInt+1, YearInt+2, "Longer run"]

# Evaluates previous meeting date:
prevMon  = ""
prevYear = str(YearInt)

if(Month=="03"):
    prevMon = "12"
if(Month=="12"):
    prevMon = "09"
if(Month=="09"):
    prevMon = "06"
if(Month=="06"):
    prevMon = "03"

if(Month=="03"):
    prevYear = str(YearInt-1)


# Let's move onto our Y-axis.
# As we want to do all 5 measures, we're going to need 10 Y-axis.
# This is because we want to compare to the previous meeting too.
# When I name the Y-axis, I am going to use "this..." to mean this meeting. 
# Similarly I will use "last..." to represent last meeting projections.

# Once I have obtained the Y values for our plot, I will create the plot right below and save it:

# Change in Real GDP:
thisGdp = []
lastGdp = []

i=0
for vals in output_rows[2]:
    if(i<4):
        valint = float(vals)
        thisGdp.append(valint)
    i+=1

j=0
for vals in output_rows[3]:
    if(j<4):
        valint = float(vals)
        lastGdp.append(valint)
    j+=1

plt.figure(1)
plt.title( "Change in real GDP")
plt.plot(x, thisGdp, label = Year + "-" + Month, marker='o', markersize=8)
plt.plot(x, lastGdp, label = prevYear + "-" + prevMon, linestyle='dashed', marker='o', markersize=8)
plt.legend()
plt.savefig('Change in real GDP ' + Year + "-" + Month)

# Unemployment rate:
thisUR = []
lastUR = []

i=0
for vals in output_rows[4]:
    if(i<4):
        valint = float(vals)
        thisUR.append(valint)
    i+=1

j=0
for vals in output_rows[5]:
    if(j<4):
        valint = float(vals)
        lastUR.append(valint)
    j+=1

plt.figure(2)
plt.title( "Unemployment rate")
plt.plot(x, thisUR, label = Year + "-" + Month, marker='o', markersize=8)
plt.plot(x, lastUR, label = prevYear + "-" + prevMon, linestyle='dashed', marker='o', markersize=8)
plt.legend()
plt.savefig('Unemployment rate ' + Year + "-" + Month)

# PCE inflation:
thisPCE = []
lastPCE = []

i=0
for vals in output_rows[6]:
    if(i<4):
        valint = float(vals)
        thisPCE.append(valint)
    i+=1

j=0
for vals in output_rows[7]:
    if(j<4):
        valint = float(vals)
        lastPCE.append(valint)
    j+=1


plt.figure(3)
plt.title( "PCE inflation")
plt.plot(x, thisPCE, label = Year + "-" + Month, marker='o', markersize=8)
plt.plot(x, lastPCE, label = prevYear + "-" + prevMon, linestyle='dashed', marker='o', markersize=8)
plt.legend()
plt.savefig('PCE inflation ' + Year + "-" + Month)

# Core PCE inflation:
thisCPCE = []
lastCPCE = []

# We create xC as the Core PCE inflation category does not use the Longer run.
# Also change the years to strings so we don't get intermediate x values such as 2019.25:
fst = str(YearInt)
snd = str(YearInt+1)
trd = str(YearInt+2)
xC  = [fst, snd, trd]

i=0
for vals in output_rows[8]:
    if(i<3):
        valint = float(vals)
        thisCPCE.append(valint)
    i+=1

j=0
for vals in output_rows[9]:
    if(j<3):
        valint = float(vals)
        lastCPCE.append(valint)
    j+=1

plt.figure(4)
plt.title( "Core PCE inflation")
plt.plot(xC, thisCPCE, label = Year + "-" + Month, marker='o', markersize=8)
plt.plot(xC, lastCPCE, label = prevYear + "-" + prevMon, linestyle='dashed', marker='o', markersize=8)
plt.legend()
plt.savefig('Core PCE inflation ' + Year + "-" + Month)

# Federal funds rate:
thisFFR = []
lastFFR = []

i=0
for vals in output_rows[11]:
    if(i<4):
        valint = float(vals)
        thisFFR.append(valint)
    i+=1

j=0
for vals in output_rows[12]:
    if(j<4):
        valint = float(vals)
        lastFFR.append(valint)
    j+=1

plt.figure(5)
plt.title( "Federal funds rate")
plt.plot(x, thisFFR, label = Year + "-" + Month, marker='o', markersize=8)
plt.plot(x, lastFFR, label = prevYear + "-" + prevMon, linestyle='dashed', marker='o', markersize=8)
plt.legend()
plt.savefig('Federal funds rate ' + Year + "-" + Month)

# Finally display our plots:
plt.show()








