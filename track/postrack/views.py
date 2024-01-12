from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import secrets
import itertools as it
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.POST.get('tnumber'):
        if 'Identifiant invalide' not in scraper(request.POST.get('tnumber')):
            return render(request,'index.html',{'data':scraper(request.POST.get('tnumber')), 'tn':request.POST.get('tnumber')})
        else:
            return render(request,'index.html',{'error':"لم يتم تسجيل طردك عند البريد الجزائري"})
    else:
        return render(request,'index.html')

def scraper(tnumber):
    url1="https://aptracking.poste.dz/index.php"
    url2="https://aptracking.poste.dz/resultat.php"
    cookiesession = secrets.token_hex(5)
    PHPSESSID = secrets.token_hex(5)
    headers1={
        'Host': 'aptracking.poste.dz',
        'Cookie': f'cookiesession1={cookiesession}; PHPSESSID={PHPSESSID}',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://aptracking.poste.dz',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://aptracking.poste.dz/index.php',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i',
        'Connection': 'close'
    }
    headers2={
        'Host': 'aptracking.poste.dz',
        'Cookie': f'cookiesession1={cookiesession}; PHPSESSID={PHPSESSID}',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.199 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Referer': 'https://aptracking.poste.dz/index.php',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Priority': 'u=0, i',
        'Connection': 'close'
    }
    data={
        'Codebarre':'true',
        'searchByCustomerReference':'false',
        'oss_language':'fr',
        'includeOldItems':'false',
        'itemCodes':f'{tnumber}',
        'Rechercher':'Suivre+l%27envoi'
        
    }

    #fieldLabel02Std
    request1=requests.post(url1,headers=headers1,data=data, timeout=5)
    request2=requests.get(url2,headers=headers2,timeout=5)
    content=request2.content
    if '15/08/2023' in str(content):
        return "Identifiant invalide"
    soup=BeautifulSoup(content,'html5lib')
    table=soup.find("table", {"class": "display"})
    tbody=table.findAll("td")
    mylist=[]
    for i in tbody:
        mylist.append(i.text)

    result=list(it.batched(mylist, 5))
    html="<thead><tr><th>التاريخ</th><th>الوقت</th><th>الحالة</th><th>المكان</th></tr></thead><tbody>"
    for i in result:
        html+=f"<tr>"
        for j in i:
            html+=f"<td>{j}</td>"
    html+="</tbody>"
    return html