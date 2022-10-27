from flask import Flask, render_template, jsonify, request
from requests_html import HTMLSession
import asyncio
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    if request.method == 'POST':

        checklist = ['java', 'Javascript', 'python', 'Python', 'Java', 'javascript']
                
        language=request.form['language']
        search_query = request.form['search_query']

        if language in checklist:
            pass
        else:
            return render_template('index.html',result={"invalid language selection"})

        regex = rf"(?i){language}(.*)"
        if re.match(regex, search_query):
            return render_template('index.html',result={"invalid search query"})
                    
        query_input = language + " " + search_query
        session1 = HTMLSession()
        url = f"https://www.youtube.com/results?search_query={query_input}&sp=CAMSBggDEAEYAg%253D%253D"

        response = session1.get(url)
        list_results = []
        list_results3 = []
        list_results4 = []
        urltemplate = "https://www.youtube.com/watch?v="

        regexquery = re.compile("(watchEndpoint\":{\"videoId\":\")\w+")

        for var in re.finditer(regexquery, response.text):
            list_results.append(var.group()[-11:])
            
        regextitle = re.compile("(\"title\":{\"runs\":\[{\"text\":\".[^\"]+)")

        for var3 in re.finditer(regextitle, response.text):
            list_results4.append(var3.group()[26:])
        list_resultspopped = list_results4[:6]

        if len(list_results)<1:
            return render_template('index.html',result="no matching videos")
            
        for i in range(len(list_results)):
            if list_results[i] not in list_results[i + 1:]:
                list_results3.append(urltemplate+list_results[i])
        #list_3 contains unique urls
        if len(list_results3)<10:
            listsize = len(list_results3)

            finalistarray = ['<' + x + '>' + y for  x,y in zip(list_results3, list_resultspopped[0:listsize])]
            return render_template('index.html',result=finalistarray)

        finalistarray = ['<' + x + '>' + y  for x, y in zip(list_results3[0:10], list_resultspopped[0:10])]
   
        return render_template('index.html',result=finalistarray, result2=language + ' ' + search_query)

    return render_template('index.html',result="most recent on youtube")


if __name__ == '__main__':
    app.run()