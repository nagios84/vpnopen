import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import os

link = 'https://www.vpngate.net/en/'
s = requests.Session()
s.head(link)

def get_link(t_link):
    return link + t_link


def get_best_score_vpn(html):
    soup = bs(html, 'lxml')
    tr = soup.find_all('table', attrs={'id': 'vg_hosts_table_id'})[-1].find_all('tr')[3]
    t_link = tr.find_all('td')[6].find('a').get('href')
    # print(t_link)
    # print(type(t_link))
    # print(dir(t_link))
    file_link = get_link(t_link)
    return s.get(file_link).text


def get_vpn_file(html):
    soup = bs(html, 'lxml')
    link = 'https://www.vpngate.net'
    t_link = soup.find_all('ul')[-2].find_all('a')[-1].get('href')
    file_link = link + t_link
    # print(file_link)
    res = s.get(file_link, stream=True)
    file_name = file_link.split('/')[-1]
    with open(file_name, 'wb') as file:
        file.write(res.content)
    
    sleep(5)
    os.system('echo %s|sudo -S %s' % ('777', "openvpn --config " + file_name))
    # os.popen("sudo -S openvpn --config " + file_name, 'w').write("777")

def main():

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        'C_OpenVPN': 'on',
        'Button3': 'Refresh Servers List'
    }

    r = s.post(link, headers=headers, data=payload).text
    get_vpn_file(get_best_score_vpn(r))


if __name__ == '__main__':
    main()
