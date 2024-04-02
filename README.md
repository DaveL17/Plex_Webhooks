### Plex Webhooks Plugin

This is an extremely simple plugin that connects Plex Server [webhooks](https://support.plex.tv/articles/115002267687-webhooks/) to Indigo. It reacts to four events from 
the Plex webhook API:
  * `media.pause` - Plex client pauses playback.
  * `media.play` - Plex client initiates playback.
  * `media.resume` - Plex client resumes playback.
  * `media.stop` - Plex client stops playback.

> [!Note]What this plugin is not: a way to control Plex from Indigo.

#### Requirements
  * Active [Plex Pass Subscription](https://support.plex.tv/articles/categories/intro-to-plex/plex-pass-subscriptions/) - the Plex webhook feature is only available to Plex Pass subscribers.
  * Authenticated Communications Path - there needs to be a valid path for the webhook payload to reach Indigo. The 
    plugin doesn't provide a means to configure IP routes or ports, and authentication is beyond the scope of this 
    readme.
  * Valid Webhook URL - entered into the Plex webhooks configuration settings.
  * Indigo version 2022.1 or later.

#### Webhook URL
A properly configured webhook URL is critical to the function of the plugin. It can be different depending on your 
environment, but generally looks something like this:

`http://10.0.1.123:8176/message/com.fogbert.indigoplugin.plexWebhooks/incoming_webhook/?api-key=abc123def456&player=Parlor`

  * `http://10.0.1.123` - the IP of the Indigo server running the plugin. It can be local, localhost, 127.0.0.1, or an 
    active Indigo Reflector address. If local, use `http` and use `https` with the Indigo Reflector service
  * `8176` - the appropriate port for the Indigo server (not required with Reflector addresses).
  * `message` - tells the Indigo server that the incoming message is for a plugin.
  * `com.fogbert.indigoplugin.plexServer` - the plist ID of this plugin.
  * `incoming_webhook` - the plugin method that's called by the `message` API.
  * `api-key=abc123def456` - a valid API key. It can be a valid Reflector access key or a local secret key if your
    version of Indigo supports them.

That's all that should be required to configure the plugin. 

#### Triggers
To actually use the plugin, you need to create Indigo triggers to respond to the incoming webhook. There is nothing 
unusual about setting them up.

  * Create a new Indigo Trigger,
  * Select "Plex Webhooks Event",
  * Select "Media Event",
  * Event: Select the event you want to trigger automation: pause, play, resume or stop.
  * Local Events Only: If you want players outside your LAN to be able to trigger automation, deselect the Local Events checkbox. It's 
    assumed that most uses would only be desired when Plex is being used locally (you probably don't want your lights 
    to dim if you're watching a movie in a hotel, for example.)
  * Media Types: Use this field to identify the media types you want to use the Trigger for. For example, you might 
    want to dim the lights when watching a movie, but not when you're listening to music.

#### Automations
For example, you can dim the lights and set a thermostat when you play a movie, and bring the lights back up when you 
pause or stop.

#### Notes
* Not all Plex media selections generate webhook events. For example, "Movies & Shows on Plex" do not generate webhook 
calls. This is due to Plex and not due to the plugin.

[current as of Indigo 2023.2 and Plex Version 4.125.1]
