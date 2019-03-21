from bs4 import BeautifulSoup
import requests
import re
import os

# get a string containing the names of all current 4P 10-dan players
player_list_url = "https://wikiwiki.jp/tenhou-chat/%E5%8D%81%E6%AE%B5%E3%83%AA%E3%82%B9%E3%83%88"
response = requests.get(player_list_url)
try:
    response.raise_for_status()
except Exception as e:
    pritn(e)
    
soup = BeautifulSoup(response.content, 'html.parser')
names_text = soup.find_all('p')[1].text

names_text = names_text.split("現役十段")[-1].split("人")[-1]

# convert the long name string to a list 
name_list = names_text.split('、')

for i in range(len(name_list)):
    # remove newline characters and characters between parentheses
    name_list[i] = re.sub(r'\(.*?\)', '', name_list[i].replace('\n', ''))

points = {}

# get their ranking points
for name in name_list:
    
    print("Stats for " + name)
    
    stats_url = "http://arcturus.su/tenhou/ranking/ranking.pl?name=" + name + "&r=8"
    print(stats_url)
    
    response = requests.get(stats_url)
    try:
        response.raise_for_status()
    except Exception as e:
        pritn(e)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    p_tags = soup.find('div', {'id':'stats'}).find_all('p')
    current_point = p_tags[1].text
    
    print(current_point)
    
    current_point = current_point.split()
    points[name] = int(current_point[3].replace("pt", ''))
    
    print("--------------")

# store (name, ranking points) to a txt file 
sorted_by_points = sorted(points.items(), key=lambda kv: kv[1], reverse = True)
txt_name = "r_points.txt"
if os.path.exists(txt_name):
    os.remove(txt_name)
with open(txt_name, 'w', encoding="utf-8") as f:
    for name_point in sorted_by_points:
        f.write(name_point[0] + " " + str(name_point[1]) + '\n')
print("All data saved to r_points.txt")  