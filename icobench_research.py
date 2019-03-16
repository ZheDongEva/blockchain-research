# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import os
import time
import lxml
import re
import urllib2
import tweepy

class Spider(object):
    def __init__(self):
        self.session = requests.session()
        self.targetUrl = None
        self.headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        }

    def getResponse(self, url=None):
        try:
            self.session.headers = self.headers
            self.targetUrl = url
            resp = self.session.get(self.targetUrl, headers = self.headers)
            return resp
        except Exception as e:
            print(e)
            return ""

    def getID(self, url):
        try:
            name = []
            content = self.getResponse(url).content
            title = SoupStrainer('div', attrs = {'class': 'ico_list'})
            soup = BeautifulSoup(content, "lxml", parse_only = title)
            values = soup.select('a[class="name"]')
            for i in values:
                tmp = re.findall("\w+", i['href'])
                del tmp[0]
                name.append('-'.join(tmp))
            return name
        except Exception as e:
            print(e)
            return ""

    def getICOBenchLink(self, id):
        url = 'https://icobench.com/ico/%s/' % id
        try:
            return url
        except Exception as e:
            print(e)
            return ''

    def getSocialLink(self, id):
        url = 'https://icobench.com/ico/%s/' % id
        try:
            content = self.getResponse(url).content
            title = SoupStrainer('div', attrs = {'class': 'socials'})
            soup = BeautifulSoup(content, "lxml", parse_only = title)
            twitter = soup.select('a[class="twitter"]')
            facebook = soup.select('a[class="facebook"]')
            telegram = soup.select('a[class="telegram"]')
            website = soup.select('a[class="www"]')
            social = []

            if telegram:
                for i in telegram:
                    social.append(i['href'])
                    break
            else:
                social.append("0")

            if facebook:
                for i in facebook:
                    social.append(i['href'])
                    break
            else:
                social.append("0")

            if twitter:
                for i in twitter:
                    social.append(i['href'])
                    break
            else:
                social.append("0")

            if website:
                for i in website:
                    social.append(i['href'])
                    break
            else:
                social.append("0")

            return social
        except Exception as e:
            print(e)
            return ['0', '0', '0', '0']

    def getRatings(self, id):
        url = 'https://icobench.com/ico/%s/' % id
        try:
            content = self.getResponse(url).content
            title = SoupStrainer('div', attrs = {'class': 'fixed_data'})
            soup = BeautifulSoup(content, "lxml", parse_only = title)
            rating = soup.find('div', itemprop = 'ratingValue')
            subRating = soup.select('div[class="col_4"]')
            ratings = []
            ratings.append(rating['content'])
            for i in subRating:
                tmp = re.findall("\d+", i.get_text())
                if tmp:
                    ratings.append('.'.join(tmp))
                else:
                    ratings.append(0)
            return ratings
        except Exception as e:
            print(e)
            return ''

    def getDate(self, url):
        try:
            start = []
            end = []
            content = self.getResponse(url).content
            title = SoupStrainer('div', attrs = {'class': 'ico_list'})
            soup = BeautifulSoup(content, "lxml", parse_only = title)
            date = soup.select('div[class="row"]')
            num = 1;
            for i in date:
                if num%3 == 1:
                    tmp = i.get_text()
                    start.append(tmp[7:])
                if num % 3 == 2:
                    tmp = i.get_text()
                    end.append(tmp[5:])
                num += 1
            return start, end
        except Exception as e:
            print(e)
            return ''

    # def getDateEnd(self, url):
    #     try:
    #         end = []
    #         content = self.getResponse(url).content
    #         title = SoupStrainer('div', attrs = {'class': 'ico_list'})
    #         soup = BeautifulSoup(content, "lxml", parse_only = title)
    #         date = soup.select('div[class="row"]')
    #         num = 1;
    #         for i in date:
    #             if num%3 == 2:
    #                 tmp = i.get_text()
    #                 end.append(tmp[5:])
    #             num += 1
    #         return end
    #     except Exception as e:
    #         print(e)

    def getFinancial(self, id):
        try:
            url = 'https://icobench.com/ico/%s/' % id
            content = requests.get(url).content
            title = SoupStrainer('div', attrs={'id': 'financial'})
            soup = BeautifulSoup(content, "lxml", parse_only=title)
            tmp0 = soup.select('div[class="value"]')
            tmp = soup.select('div[class="label"]')
            financial = {}
            for i, j in zip(tmp, tmp0):
                financial[i.get_text()] = j.get_text().replace('\t', '')
            financialResult = {}
            if financial.has_key("Type"):
                financialResult["Type"] = financial["Type"]
            else:
                financialResult["Type"] = 0

            if financial.has_key("Raised"):
                financialResult["Raised"] = financial["Raised"]
            else:
                financialResult["Raised"] = 0

            if financial.has_key("Token"):
                financialResult["Token"] = financial["Token"]
            else:
                financialResult["Token"] = 0

            if financial.has_key("Platform"):
                financialResult["Platform"] = financial["Platform"]
            else:
                financialResult["Platform"] = 0

            return financialResult
        except Exception as e:
            print(e)
            return {"Type": 0, "Platform": 0, "Symbol": 0 ,"Raised": 0}

    def getFacebookNum(self, facebook):
        try:
            if facebook == "0":
                return 0
            else:
                content = requests.get(facebook).content
                title = SoupStrainer('div', attrs={'class': 'clearfix _ikh'})
                soup = BeautifulSoup(content, "lxml", parse_only=title)
                value = soup.select('div[class="_4bl9"]')
                count = []
                tmp = re.findall("\d+", value[1].get_text())
                count.append(''.join(tmp))
                return (count[0])
        except Exception as e:
            print(e)
            return 0

    def getTwitterNum(self, twitter):
        try:
            if twitter == "0":
                return 0
            else:
                account = re.findall("\w+", twitter)
                consumer_key = "pTg8ySoedFsiowjF5p44FfrkJ"
                consumer_secret = "I5bBTF2ZbPLdLWMu4NzHm3AmrdUiSSZd27UUpctVDaRwy2ARxJ"
                access_token = "937166242208763904-S51fserjPs8bqkdavOC4gMuBU2Oq9xi"
                access_token_secret = "FzpMOJzlYNS0mE9zeE9IgNKNOHTgLfuTtb6FH96ntFtyM"
                # Tweepy OAuthHandler
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                user = api.get_user(account[-1])
                return user.followers_count
        except Exception as e:
            print(e)
            return 0

    def getTelegramNum(self, telegram):
        try:
            if telegram == "0":
                return 0
            else:
                content = requests.get(telegram).content
                title = SoupStrainer('div', attrs = {'class': 'tgme_page_wrap'})
                soup = BeautifulSoup(content, "lxml", parse_only = title)
                value = soup.select('div[class="tgme_page_extra"]')
                count = []
                tmp = re.findall("\d+", value[0].get_text())
                count.append(''.join(tmp))
                return(count[0])
        except Exception as e:
            print(e)
            return 0

    def dumpCSV(self):
        path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'icoCoinRating.csv')
        urls = ['https://icobench.com/icos?page={}'.format(str(i)) for i in range(147, 309)]
        with open(path, 'w') as f:
            # fieldnames = ['name', 'link', 'rating', 'ico_profile', 'team', 'vision', 'product', 'start', 'end', 'www', 'telegram', 'telegram_count', 'facebook', 'facebook_count', 'twitter', 'twitter_count']
            fieldnames = ['name', 'link', 'rating', 'start', 'end', 'website', 'telegram', 'telegram_count', 'facebook', 'facebook_count', 'twitter', 'twitter_count', 'symbol', 'platform', 'type', 'raised']
            wr = csv.DictWriter(f, fieldnames=fieldnames)
            wr.writeheader()
            i = 1
            for url in urls:
                ID = self.getID(url)
                start, end = self.getDate(url)
                # end = self.getDateEnd(url)
                for x, y, z in zip(ID, start, end):
                    try:
                        print(i, x)
                        link = self.getICOBenchLink(x)
                        ratings = self.getRatings(x)
                        socialLink = self.getSocialLink(x)
                        financial = self.getFinancial(x)
                        telegram = socialLink[0].encode('ascii', 'ignore').decode('ascii')
                        facebook = socialLink[1].encode('ascii', 'ignore').decode('ascii')
                        twitter = socialLink[2].encode('ascii', 'ignore').decode('ascii')
                        website = socialLink[3].encode('ascii', 'ignore').decode('ascii')
                        telegram_count = self.getTelegramNum(telegram)
                        twitter_count = self.getTwitterNum(twitter)
                        facebook_count = self.getFacebookNum(facebook)
                        wr.writerow({'name': x, 'link': link, 'rating': ratings[0], 'start': y, 'end': z, 'website': website, 'telegram': telegram, 'telegram_count': telegram_count, 'facebook': facebook, 'facebook_count': facebook_count, 'twitter': twitter, 'twitter_count': twitter_count, 'symbol': financial["Token"], 'platform': financial["Platform"], 'type': financial["Type"], 'raised': financial["Raised"]})
                    except Exception as e:
                        print(e)
                    i += 1

if __name__ == '__main__':
    spider = Spider()
    start = time.time()
    spider.dumpCSV()
    print(time.time() - start)
