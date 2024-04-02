import json
import logging

import logging

try:
    import indigo
except ImportError:
    pass

LOG_FORMAT = '%(asctime)s.%(msecs)03d\t%(levelname)-10s\t%(name)s.%(funcName)-28s %(msg)s'


class Plugin(indigo.PluginBase):
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.plugin_file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))
        self.indigo_log_handler.setLevel(10)

    def run_concurrent_thread(self):  # noqa
        try:
            while True:
                self.sleep(1)
        except self.StopThread:
            pass

    def incoming_webhook(self, action, dev=None, caller_waiting_for_result=None):
        try:
            # Get the entire JSON payload.
            payload = json.loads(action.props['body_params']['payload'])
            self.fire_trigger(payload)
            return True
        except Exception as err:
            indigo.server.log(f"Exception: {err}", isError=True)
            return False

    def fire_trigger(self, payload: dict) -> bool:
        """
        Fire any triggers tied to the media event

        Users can create as many triggers as they want that are linked to the media event. All triggers that match the
        media event will fire.

        * Note that two media events are not tied to any triggers: `media.rate` and `media.scrobble`. There are other
        events that are not covered that relate to Plex Server administration. Two events may be worth considering in
        the future: `admin.database.backup` and `admin.database.corrupted` where users might want to rely on Indigo for
        notifications.
        ---
        :param dict payload:
        :return bool:
        """
        event      = payload['event']  # pause, play, resume, stop
        media_type = payload['Metadata']['type']  # movie, show, track,
        is_local   = payload['Player']['local']
        player     = payload['Player']['title']
        self.logger.debug(f"Trigger event [{event}] received from player [{player}].")

        try:
            # Iterate through all triggers.
            for trigger in indigo.triggers.iter("self"):
                if trigger.enabled:
                    # If we match event and media type.
                    if trigger.pluginProps['event'] == event and media_type in trigger.pluginProps['mediaTypes']:
                        # Fire trigger if player is local or trigger prop "Local Events Only" is False.
                        local_player = trigger.pluginProps['localPlayer']
                        if (local_player and is_local) or not local_player:
                            indigo.trigger.execute(trigger.id)
            return True
        except Exception as err:
            indigo.server.log(f"Exception: {err}", isError=True)
            return False
