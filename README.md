# zbx-hipchat
This alert script creates cards in hipchat that are expandable to reveal useful links to the alert.  
This uses the new HipChat v2 API. [HipChat API Info](https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens#APIaccesstokens-Usergeneratedtokens)

####Add a new media type to Zabbix

![Alt text](/imgs/zbx-media type.png?raw=true "Media Type")

Define the parameters like so.

1. {ALERT.SENDTO}
2. {ALERT.MESSAGE}
3. You subdomain name for the HipChat URL
4. HipChat v2 API Key
5. Image to use for recovery/OK Messages(Optional)
6. Image to use for Problem Messages(Optional)

**_The images are optional but you must provide both if you are using them._**

####Add a new user for each HipChat room in Zabbix

For each room you want to send to create a user and add a contact type of HipCard to it.

![Alt text](/imgs/media-send-to.png?raw=true "Send To Address")

Set the Send to field to the HipChat Room ID you want to use for this user contact.

####Create a new action in Zabbix

![Alt text](/imgs/zbx-action.png?raw=true "Action Messsage")

The Subject doesn't matter its not used to alert HipChat.  
Format the Default and Recovery Messages like so.

>name: "{TRIGGER.NAME}"  
>id: "{TRIGGER.ID}"  
>status: "{TRIGGER.STATUS}"  
>hostname: "{HOSTNAME}"  
>event_id: "{EVENT.ID}"  
>severity: "{TRIGGER.SEVERITY}"  
>url: "{TRIGGER.URL}"  
>description: "{TRIGGER.DESCRIPTION}"  


The alerts look like the following in HipChat.

![Alt text](/imgs/alert-sml.png?raw=true "Alert Example")

You can click the down arrow on the card  to expand the alert to reveal more information and links.

![Alt text](/imgs/alert-lrg.png?raw=true "Expanded Alert Example")

* Clicking the name of the Alert will take you to the Event's view in Zabbix filtered to the trigger for the last 7 days.
* Clicking More Information will take you to the Description page of the trigger in Zabbix
* Clicking Events will take you to the Event's view in Zabbix filtered to the trigger for the last 7 days.
* Clicking Acknowledge will take you the acknowledgement comment screen for the trigger.
* Clicking Trigger Link takes you to whatever URL you set within the trigger itself.

Addtional information listed on the card is
* Status - This status of the trigger which is also duplicated in the title of the card.
* Severity - The severity of the trigger.
* Hostname - The hostname or IP of the host the trigger belongs to.

#### Message Colors
The colors of the message vary depending on severity level.

* Green Messages
  * Recovery Messages
* Grey Messages
  * Not Classified
  * Information
* Yellow Messages
  * Warning
  * Average
* Red Messages
  * High
  * Disaster
