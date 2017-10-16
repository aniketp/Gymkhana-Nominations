
import pprint
import requests
from bs4 import BeautifulSoup, Comment
import re


def getRecord(rollNo):
    roll = str(rollNo)
    req = requests.get('https://oa.cc.iitk.ac.in/Oa/Jsp/OAServices/IITk_SrchRes.jsp?typ=stud&numtxt=' + roll + '&sbm=Y')
    soup = BeautifulSoup(req.text,"lxml")
    record = {}

    record['roll'] = roll

    image = 'http://oa.cc.iitk.ac.in/Oa/Jsp/Photo/' + roll + '_0.jpg'
    record['image'] = image

    data = soup.findChildren('p')
    name = data[0].text.split(':')[1]
    name = re.sub('\s+', ' ', name)
    record['name'] = name

    if not name:
        return None

    program = data[1].text.split(':')[1]
    program = re.sub('\s+', ' ', program)
    record['program'] = program

    dept = data[2].text.split(':')[1]
    dept = re.sub('\s+', ' ', dept)
    record['department'] = dept

    room = data[3].text.split(':')[1]
    room = re.sub('\s+', ' ', room)
    hall = room.split(',')[0]
    record['hall'] = hall
    room = room.split(',')[1]
    record['room'] = room

    email = data[4].text.split(':')[1]
    email = re.sub('\s+', '', email)
    record['email'] = email

    bloodData = data[5].text.split('<b>')[0]
    blood = bloodData.split(':')[1]
    blood = re.sub('\s+', '', blood)
    record['blood'] = blood

  

    genderData = data[6].text.split(':')
    gender = genderData[1][0]
    gender = re.sub('\s+', ' ', gender)
    record['gender'] = gender

    country = genderData[2]
    country = re.sub('\s+', ' ', country)
    record['country'] = country

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    addressSoup = BeautifulSoup(comments[1])
    permanentAddressData = addressSoup.findAll('p')[1].text
    phonePos = permanentAddressData.index('Phone no:')
    mobilePos = permanentAddressData.index('Mobile no:')

    address  = permanentAddressData[19:phonePos]
    address = re.sub('\s+', ' ', address)
    record['address'] = address

    phone = permanentAddressData[(phonePos + 9):mobilePos]
    phone = re.sub('\s+', ' ', phone)
    record['phone'] = phone

    mobile = permanentAddressData[(mobilePos + 10):]
    mobile = re.sub('\s+', ' ', mobile)
    record['mobile'] = mobile

    return record



#print(getRecord(160113))

#arrayOfRecords = []
#for i in range(11000, 14000):
 #   arrayOfRecords.append(getRecord(i))




