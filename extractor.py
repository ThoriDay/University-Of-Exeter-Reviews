import pandas as pd
import re
from bs4 import BeautifulSoup

with open("unireviews.html", "r", encoding="utf-8") as f:
    htmlDoc = f.read()

soup = BeautifulSoup(htmlDoc, 'html.parser')
paras = soup.findAll('p')

#Reviews
reviews = []
for p in paras:
    span = p.find("span")
    if span is not None:
        text = span.text
        reviews.append(text)
reviews = reviews[3:]
#print(len(reviews))


divs = soup.find_all('div', class_ = "review-box__content p tw-mb-6 tw-basis-full")


#Stars out of 5
stars = []
for d in divs:
    span2 = d.find(class_ ="tw-relative tw-top-[-2px] tw-left-[2px]")
    if span2 is not None:
        text2 = span2.text
        stars.append(text2)
#print(len(stars))


datNm = []
spans = soup.find_all("span", class_="tw-text-sc-silver-sand")
for s in spans:
    sp = s.next_sibling
    datNm.append(sp)


#Members & Dates
members = []
dates = []
for i in datNm:
    if str(i).startswith('<'):
        for m in str(i).split():
            numbers = re.findall(r'\d+', m)

        members.append(numbers)
    else:
        dates.append(i)       
#print(len(members))
#print(len(dates))

dates = [element.replace("\n", "") for element in dates]
#print(dates)

#Ratings
ratings = []
div2 = soup.find_all("div", class_ = "mb- mt- tw-pl-[34px]")
for div in div2:
    for di in str(div.div).split():
        no = re.findall(r'\d+', di)
    ratings.append(no)

#print(len(ratings))
   
#print(div2[0].next_sibling)

campus = []
clubs = []
su = []
cs = []
wifi = [] 

ratings = [item for sublist in ratings for item in sublist]
#print(ratings)

campus = ratings[::5]
#print(campus)

clubs = ratings[1::5]
su = ratings[2::5]
cs = ratings[3::5]
wifi = ratings[4::5]

members = [y for x in members for y in x]


data = {'Member ID' : members, 'Date' : dates, 'Review' : reviews, 'Student Review' : stars,
                  'Campus/Facilities' : campus, 'Club/Societies' : clubs, 'Careers Service' : cs, 'Wifi/Internet' : wifi}

series_list = [pd.Series(data[key], name=key) for key in data]
df = pd.concat(series_list, axis=1)
df = pd.DataFrame(df)



#df = pd.DataFrame({'Member ID' : members, 'Date' : dates, 'Review' : reviews, 'Student Review' : stars,
#                  'Campus/Facilities' : campus, 'Club/Societies' : clubs, 'Careers Service' : cs, 'Wifi/Internet' : wifi})

#print(df)
df.to_csv("ExeterReviews.csv", index=False)