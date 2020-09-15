from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import re
import pandas as pd

# https://www.premierleague.com/players?se=274&cl=-1
# CL:
CLUBS_CL = \
    {'Arsenal': 1,
     'Aston Villa': 2,
     'AFC Bournemouth': 127,
     'Brighton and Hove Albion': 131,
     'Burnley': 43,
     'Chelsea': 4,
     'Crystal Palace': 6,
     'Everton': 7,
     'Leicester City': 26,
     'Liverpool': 10,
     'Manchester City': 11,
     'Manchester United': 12,
     'Newcastle United': 23,
     'Norwich City': 14,
     'Sheffield United': 18,
     'Southampton': 20,
     'Tottenham Hotspur': 21,
     'Watford': 33,
     'West Ham United': 25,
     'Wolverhampton Wanderers': 38
     }


class PlayerStatistics:

    def __init__(self, cl):
        ''' set options '''

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.__driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        self.__driver.set_window_size(1600, 900)

        start_urls = [f'https://www.premierleague.com/players?se=274&cl={cl}']
        self.__go_url(start_urls[0], 3)
        self.__close_adevert()

    def __go_url(self, url, t=0):
        ''' open url address '''
        self.__driver.get(url)
        time.sleep(t)

    def __close_adevert(self):
        ''' close advert '''
        self.__driver.find_element_by_xpath("//a[@id='advertClose']").click()

    def close_driver(self):
        ''' close driver '''
        self.__driver.close()

    def get_players(self, club_name):
        ''' get names, links of club players'''

        # get players
        # player_links = []
        # player_names = []
        player_s_name_link = {}

        # get tags with players
        players = self.__driver.find_elements_by_css_selector('tbody tr td:nth-child(1) a')

        for player in players:
            # get one player statistics
            link = player.get_attribute('href').replace('overview', 'stats?co=1&se=274')
            # get player name
            name = player.get_attribute('innerHTML')
            # delete <img> tag
            name = re.split(r'>', name)[-1]
            # print(name)

            # remove duplicate players (site error)
            player_s_name_link[name] = link
            # link to player statistics
            # player_links.append(link)
            # player_names.append(name)

        # print(player_names)
        # print(player_links)

        advert_flag = True
        dfs_stats = []

        for p_name, p_link in player_s_name_link.items():
            self.__go_url(p_link)

            # one time close the advert
            if advert_flag:
                self.__close_adevert()
                advert_flag = False

            # wait 2 secends to open and load the page
            time.sleep(2)

            # get stats
            df = self.get_player_stats(p_name)
            dfs_stats.append(df)

        # combine all dataframes in one
        df = pd.concat(dfs_stats)

        # save datafrome to disk
        df.to_csv(f'clubs/{club_name}.csv')

    def get_player_stats(self, name):
        ''' get DataFrame with statistics from player '''

        df_stats = pd.Series()
        stats_list = []
        for stat in self.__driver.find_elements_by_css_selector('div.statsListBlock .normalStat span:first-child'):
            # get text value
            key = stat.get_attribute('innerHTML')
            # remove img tag from text
            stats_list.append(key.split('<')[0])

        # change list to dataSeries
        for i in range(0, len(stats_list), 2):
            k = i
            v = i + 1
            # add skill: value
            df_stats[stats_list[k]] = stats_list[v].strip()

        # get an additional variable: appearances
        appearances = self.__driver.find_elements_by_css_selector('span.allStatContainer.statappearances')[
            0].get_attribute('innerHTML')
        df_stats['Appearances'] = appearances

        # change dataSeries to dataFrame
        df_stats = pd.DataFrame(data=[df_stats.values], columns=df_stats.index, index=[name])
        print(f'{name}:')
        print(df_stats)

        return df_stats
        # print('Appearances: ', appearances)


def main():
    # iterate through each club
    for club_name, cl_appendix in CLUBS_CL.items():
        # if club_name in ('Arsenal', 'Aston Villa', 'AFC Bournemouth'):
        #     continue
        clubs_stats = PlayerStatistics(cl_appendix)
        clubs_stats.get_players(club_name)
        # close selenium driver
        clubs_stats.close_driver()


if __name__ == '__main__':
    main()
