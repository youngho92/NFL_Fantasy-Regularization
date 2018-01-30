## This file is to scrap historical performance of players and teams

import scrapy
import pandas as pd


class TestSpider(scrapy.Spider):
    name = "test_spider"
    start_urls = ['https://www.footballdb.com/fantasy-football/index.html?pos=QB&yr=2010&wk=1&rules=1']

    # make a list to iterate different positions, years, and weeks
    url_loop = [position + '-' + str(year) + '-' + str(week) for position in ['QB', 'WR', 'RB', 'TE', 'K', 'DST'] \
    for year in range(2010, 2018) for week in range(1, 18)]
    index = 0

    def parse(self, response):
        
        # player names
        names = response.xpath('//div//table//span[@class="hidden-xs"]//a/text()').extract()
        home_teams = response.xpath('//div//table//td[@class="center"]/b/text()').extract()
        away_teams = response.xpath('//div//table//td[@class="center"]/text()').extract()
        # remove @ from away_teams
        away_teams = [s.replace("@", "") for s in away_teams]

        # extract stats for every player
        player_stats = response.xpath('//div//table//tr//td/text()').extract()
        # extract columns and arrange the data by column
        titles = response.xpath('//div//a/@title').extract()
        len_titles = len(titles)
        len_names = len(names)
        stats = [[player_stats[(1+len_titles)*i+j] for i in range(len_names)] for j in range(1, 1+len_titles)]


        yield {self.url_loop[self.index]: [names, home_teams, away_teams, titles, stats]}

        # next url
        self.index += 1

        next_pos = self.url_loop[self.index].split('-')[0]
        next_yr = self.url_loop[self.index].split('-')[1]
        next_wk = self.url_loop[self.index].split('-')[2]
        next_url = 'https://www.footballdb.com/fantasy-football/index.html?pos=' + next_pos\
        + '&yr=' + next_yr + '&wk=' + next_wk + '&rules=1'

        if self.index < len(self.url_loop):
            yield scrapy.Request(
                response.urljoin(next_url),
                callback=self.parse
            )
