
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

if __name__ == '__main__':
    for x in range(1):
        url='https://www.sanego.de/ajax/load-more-doctors-for-search'
        payload = {'body':'doctorType=Arzt&federalStateOrMedicalArea=Akupunktur&p=0'}
        headers = {'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
                    "accept": "text/javascript, text/html, application/xml, text/xml, */*",
                    "accept-language": "en-US,en;q=0.9,ceb;q=0.8,fr;q=0.7",
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-requested-with": "XMLHttpRequest"}
        r = requests.post(url, data=json.dumps(payload),headers=headers)
        soup = bs.BeautifulSoup(r.text,'html.parser')
        allA = soup.find_all('a', href=True)
        urls = []
        for a in allA:
            if a['href'] not in urls:
                urls.append(a['href'])
        for url in urls:
            print(url)



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