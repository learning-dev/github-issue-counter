from bs4 import BeautifulSoup
from datetime import datetime
import locale
import requests 
import humanize
from flask import Flask, request, render_template 
from forms import InputForm

#URL = 'https://github.com/facebook/react/issues'

#response = requests.get(URL)
#soup = BeautifulSoup(response.text, 'html.parser')     

soup = ''

def total_issues():

    issue_tag = soup.find("a", {"class": "btn-link"}).get_text()
    issues_open = issue_tag.strip( ) 
    issues_open = issues_open.split()[0]
    issues_open = int(issues_open.replace(',',''))

    print("Total number of open Issues are :", issues_open)
    return count_issues(soup, issues_open)


def count_issues(soup, issues_open):
    
    issues_today = 0
    issues_current_week = 0
    time_tags = soup.find_all('relative-time')
    current_num = 0
    page = 1
    while (current_num < 7):
        if (page > 1):
            res = requests.get(URL + '?page='+ str(page))
            print('url', URL + '?page='+ str(page))
            if(res.status_code == 200):
                soup = BeautifulSoup(res.text, 'html.parser')
                time_tags = soup.find_all('relative-time')
        print(len(time_tags))
        for tag in time_tags:
            time_posted = tag.attrs['datetime']
            time_posted = datetime.strptime(time_posted, '%Y-%m-%dT%H:%M:%S%z')
            local_native = time_posted.astimezone().replace(tzinfo=None)
            time_text = humanize.naturaltime(local_native)
            print(time_text)
            time_text = time_text.split( )
            print(time_text)

            if time_text[1] in ['years', 'months']:
                current_num = 8
            elif time_text[1] in ['hours', 'hour','seconds','minutes'] :
                issues_today = issues_today + 1

            elif time_text[1] in ['day', 'days']:
                if time_text[0] == 'a':
                    time_text[0] = 1
                no_of_days =  int(time_text[0])
                print('no_of_days:',no_of_days)
                if no_of_days < 7:
                    issues_current_week += 1 
                current_num = no_of_days
                print('current_num',current_num)
                if current_num  > 7 :
                    break
            
        page += 1
        for_week = issues_current_week + issues_today
        more_than_week = issues_open - for_week

    output_dict = {}
    output_dict['total'] = issues_open
    output_dict['day'] =issues_today
    output_dict['week'] = issues_current_week  
    output_dict['more_week'] = more_than_week
    return output_dict


app = Flask(__name__)

app.config['SECRET_KEY']= '5b737afd51a9fef449c3ca09fbd79857'



@app.route("/", methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
        response = requests.get(form.github_url.data)
        print(form.github_url.data)
        if response.status_code == 200:
            global soup
            soup = BeautifulSoup(response.text, 'html.parser')
            output_dict = total_issues()
            return render_template('output.html', output_dict=output_dict)
    return render_template('input.html', title='Input', form=form)



@app.route("/output", methods=['GET', 'POST'])
def get_issues(text):
    response = requests.get(text)
    if response.status_code != 200:
        print("Please enter Valid URL or check your connnection")
        return 'Error: URL not Valid!'
    else:
        global soup
        soup = BeautifulSoup(response.text, 'html.parser')
        output_dict = total_issues()
        return render_template('output.html', output_dict=output_dict)

if __name__ == '__main__':
    app.run(debug=True)





