__author__ = 'Ben'
import random
import string
import time



class lookBusy:
    def lookBusy(a):
        dataCategories=['Grant','Abstract','Publication', 'Project', 'Attendee', 'Author','Viewership','Research','Stastical','Genome']
        for num in range(a):
            time.sleep(random.randint(0,2))
            acronym=''
            for num2 in range(random.choice(range(3,6))):
                acronym+=random.choice(string.ascii_uppercase)
            acronym+=' '
            year=random.choice(range(1910,2015))
            dataCateg=random.choice(dataCategories)
            if year<1980:
                dataCategories.remove('Viewership')
                dataCategories.remove('Genome')
                dataCateg=random.choice(dataCategories)
                dataCategories.append('Viewership')
                dataCategories.append('Genome')
            print('Scraping '+acronym+dataCateg+' Data From Year '+str(year)+'. . . ')
            time.sleep(random.randint(3,20))
            print('Finished Scraping '+acronym+dataCateg+' Data From Year '+str(year)+'.')

    lookBusy(50000)