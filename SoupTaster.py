#Modify for every business location
url = "https://www.yelp.com/biz/butteriffic-bakery-and-cafe-memphis-2?osq=Butteriffic+Bakery+%26+Cafe&start=0"

#Installations and Imports
!pip install requests
!pip install html5lib
!pip install bs4

import re
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv

#number of reviews for location
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
ugly=(soup.prettify())
marker = " of "
spot = ugly.find('href="#reviews"')
zone = ugly[spot:spot+200]
numrevs = 0
numpages = 0
if re.search(r' reviews\)', zone):
    newspot = zone.find(' reviews)')
    newzone = zone[:newspot]
    quote_index = newzone.find('(')
    if quote_index != -1:
        # If quote_index is not -1, it means a double quote was found
        print("First double quote found at index:", quote_index)
        numrevs = int(newzone[quote_index+1:len(newzone)])
        numpages = int(numrevs/10)
        if numrevs%10 > 0:
          numpages+=1
        print("Number of reviews:", numrevs)
        print (numpages)
    else:
        print("Double quote not found in 'newzone'")
else:
    print("Substring ' reviews)' not found in 'zone'")


#Making a List of Urls for all pages of reviews
urls = []
url = url[0:url.find("start=")+6]
num = 0

for i in range(numpages):
  newrl = url + str(num)
  num = num+10
  urls.append(newrl)

#initializing empty list for reviews
allrevs=[]

#defining review parsing tool
def parseReviews():
  if "review" in ugly:
    print(ugly.count("review"))
  print(len(ugly))

  reviews = [] #list to fill with reviews
  reviewmarker = "node.text" #string I found that was consistently in front of reviews
  j=0 #bookmark so as we search through the string, we start after the last place we found reviewmarker
  for i in range(ugly.count(reviewmarker)): #iterating though the number of times reviewmarker is present in the string
    spot = ugly.find(reviewmarker, j, len(ugly)) #find all instances of reviewmarker in ugly starting from the point where the last reviewmarker ended
    j = spot + len(reviewmarker) #updating bookmark position
    if bool(re.search(r"", ugly[spot:spot+200])) == True and bool(re.search(r" ", ugly[spot:spot+200])) == True: #filtering out things that are not reviews
      review = ugly[spot+40:spot+5082].replace("&#x27;" , "").replace("&#x2F" , "") #getting rid of clutter
      if '&quot' in review: #finding the end of the review
        spot = review.find('&quot', 0, len(review))
        review = review[0:spot]
      reviews.append(review) #adding reviews to review list
      if review in allrevs:
        continue
      else:
        allrevs.append(review)

#running function on all urls
for j in urls:
  r = requests.get(j)
  soup = BeautifulSoup(r.content, 'html5lib')
  ugly=(soup.prettify())
  parseReviews()
  print("allrevs length: ", len(allrevs))

#See all reviews
for i in allrevs:
  print(i)

