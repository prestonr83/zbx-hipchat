#!/usr/bin/env python
"""Zabbix Action Alert Script for HipChat v2 API.

This module fires off messages to HipChat using the cards layout that is
collapse-able. The alerts contain links to the following areas within Zabbix.
Trigger Descriptions
Past Events for the Trigger
Acknowledgement form for the Trigger
URL Link for URL Defined in the Trigger
"""
import re
import sys
import json
import requests


class ZabbixAlert(object):
    """Parses Zabbix message and formats it for consumption by HipChat v2 API.

    The _description method is not currently used due to 5
    line limit in hipchat card messages.

    Attributes:
        images(okimg, probimg): Provide the URLs for images to use as icons
                                for OK and PROBLEM states.
        sendmsg(): Sends the formatted JSON to the HipChat API endpoint.

    """

    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, roomid, message, hipname, token, zbxurl):
        """
        The __init__ method requires 4 arguments.

        Args:
            roomid (int): The room ID for the HipChat room to be alerted.
                          This would be the {ALERT.SENDTO} macro from Zabbix.

            message (str): The message would be the {ALERT.MESSAGE} macro from
                           Zabbix.

                           It should be formatted like the following

                           name: "{TRIGGER.NAME}"
                           id: "{TRIGGER.ID}"
                           status: "{TRIGGER.STATUS}"
                           hostname: "{HOSTNAME}"
                           event_id: "{EVENT.ID}"
                           severity: "{TRIGGER.SEVERITY}"
                           url: "{TRIGGER.URL}"
                           description: "{TRIGGER.DESCRIPTION}"

            hipname (str): The company name for your hipchat account.

            token (str): The HipChat v2 API token.

            zbxurl (str): The FQDN of your Zabbix installation.
        """
        self.roomid = roomid
        self.message = message
        self.hipname = hipname
        self.token = token
        self.zbxurl = zbxurl
        self.okimg = "http://"
        self.probimg = "http://"

    def _parse(self):
        pattern = (r'name: *"(.*)"\s*id: *"(.*)"\s*status: *"(.*)"\s*hostname:'
                   r' *"(.*)"\s*event_id: *"(.*)"\s*severity: *"(.*)"\s*url: *'
                   r'"(.*)"\s*description: *"([\w\W\s]*)"')
        matches = re.match(pattern, self.message)
        return matches

    def _name(self):
        name = self._parse()
        return name.group(1)

    def _triggerid(self):
        triggerid = self._parse()
        return triggerid.group(2)

    def _status(self):
        status = self._parse()
        return status.group(3)

    def _hostname(self):
        hostname = self._parse()
        return hostname.group(4)

    def _eventid(self):
        eventid = self._parse()
        return eventid.group(5)

    def _severity(self):
        sev = self._parse()
        return sev.group(6)

    def _url(self):
        url = self._parse()
        if url.group(7) == "":
            url = "#"
        else:
            url = url.group(7)
        return url

    def _description(self):
        """This is here for future use. It is not currently implemented."""
        desc = self._parse()
        return desc.group(8)

    def images(self, okimg=None, probimg=None):
        """Set the image URLS for the icons used in OK and PROBLEM states."""
        self.okimg = okimg
        self.probimg = probimg

    def _statassets(self):
        if self._status() == "PROBLEM":
            statlozenge = "lozenge-error"
            img = self.probimg
        if self._status() == "OK":
            statlozenge = "lozenge-success"
            img = self.okimg
        return (statlozenge, img)

    def _sevassets(self):
        if self._severity() == "Not classified" or \
           self._severity() == "Information":
            sevlozenge = "lozenge"
            msgcolor = "gray"
        elif self._severity() == "Warning" or self._severity() == "Average":
            sevlozenge = "lozenge-current"
            msgcolor = "yellow"
        elif self._severity() == "High" or self._severity() == "Disaster":
            sevlozenge = "lozenge-error"
            msgcolor = "red"
        if self._status() == "OK":
            msgcolor = "green"
        return (sevlozenge, msgcolor)

    def _formatmessage(self):
        message = ("{0}:{1} \n <a href='{5}"
                   "/tr_comments.php?triggerid={2}'>More Information</a> | "
                   "<a href='{5}/events.php?"
                   "filter_set=1&triggerid={2}&period=604800'>Events</a> | "
                   "<a href='{5}/zabbix.php?"
                   "action=acknowledge.edit&acknowledge_type=1&"
                   "eventids[]={3}&backurl=tr_status.php'>Acknowledge</a> | "
                   "<a href='{4}'>Trigger Link</a></b>") \
                    .format(self._status(), self._name(), self._triggerid(),
                            self._eventid(), self._url(), self.zbxurl)
        return message

    def _card(self):
        statloz, statimg = self._statassets()
        sevloz, _ = self._sevassets()
        card = {
            "style": "application",
            "format": "medium",
            "url": ("{1}/events.php?filter_set=1&"
                    "triggerid={0}&period=604800").format(self._triggerid(),
                                                          self.zbxurl),
            "id": self._eventid(),
            "title": self._name(),
            "activity": {
                "html": ("<b><span class='aui-lozenge aui-{0}'>{1}</span> {2}"
                         "</b>").format(statloz, self._status(), self._name())},
            "description": {
                "format": "html",
                "value": ("<b><a href='{3}/"
                          "tr_comments.php?triggerid={0}'>More Information</a>"
                          " | <a href='{3}/events.php?"
                          "filter_set=1&triggerid={0}&period=604800'>Events</a>"
                          " | <a href='{3}/zabbix.php?"
                          "action=acknowledge.edit&acknowledge_type=1&"
                          "eventids[]={1}&backurl=tr_status.php'>Acknowledge"
                          "</a> | <a href='{2}'>Trigger Link</a></b>").format(
                              self._triggerid(), self._eventid(), self._url(),
                              self.zbxurl)},
            "icon": {"url": statimg},
            "attributes": [{
                "value": {
                    "label": self._status(),
                    "style": statloz
                },
                "label": "Status"
                },
                {"value": {
                    "label": self._severity(),
                    "style": sevloz
                },
                "label": "Severity"
                },
                {"value": {
                    "label": self._hostname(),
                    "style": "lozenge"
                },
                "label": "Hostname"
                },
            ],
        }
        return card

    def sendmsg(self):
        """Sends the message data to the HipChat API.
           Call it after calling the Class with needed parameters
           to send the message"""
        _, color = self._sevassets()
        payload = {'notify': 'true', 'color': color, 'message':
                  self._formatmessage(), 'card': self._card(), 'message_format':
                  'html'}
        params = {'auth_token': self.token}
        resp = requests.post('https://{0}.hipchat.com/v2/room/{1}/notification'.
                             format(self.hipname, self.roomid), data=json.dumps
                             (payload), headers=self.HEADERS, params=params)
        return resp

def main():
    ZBXALERT = ZabbixAlert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5])
    if len(sys.argv) == 8:
        ZBXALERT.images(okimg=sys.argv[6], probimg=sys.argv[7])
    resp = ZBXALERT.sendmsg()
    return resp


if __name__ == '__main__':
    main()
