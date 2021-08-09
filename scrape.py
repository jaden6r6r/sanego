
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
if __name__ == '__main__':

    def scrape(urlSlug):
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
        print(urlComposed)
        header = soup.find('h1',text=True)

        #get name and speciality. 
        headerSplit = header.text.split(",")
        name = headerSplit[0].lstrip()
        mainSpeciality = headerSplit[2].lstrip()
        print(mainSpeciality)

        #get sub specialities 
        contentClass = soup.find_all('div', class_='content')
        ulItem = contentClass[3].find('ul')
        subItem = ulItem.find_all('li')
        subSpeciality = []
        for li in subItem:
            if (li.text != mainSpeciality):
                subSpeciality.append(li.text)
        for sub in subSpeciality:
            print(sub)

        #get location
        contentClass = soup.find('div', class_='contact')
        ulItem = contentClass.find_all('p')
        print(ulItem[0].text)
        

        time.sleep(10)




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