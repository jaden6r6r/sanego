
#First get a list of all specialities to include in the fetch query 

#for each of these specialities, find out the number of pages - starting at 0, 200 will be returned otherwise 4xx

#while statuscode(var) == 200
    ##Make the request
        ##Will return html containing the 'view profile' 
            #For each 'view profile' 
                #Get the page, store the data

import requests
import json
import bs4 as bs
import time 
import urllib.parse
import re
import csv
if __name__ == '__main__':

    def scrape(urlSlug):
        scrapedUrl = ''
        scrapedName =''
        scrapedMainSpeciality = ''
        scrapedSubSpeciality = []
        scrapedLocationClinic = ''
        scrapedLocationUrl = ''
        scrapedLocationAddress = ''
        scrapedAddress = ''
        scrapedPhone = ''
        scrapedFax =''
        scrapedMobile =''
        scrapedEmail = ''
        scrapedInsurance = '' 
        scrapedPhotoURL = ''
        scrapedRatingScore = ''
        scrapedNoRatings ='' 
        scrapedLanguages = ''


        # given a url, get the required data. 
        urlBase = 'https://www.sanego.de'
        urlComposed = urlBase+urlSlug
        headers = { "accept": "text/javascript, text/html, application/xml, text/xml, */*",
                "accept-language": "en-US,en;q=0.9,ceb;q=0.8,fr;q=0.7,de",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest"}

        r = requests.post(urlComposed,headers=headers)
        r.encoding = r.apparent_encoding
        soup = bs.BeautifulSoup(r.content,'html.parser')
        #get URL 
        header = soup.find('h1',text=True)
        scrapedUrl = urlComposed

        #get name and speciality. 
        headerSplit = header.text.split(",")
        scrapedName = headerSplit[0].lstrip()
        scrapedMainSpeciality = headerSplit[2].lstrip()

        #get sub specialities 
        contentClass = soup.find_all('div', class_='content')
        ulItem = contentClass[3].find('ul')
        subItem = ulItem.find_all('li')
        subSpeciality = []
        for li in subItem:
            if (li.text != scrapedMainSpeciality):
                scrapedSubSpeciality.append(li.text)
        

        #get clinic name + url 
        contentClass = soup.find('div', class_='contact')
        if (contentClass.find('a')):
            urlLocation = contentClass.find('a')['href']
            scrapedLocationUrl = contentClass.find('a')['href']
            if (scrapedLocationUrl.find('font')!= -1):
                print(scrapedLocationUrl.find('font'))
                scrapedLocationClinic = scrapedLocationUrl.find('font')

        #get Address
        contentClass = soup.find('div', class_='contact')
        ulItem = contentClass.find_all('p')
        scrapedAddress = ulItem[0].text

        #get telephone 
        if(soup.find('span', itemprop='telephone')):
            phone = soup.find('span', itemprop='telephone')
            scrapedPhone = phone.text

        #get fax
        faxUnclean = soup.find_all('span')
        for span in faxUnclean:
            if 'Fax' in span.text:
                faxClean = re.sub("[^0-9()]","",span.text)
                scrapedFax = faxClean

        #get mobile
        mobileUnclean = soup.find_all('span')
        for span in mobileUnclean:
            if 'Mobile phone' in span.text:
                mobileClean = re.sub("[^0-9()/]","",span.text)
                scrapedMobile = mobileClean

        #get email
        emailUnclean = soup.find_all('span')
        for span in emailUnclean:
            if '@' in span.text:
                scrapedEmail = span.text

        #get insurance 
        insuranceUnclean = soup.find_all('div', class_='content')
        for font in insuranceUnclean:
            if 'Versicherung' in font.text:
                stripLeading = re.sub(r'^.*?Versicherung', 'Versicherung', font.text)
                stripTrailing = stripLeading.split('.',1)
                scrapedInsurance = stripTrailing[0].replace('Versicherung: ','')
                break
        
        #getImage
        imageTag = soup.find('a', class_='bigImg')
        scrapedPhotoURL = imageTag['href']

        #getRatingScore
        score = soup.find_all('div', class_='secondDegInfo')
        scrapedRatingScore = score[2].text

        #getNoRatings
        ratings = soup.find('div',class_='stats')
        value = ratings.find('span', class_='value')
        scrapedNoRatings = value.text

        #getLanguages
        languagesUnclean = soup.find_all('div', class_='content')
        for font in languagesUnclean:
            if 'Spricht:' in font.text:
                stripLeading = re.sub(r'^.*?Spricht:', 'Spricht:', font.text)
                stripTrailing = stripLeading.split('.',1)
                scrapedLanguages = stripTrailing[0].replace('Spricht: ','')
                break
        


        # print('url is: ',scrapedUrl)
        # print('name is ', scrapedName)
        # print('main speciality is ',scrapedMainSpeciality)
        # for sub in scrapedSubSpeciality:
        #     print(' sup speciality ',sub)
        # print('address  ',scrapedAddress)
        # if (len(scrapedLocationClinic)>0):
        #     print('name of clinic ',scrapedLocationClinic)
        # if (scrapedLocationUrl):
        #     print('url for location ',scrapedLocationUrl)
        # print('telephone is ', scrapedPhone)
        # print('fax is ', scrapedFax)
        # if (scrapedMobile!=''):
        #     print('mobile is ', scrapedMobile)
        # if(scrapedEmail!=''):
        #     print('email is ', scrapedEmail)
        # if(scrapedInsurance!=''):
        #     print('insurance type, ', scrapedInsurance)
        # print('photo URL', scrapedPhotoURL)
        # print('rating is ',scrapedRatingScore)
        # print('number of ratings ',scrapedNoRatings)
        # print('languages spoken ', scrapedLanguages)
        appendList = []
        appendList.append(scrapedUrl)
        appendList.append(scrapedName)
        appendList.append(scrapedMainSpeciality)
        appendList.append(scrapedSubSpeciality)
        appendList.append(scrapedAddress)
        appendList.append(scrapedLocationClinic)
        appendList.append(scrapedLocationUrl)
        appendList.append(scrapedPhone)
        appendList.append(scrapedFax)
        appendList.append(scrapedMobile)
        appendList.append(scrapedEmail)
        appendList.append(scrapedInsurance)
        appendList.append(scrapedPhotoURL)
        appendList.append(scrapedRatingScore)
        appendList.append(scrapedNoRatings)
        appendList.append(scrapedLanguages)



        with open('output.csv', 'a') as csvFile:
            wr = csv.writer(csvFile,dialect='excel')
            # zip(scrapedUrl,scrapedName, scrapedMainSpeciality, scrapedSubSpeciality,scrapedAddress,scrapedLocationClinic,scrapedLocationUrl,scrapedPhone, scrapedFax,scrapedMobile,scrapedEmail,scrapedInsurance,scrapedPhotoURL,scrapedRatingScore,scrapedNoRatings,scrapedLanguages)
            wr.writerow(appendList)




    #Get URLS of all areas of specialities and append to list 
    specialities = []
    url='https://www.sanego.de/Arzt/Fachgebiete/'
    headers = { "accept": "text/javascript, text/html, application/xml, text/xml, */*",
                "accept-language": "en-US,en;q=0.9,ceb;q=0.8,fr;q=0.7,de",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest"}

    r = requests.post(url,headers=headers)
    r.encoding = r.apparent_encoding
    text = str(r.content, 'utf-8', errors='replace')
    soup = bs.BeautifulSoup(text,'html.parser')
    print(soup.original_encoding)
    for ul in soup.find_all('ul', class_='itemList'):
        for li in ul.find_all('li'):
            a = li.find('a')
            href= a['href']
            specialities.append(href)


    #For each of the specialities, begin querying the ajax 
    for speciality in specialities:
        pageNum = 0 
        valid = True
        while valid == True:
            speciality = speciality.replace('/Arzt/','')
            speciality = speciality.replace('/','')
            decoded = urllib.parse.unquote(speciality)
            decoded =decoded.replace(' ','&')

            #replace space with &
            
            url='https://www.sanego.de/ajax/load-more-doctors-for-search'
            payload = {'body':'doctorType=Arzt&federalStateOrMedicalArea={decoded}&p={pageNum}'.format(decoded=decoded, pageNum=pageNum)}
            headers = {
                        "accept": "text/javascript, text/html, application/xml, text/xml, */*",
                        "accept-language": "en-US,en;q=0.9,ceb;q=0.8,fr;q=0.7,de",
                        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
                        "sec-ch-ua-mobile": "?0",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "x-requested-with": "XMLHttpRequest"}
            r = requests.post(url, data=json.dumps(payload),headers=headers)
            if r.status_code == 200:
                text = str(r.content, 'UTF-8', errors='replace')
                soup = bs.BeautifulSoup(text,'html.parser')
                allA = soup.find_all('a', href=True)
                urls = []
                for a in allA:
                    if a['href'] not in urls:
                        urls.append(a['href'])
                for url in urls:
                    scrape(url)
                    ##Parse and log. 
                # pageNum = pageNum + 1
            else:
                valid = False
                print(decoded,' ',pageNum, ' invalid page ', r.status_code)



'''
Query to use: 

    fetch("https://www.sanego.de/ajax/load-more-doctors-for-search", {
    "headers": {
        "accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "accept-language": "en-US,en;q=0.9,ceb;q=0.8,fr;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "https://www.sanego.de/Arzt/Akupunktur/", 
    "referrerPolicy": "unsafe-url",
    "body": "doctorType=Arzt&federalStateOrMedicalArea=Akupunktur&p=310", -- increment the p each time the guard is true. Amend the category/area on each run of the for loop  
    "method": "POST",
    "mode": "cors",
    "credentials": "include"
    }).then(resp=>console.log(resp.text()));

'''