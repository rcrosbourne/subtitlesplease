import logging
import re
import requests
import zipfile
import io
import os
import tempfile
import shutil
from lxml import html

from modules.basesubtitles import BaseSubtitles


class Subscene(BaseSubtitles):
    """
    This module is responsible for getting subtiles from subscene.com
    """
    SEARCH_URL = "https://subscene.com/subtitles/release?q="
    BASE_URL = "https://subscene.com"

    def get_subtitles(self, title=None, location=None, language="English"):
        """
        Get the subtitles in 3 phases
        1) query for title
        2) select the best subtitle
        3) download the subtitle to location
        :param language: Language of subtitle
        :param title: Video title to search for
        :param location: location on the filesystem to store subtitle
        :return: True of subtitle was found false otherwise
        """
        try:
            logging.info("%s Getting title of %s to store %s" % (str(self), title, location))
            subtitle_list = self.query_subscene(title=title, language=language)
            logging.info("%s subtitles found" % len(subtitle_list))
            if len(subtitle_list) > 0:
                subtitle = self.best_subtitle_from_list(subtitle_list, title)
                if subtitle:
                    self.download_subtitle(subtitle=subtitle, location=location, title=title)
                    return True
                else:
                    logging.info("No suitable subtitles were found")
                    return False
            return False
        except Exception as ex:
            logging.error("An error occurred getting subs: %s" % ex)
            return False

    @staticmethod
    def best_subtitle_from_list(subtitle_list, title):
        """
        This function should pick the best subtitle for our title
        prioritizing HI.
        :param subtitle_list:
        :param title:
        :return: best subtitle match
        """
        try:
            # if it is a tv show we need to prioritze correctness
            tv_show_regex = "([sS]\d{2}[eE]\d{2})"
            tv_show_check = re.compile(tv_show_regex)
            res = tv_show_check.search(title)
            filtered_list = []
            logging.info("Getting best subtitle from list")
            if res:
                logging.info("Title appears to be a TV-Show")
                # title is a tv-show we need to search for the same tv-show in our list
                # eliminate those that aren't
                (value,) = res.groups()
                new_re = re.compile(value)
                for sub in subtitle_list:
                    if new_re.search(sub.title):
                        # now we know we have the correct Season and Episode
                        # we now need to ensure we have the right title.
                        # that is everything to the left of S00E00 must match
                        left_of_title = title.split(value)[0]
                        left_of_subtitle_title = sub.title.split(value)[0]
                        if left_of_title.lower() == left_of_subtitle_title.lower():
                            # now we know we have the right title
                            # I am biased to hearing impaired subtitles done by GoldenBeard
                            # So I will select that to return otherwise any will do
                            filtered_list.append(sub)
                if len(filtered_list) > 0:
                    preferred_choice = [x for x in filtered_list if x.owner == "GoldenBeard" and x.hearing_impaired]
                    if len(preferred_choice) > 0:
                        return preferred_choice[0]
                    else:
                        return filtered_list[0]
                else:
                    # No subtitles found
                    logging.info("No subtitles were found")
                    return None
            else:
                # this is not a tv-show but a movie.
                # there is no good way to check for accuracy
                # So we are just going to compare string for string separated by .
                # assign a point for any match and return the subtitle with the hishest points
                logging.info("Title is a movie")
                title_strings = title.split(".")
                sub_with_score_list = []
                for sub in subtitle_list:
                    sub_title_strings = sub.title.split(".")
                    values = set(title_strings).intersection(sub_title_strings)
                    # lets calculate relevance as a % of matches
                    relevance = (len(values) / len(title_strings)) * 100
                    # Ignore relevance less than 20%
                    if relevance > 20:  # I call this tolerance
                        sub_with_score_list.append((sub, relevance))
                # now we have a list of tuples with subtitles and their score.
                # we have eliminated anything below our tolerance of 20%
                # how do we choose
                # Ideally we want 100% relevance. Lets start with those
                hundred_percent_relevance = [(x, y) for (x, y) in sub_with_score_list if y == 100]
                if len(hundred_percent_relevance) > 0:
                    logging.info("We have a title with 100% relevance. Lets take it")
                    return hundred_percent_relevance[0][0]
                else:
                    # We don't have 100%. Lets be strict and only allow those with 1 difference
                    min_tolerance = ((len(title_strings) - 1) / len(title_strings)) * 100
                    logging.info("No movie had 100 percent relevance lets settle for %0.2f tolerance" % min_tolerance)
                    min_tolerance_list = sorted([(x, y) for (x, y) in sub_with_score_list if y >= min_tolerance],
                                                key=lambda x: x[1])
                    if min_tolerance_list and len(min_tolerance_list) > 0:
                        # return the one with the highest relevance
                        return min_tolerance_list[0][0]
                    else:
                        logging.info("No subtitles lvl 1 minimum tolerance. Lets go 1 lvl worse")
                        min_tolerance = ((len(title_strings) - 2) / len(title_strings)) * 100
                        logging.info(
                            "Lets settle for %0.2f tolerance" % min_tolerance)
                        min_tolerance_list = sorted([(x, y) for (x, y) in sub_with_score_list if y >= min_tolerance],
                                                    key=lambda x: x[1])
                        if min_tolerance_list and len(min_tolerance_list) > 0:
                            # return the one with the highest relevance
                            return min_tolerance_list[0][0]
                        else:
                            logging.info("Any lower and we jeopardize accuracy we are stopping here")
                            return None
        except Exception as ex:
            logging.error("Something went wrong %s" % ex)
            return None

    def __str__(self):
        return "Subscene"

    def query_subscene(self, title, language="English"):
        try:
            r = requests.post(url=self.SEARCH_URL + title)
            tree = html.fromstring(r.content)
            rows = tree.xpath("//*[@id=\"content\"]/div[1]/div/div/table/tbody/tr")
            results = []
            for row in rows:
                sub_s = SubsceneSubs()
                lang = row.xpath("td[1]/a/span[1]/text()")[0].strip()
                if lang == language:
                    sub_s.language = row.xpath("td[1]/a/span[1]/text()")[0].strip()
                    sub_s.title = row.xpath("td[1]/a/span[2]/text()")[0].strip()
                    sub_s.link = row.xpath("td[1]/a/@href")[0].strip()
                    sub_s.owner = row.xpath("td[4]/a/text()")[0].strip()
                    sub_s.hearing_impaired = len(row.xpath("td[3][contains(@class, 'a41')]")) == 1
                    results.append(sub_s)
            return results
        except Exception as ex:
            logging.error("An error occurred fetching subs: %s" % ex)

    def download_subtitle(self, subtitle, location, title):
        try:
            r = requests.get(url=self.BASE_URL + subtitle.link)
            subtitle_page = html.fromstring(r.content)
            subtitle_download_link = subtitle_page.xpath("//*[@id=\"downloadButton\"]/@href")[0].strip()
            if subtitle_download_link:
                # this is the link to do the download file
                # lets use BytesIO to read that shit
                r = requests.get(url=self.BASE_URL + subtitle_download_link)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                file_list = z.namelist();
                subtitle_only = [sub for sub in file_list if sub.endswith("srt")]
                # rename the file
                # create a temp directory to extract files
                temp_dir = tempfile.mkdtemp()
                z.extractall(path=temp_dir, members=subtitle_only)
                # rename downloaded subtitle to location with title name
                # if title contains extension (avi, mp4, mkv) remove it otherwise use the title
                renamed_string = ""
                if title.endswith(".avi") or title.endswith(".mkv") or title.endswith(".mp4"):
                    renamed_string = title[:-4]
                else:
                    renamed_string = title
                shutil.move(os.path.join(temp_dir, subtitle_only[0]), os.path.join(location, renamed_string + ".srt"))
                # remove tempdir
                shutil.rmtree(temp_dir)
        except Exception as ex:
            logging.error("Error while downloading subtitle: %s" % ex)


class SubsceneSubs(object):
    def __init__(self, language="English", title="", owner="", link="", hearing_impaired=False):
        self.language = language
        self.title = title
        self.owner = owner
        self.link = link
        self.hearing_impaired = hearing_impaired
