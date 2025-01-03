from bs4 import BeautifulSoup;
import requests;

response = requests.get("https://ftw.usatoday.com/lists/best-video-games");

games_web = response.text

# print(response)

webpage = BeautifulSoup(games_web, 'html.parser');

titles = webpage.find_all(name='span', class_ ='listicle-header-text');
ranking = webpage.select(selector='.listicle-count');

titles_list = [];
ranking_list = [];


for element in titles:
    element_to_be_added = element.getText();
    # titles_list += element_to_be_added
    titles_list.append(element_to_be_added);

for element in ranking:
    element_to_be_added = element.getText().strip();
    ranking_list.append(element_to_be_added);


titles_list = titles_list[::-1]
ranking_list = ranking_list[::-1]

content_list = [element.getText().strip() for element in webpage.select(selector='.listicle-content')][::-1]
# print(len(content_list))


with open("top_100_games_list.txt", 'w', encoding='utf-8') as file:
    for i in range(len(ranking_list)):
        file.write(f'{ranking_list[i]}\n');
        file.write(f'{titles_list[i]}\n');
        file.write(f'{content_list[i]}\n');
        file.write('-'* 40 + '\n');
