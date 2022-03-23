# Python code for automatic enrolling in free Udemy courses that are provided by personbook.com and capured by this code - The code uses Selenium for web automaion.
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from timeit import default_timer
import datetime

email = input("Email: ")
# Change password
start = default_timer() # for calculating the duration of execution

def Convert(n): # Convert from seconds to hour: minute: second
    return str(datetime.timedelta(seconds = n))
def ClearConsole() :
    system('cls') # to clear whatever before the input
def OpenBrowser() : # Returs 'driver' to use it in navigating and getting url in the browser
    try :
        driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')    # WebDriver is added to the same folder of the py file.
    except :
        print('|| ' + 'WebDriver is missed.\nIt should be in this path\n --> C:/webdriver/chromedriver.exe')
        input('Exit?')
        exit(0)
    driver.maximize_window()
    return driver
def ReadList() :
    courses_list = list()
    try :
        page = open('personbook_list.txt', 'r', encoding="utf-8")
    except :
        print('|| ' + 'There is a problem with courses_list(personbook_list.txt). Maybe location')
        exit(0)

    for line in page :
        courses_list.append(line.strip())
    page.close()

    try :
        page = open('special_list.txt', 'r', encoding="utf-8")
    except :
        print('|| ' + 'There is a problem with courses_list(special_list.txt). Maybe location')
        exit(0)

    for line in page :
        courses_list.append(line.strip())
    page.close()

    return courses_list
def LoginUdemy() :
    driver.get('https://www.udemy.com/join/login-popup/') # Udemy Login Page
    time.sleep(random.randint(4, 8))
    ClearConsole()
    while True :
        try :
            driver.find_element_by_name('email').send_keys(email)    # Changable
            driver.find_element_by_name('password').send_keys(input("Password: "))  # Changable
            ClearConsole()
            #time.sleep(random.randint(5, 10))
            driver.find_element_by_name('submit').click()
            #time.sleep(random.randint(4, 8))
            print('|| ' + 'Email: ' + email)
            input('Click Log in')
            break
        except :
            condition = input('Are you a human :). Get login page, then press Enter OR Type c if you logged in')
            if condition == 'c' :
                break
def get_first_enroll_xpaths() :
    first_enroll_xpaths = list()

    ids = {'udemy', 'jp', 'sg'}
    nums = {1, 2, 3}
    for id in ids :
        for j in nums :
            for k in nums :
                first_enroll_xpaths.append('//*[@id="%s"]/div[%d]/div[3]/div[1]/div[%d]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[5]/div/button' % (id , j, k))

    for no in range(1000) :
        first_enroll_xpaths.append('//*[@id="u%s-tabs--5-content-0"]/div/div[1]/div/div[5]/div/button' % no)

    return first_enroll_xpaths
def get_first_enroll_xpaths_text() :
    first_enroll_xpaths_text = list()

    ids = {'udemy', 'jp', 'sg'}
    nums = {1, 2, 3}
    for id in ids :
        for j in nums :
            for k in nums :
                first_enroll_xpaths_text.append('//*[@id="%s"]/div[%d]/div[3]/div[1]/div[%d]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[5]/div/button/span' % (id , j, k))

    for no in range(1000) :
        first_enroll_xpaths.append('//*[@id="u%s-tabs--5-content-0"]/div/div[1]/div/div[5]/div/button/span' % no)

    return first_enroll_xpaths_text
def get_enrolled_xpaths() :
    enrolled_xpaths = list()

    ids = {'udemy', 'jp', 'sg'}
    nums = {1, 2, 3}
    for id in ids :
        for j in nums :
            for k in nums :
                enrolled_xpaths.append('//*[@id="%s"]/div[%d]/div[3]/div[1]/div[%d]/div/div/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[2]/div/button/span' % (id , j, k))

    for no in range(1000) :
        enrolled_xpaths.append('//*[@id="u%s-tabs--5-content-0"]/div/div[1]/div/div[2]/div/button/span' % no)

    return enrolled_xpaths
