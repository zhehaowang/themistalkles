#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import random
import pprint
import datetime

from helpers import get_structured_feeds

class TestParsing(unittest.TestCase):
    def setUp(self):
        return

    def test_parse_textfeeds(self):
        feeds = [
            'christopher__yang liked 8 posts. 41m',
            "miebakayohannes liked familynofriends14's post. 60m",
            "dustin_oharry and randy.illum liked fitzfitzfitzfitzfitz's post. 2h",
            'ytong_chn liked 5 posts. 2h',
            'sjs7007 started following alydiaz and uber. 4h',
            'jcwangins started following jsyabc217. 5h',
            'jcwangins liked 2 posts. 5h',
            'yukaitu liked 2 posts. 6h',
            'jorlenise started following leeoralexandra and tughuart. 6h',
            'stumblex liked 8 posts. 7h',
            "junjuewang liked ji_ye_'s post. 7h",
            "sunny_liiiii liked changmin88's post. 11h",
            "kooorio liked avant.arte's post. 12h",
            "randy.illum liked j_slash_k's post. 18h",
            'christopher__yang liked 5 posts. 19h',
            'yemaobisutorozipterasu shared 3 posts at お肉とワイン野毛ビストロzip 19h',
            'randy.illum started following barstoolsports, erikalee305 and steadmanart. 20h',
            "skylar.hly liked ameliewenzhao's post. 21h",
            "diraccat liked tianjinye9's post. 21h",
            'lbysophia liked 4 posts. 1d',
            'dustin_oharry liked 4 posts. 1d',
            'skylar.hly started following thoughtcatalog, wilderpoetry and 2 others. 1d']
        # TODO: fix
        # liked siyuqtt's comment: 沉舟侧畔千帆过 病树前头万木春 一切都会变好的！
        structured_feeds = get_structured_feeds(feeds, datetime.datetime(2018, 11, 18, 19, 15, 18, 21885))

        expectation = [ {   'action': 'liked',
                            'count': 8,
                            'subject': ['christopher__yang'],
                            'time': datetime.datetime(2018, 11, 18, 18, 34, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['miebakayohannes'],
                            'target': ['familynofriends14'],
                            'time': datetime.datetime(2018, 11, 18, 18, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['dustin_oharry', 'randy.illum'],
                            'target': ['fitzfitzfitzfitzfitz'],
                            'time': datetime.datetime(2018, 11, 18, 17, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 5,
                            'subject': ['ytong_chn'],
                            'time': datetime.datetime(2018, 11, 18, 17, 15, 18, 21885)},
                          { 'action': 'started_following',
                            'subject': ['sjs7007'],
                            'target': ['alydiaz', 'uber'],
                            'time': datetime.datetime(2018, 11, 18, 15, 15, 18, 21885)},
                          { 'action': 'started_following',
                            'subject': ['jcwangins'],
                            'target': ['jsyabc217'],
                            'time': datetime.datetime(2018, 11, 18, 14, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 2,
                            'subject': ['jcwangins'],
                            'time': datetime.datetime(2018, 11, 18, 14, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 2,
                            'subject': ['yukaitu'],
                            'time': datetime.datetime(2018, 11, 18, 13, 15, 18, 21885)},
                          { 'action': 'started_following',
                            'subject': ['jorlenise'],
                            'target': ['leeoralexandra', 'tughuart'],
                            'time': datetime.datetime(2018, 11, 18, 13, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 8,
                            'subject': ['stumblex'],
                            'time': datetime.datetime(2018, 11, 18, 12, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['junjuewang'],
                            'target': ['ji_ye_'],
                            'time': datetime.datetime(2018, 11, 18, 12, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['sunny_liiiii'],
                            'target': ['changmin88'],
                            'time': datetime.datetime(2018, 11, 18, 8, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['kooorio'],
                            'target': ['avant.arte'],
                            'time': datetime.datetime(2018, 11, 18, 7, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['randy.illum'],
                            'target': ['j_slash_k'],
                            'time': datetime.datetime(2018, 11, 18, 1, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 5,
                            'subject': ['christopher__yang'],
                            'time': datetime.datetime(2018, 11, 18, 0, 15, 18, 21885)},
                          { 'action': 'shared',
                            'count': 3,
                            'subject': ['yemaobisutorozipterasu'],
                            'target': ['お肉とワイン野毛ビストロzip'],
                            'time': datetime.datetime(2018, 11, 18, 0, 15, 18, 21885)},
                          { 'action': 'started_following',
                            'subject': ['randy.illum'],
                            'target': ['barstoolsports', 'erikalee305', 'steadmanart'],
                            'time': datetime.datetime(2018, 11, 17, 23, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['skylar.hly'],
                            'target': ['ameliewenzhao'],
                            'time': datetime.datetime(2018, 11, 17, 22, 15, 18, 21885)},
                          { 'action': 'liked',
                            'subject': ['diraccat'],
                            'target': ['tianjinye9'],
                            'time': datetime.datetime(2018, 11, 17, 22, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 4,
                            'subject': ['lbysophia'],
                            'time': datetime.datetime(2018, 11, 17, 19, 15, 18, 21885)},
                          { 'action': 'liked',
                            'count': 4,
                            'subject': ['dustin_oharry'],
                            'time': datetime.datetime(2018, 11, 17, 19, 15, 18, 21885)},
                          { 'action': 'started_following',
                            'subject': ['skylar.hly'],
                            'target': ['thoughtcatalog', 'wilderpoetry', 'unknown', 'unknown'],
                            'time': datetime.datetime(2018, 11, 17, 19, 15, 18, 21885)}]

        self.assertEqual(len(feeds), len(structured_feeds))
        self.assertEqual(expectation, structured_feeds)

if __name__ == '__main__':
    unittest.main()
