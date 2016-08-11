#!/usr/bin/env python
import sys
sys.path.append('../')
import unittest
import hipcard
import requests
import requests_mock
import argparse

@requests_mock.Mocker()
class C_HIPCARD(unittest.TestCase):

    def setUp(self):
        self.sendto = "testroom"
        self.msg = ('name: "Test Trigger Name" \n'
                    'id: "1234567" \n'
                    'status: "OK" \n'
                    'hostname: "xyz.com" \n'
                    'event_id: "987654321" \n'
                    'severity: "Disaster" \n'
                    'url: "url.xyz.com" \n'
                    'description: "Test Trigger Description"')
        self.hipurl = "testhipurl"
        self.hiptoken = "abcedfg12345678"
        self.zbxurl = "https://zbx.test.com"
        self.okimg = "http://xyz.com/ok.png"
        self.probimg = "http://xyz.com/prob.png"


    def test_sendmsg(self, m):
        testtext = (u'{"color": "green", "message": "OK:Test Trigger Name \\n '
                   '<a href=\'https://zbx.test.com/tr_comments.php?triggerid='
                   '1234567\'>More Information</a> | <a href=\'https://zbx.test'
                   '.com/events.php?filter_set=1&triggerid=1234567&period='
                   '604800\'>Events</a> | <a href=\'https://zbx.test.com/'
                   'zabbix.php?action=acknowledge.edit&acknowledge_type=1&'
                   'eventids[]=987654321&backurl=tr_status.php\'>Acknowledge'
                   '</a> | <a href=\'url.xyz.com\'>Trigger Link</a></b>",'
                   ' "notify": "true", "card": {"style": "application",'
                   ' "activity": {"html": "<b><span class=\'aui-lozenge '
                   'aui-lozenge-success\'>OK</span> Test Trigger Name</b>"}, '
                   '"icon": {"url": "http://xyz.com/ok.png"}, "format": '
                   '"medium", "url": "https://zbx.test.com/events.php?'
                   'filter_set=1&triggerid=1234567&period=604800", '
                   '"attributes": [{"value": {"style": "lozenge-success", '
                   '"label": "OK"}, "label": "Status"}, {"value": {"style": '
                   '"lozenge-error", "label": "Disaster"}, "label": "Severity"}'
                   ', {"value": {"style": "lozenge", "label": "xyz.com"}, '
                   '"label": "Hostname"}], "title": "Test Trigger Name", '
                   '"id": "987654321", "description": {"value": "<b>'
                   '<a href=\'https://zbx.test.com/tr_comments.php?triggerid='
                   '1234567\'>More Information</a> | <a href=\'https://zbx.test'
                   '.com/events.php?filter_set=1&triggerid=1234567&period='
                   '604800\'>Events</a> | <a href=\'https://zbx.test.com/'
                   'zabbix.php?action=acknowledge.edit&acknowledge_type=1&'
                   'eventids[]=987654321&backurl=tr_status.php\'>Acknowledge'
                   '</a> | <a href=\'url.xyz.com\'>Trigger Link</a></b>",'
                   ' "format": "html"}}, "message_format": "html"}')
        testurl = (u'https://testhipurl.hipchat.com/v2/room/testroom/'
                   'notification?auth_token=abcedfg12345678')
        m.register_uri(requests_mock.ANY, 'https://testhipurl.hipchat.com/v2/room/testroom/notification?auth_token=abcedfg12345678', text='resp')
        test = hipcard.ZabbixAlert(self.sendto, self.msg, self.hipurl,
                                   self.hiptoken, self.zbxurl)
        test.images(okimg=self.okimg, probimg=self.probimg)
        resp = test.sendmsg()
        self.assertEqual(resp.request.text, testtext)
        self.assertEqual(resp.url, testurl)

    def test_main(self, m):
        testtext = (u'{"color": "green", "message": "OK:Test Trigger Name \\n '
                   '<a href=\'https://zbx.test.com/tr_comments.php?triggerid='
                   '1234567\'>More Information</a> | <a href=\'https://zbx.test'
                   '.com/events.php?filter_set=1&triggerid=1234567&period='
                   '604800\'>Events</a> | <a href=\'https://zbx.test.com/'
                   'zabbix.php?action=acknowledge.edit&acknowledge_type=1&'
                   'eventids[]=987654321&backurl=tr_status.php\'>Acknowledge'
                   '</a> | <a href=\'url.xyz.com\'>Trigger Link</a></b>",'
                   ' "notify": "true", "card": {"style": "application",'
                   ' "activity": {"html": "<b><span class=\'aui-lozenge '
                   'aui-lozenge-success\'>OK</span> Test Trigger Name</b>"}, '
                   '"icon": {"url": "http://xyz.com/ok.png"}, "format": '
                   '"medium", "url": "https://zbx.test.com/events.php?'
                   'filter_set=1&triggerid=1234567&period=604800", '
                   '"attributes": [{"value": {"style": "lozenge-success", '
                   '"label": "OK"}, "label": "Status"}, {"value": {"style": '
                   '"lozenge-error", "label": "Disaster"}, "label": "Severity"}'
                   ', {"value": {"style": "lozenge", "label": "xyz.com"}, '
                   '"label": "Hostname"}], "title": "Test Trigger Name", '
                   '"id": "987654321", "description": {"value": "<b>'
                   '<a href=\'https://zbx.test.com/tr_comments.php?triggerid='
                   '1234567\'>More Information</a> | <a href=\'https://zbx.test'
                   '.com/events.php?filter_set=1&triggerid=1234567&period='
                   '604800\'>Events</a> | <a href=\'https://zbx.test.com/'
                   'zabbix.php?action=acknowledge.edit&acknowledge_type=1&'
                   'eventids[]=987654321&backurl=tr_status.php\'>Acknowledge'
                   '</a> | <a href=\'url.xyz.com\'>Trigger Link</a></b>",'
                   ' "format": "html"}}, "message_format": "html"}')
        testurl = (u'https://testhipurl.hipchat.com/v2/room/testroom/'
                   'notification?auth_token=abcedfg12345678')
        m.register_uri(requests_mock.ANY, 'https://testhipurl.hipchat.com/v2/room/testroom/notification?auth_token=abcedfg12345678', text='resp')
        sys.argv = ["x", self.sendto, self.msg, self.hipurl, self.hiptoken, self.zbxurl, self.okimg, self.probimg]
        test = hipcard.main()
        self.assertEqual(test.request.text, testtext)
        self.assertEqual(test.url, testurl)

if __name__ == "__main__":
    unittest.main()

