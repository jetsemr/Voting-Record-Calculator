import requests
from bs4 import BeautifulSoup
import pandas as pd

url = input("Enter tabroom url for judge list: ")

html_text = requests.get(url).text
soup1 = BeautifulSoup(html_text, 'html.parser')

nameTable = soup1.find('table', id="judgelist")

headers = ['Name']

nameData = pd.DataFrame(columns = headers)

for i in nameTable.find_all('tr')[1:]:
  row_data = i.find_all('td')
  row = row_data[1].text.strip() + ' ' + row_data[3].text.strip()
  length = len(nameData)
  nameData.loc[length] = row.strip()

affWinPercent = []
index = 0
prevPath = ''

for link in soup1.find_all('a'):
  path = link.get('href')

  if (path != prevPath):
    if "judge_person_id" in path:
      url = "https://www.tabroom.com/" + path
      page = requests.get(url)
      soup2 = BeautifulSoup(page.text, 'html.parser')

      table = soup2.find('table', id='judgerecord')
      votingRecord = []
      for i in table.find_all('tr')[1:]:
        row_data = i.find_all('td')
        row = row_data[7].text
        votingRecord.append(row.strip())

      affCount = 0
      for i in range(len(votingRecord)):
        if votingRecord[i] == 'Aff':
          affCount += 1

      affPercent = affCount / len(votingRecord)
      # print(index ,path, affPercent)
      affWinPercent.append(affPercent)
      index += 1
  prevPath = path

nameData['Aff Win Percent'] = affWinPercent
nameData.to_csv('judges.csv')