def SaveSourcePage(i) :
    page = open(email + ' - ' + 'rare case happen at' + ' course ' + str(i) + '.txt', 'w', encoding="utf-8")    # Changable
    page.write(driver.page_source)

### MAIN ###
driver = OpenBrowser() # Run the browser

courses_list = ReadList() # save links in it

LoginUdemy() # get to Udemy.com and sign in

# Through a loop (get to udemy links from the list one by one and enroll)
ClearConsole()
first_enroll_xpaths = get_first_enroll_xpaths()    # Put the xpaths of enroll now from first page in a list | I used list because the xpath changes between len(first_enroll_xpaths) xpaths
first_enroll_xpaths_text = get_first_enroll_xpaths_text()  # Put the xpath of Enroll Now in a list as text to know detect that is it Enroll Now or Buy Now
enrolled_xpaths = get_enrolled_xpaths() # Put the xpaths of Go to Course(I Enrolled before) in a list to convert to text and check it.
second_enroll_xpath = '//*[@id="udemy"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button' # Second Enroll Now, It should be Enroll Now always

i = 0 # For numbering the courses
enrolled_successfully = 0   # For counting courses that had enrolled in successfully
print('|| ' + 'Email: ' + email)
for link in courses_list :
    fucked_first_enroll_xpath = 0   # Testing
    driver.get(link)
    time.sleep(random.randint(5, 10))
    i = i + 1 # For numbering the courses

    # Check if it's free --> Get what is written on the Enroll Now button so if it's Buy now, skip this link
    temp_1 = None
    for word in first_enroll_xpaths_text :
        try :
            temp_1 = driver.find_element_by_xpath('%s' % (word)).text
            if temp_1 == 'Buy now' : break
        except :
            pass
    if temp_1 == 'Buy now' :    # Skip the link if it's not free
        print('|| ' + '%d\'th Course is not free' % i)
        continue

    # Check if I Enrolled before or not and skip the link if it is true
    temp_2 = None
    for word in enrolled_xpaths :
        try :
            temp_2 = driver.find_element_by_xpath('%s' % (word)).text
            if temp_2 == 'Go to course' : break
        except :
            pass
    if temp_2 == 'Go to course' :    # Skip the link if It's enrolled already
        print('|| ' + '%d\'th Course is enrolled already' % i)
        continue


    for xp in first_enroll_xpaths : # Finds Enroll Now button and click it
        try :
            driver.find_element_by_xpath('%s' % (xp)).click()
            time.sleep(random.randint(4, 8))
            break
        except :
            fucked_first_enroll_xpath = fucked_first_enroll_xpath + 1

    if fucked_first_enroll_xpath == len(first_enroll_xpaths) : # Stop if there isn't Enroll Now button
        print('|| ' + '%d\'th Course --> No xpath. Maybe You Already Enrolled or this not Udemy site' % i)
        # save screenshot and page source of page
        fname = str(random.randint(10000, 1000000))
        driver.save_screenshot(fname + '.png')
        with open(fname + '.txt', 'w', encoding='utf-8') as ps :
            ps.write(driver.page_source)
        print('Saved --> screenshot and page source --> filename: ' + fname)
        continue


    try :   # Finds second Enroll Now button and click it and save webpage if there is an error
        driver.find_element_by_xpath('%s' % (second_enroll_xpath)).click()
        print('|| ' + 'Successfully Enrolled in %d\'th Course' % i)
        enrolled_successfully = enrolled_successfully + 1
    except :
        print('|| ' + 'Unsuccessfully Enrolled in %d\'th Course - Source file saved - No enroll button in second page' % i)
        SaveSourcePage(str(i) + ' second_enroll')

    time.sleep(random.randint(7, 15))

print('|| ' + 'Links are finished')
print('|| ' + 'Enrolled Successfully = %d' % enrolled_successfully)

duration = default_timer() - start
duration = Convert(duration)
duration = duration[:duration.find('.')]
print('|| ' + 'Time(s): %s' % duration)
input('Exit?')

driver.quit()
