# -*- coding: utf-8 -*-

# This is a simple Reminder Alexa Skill, built using
# the decorators approach in skill builder.
import sys

sys.path.append("/opt/")

import logging

from datetime import datetime, timedelta
import dateutil.tz

from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.skill_builder import SkillBuilder, CustomSkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value, get_user_id, get_device_id
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.services import ServiceException
from ask_sdk_model.services.reminder_management import Trigger, TriggerType, AlertInfo, SpokenInfo, SpokenText, \
    PushNotification, PushNotificationStatus, ReminderRequest

from ask_sdk_model.ui import SimpleCard, AskForPermissionsConsentCard
from ask_sdk_model import Response

from DynamoDB.put_item import put_item
from change_slot_value import change_slot_value

logging.basicConfig(level=logging.DEBUG)  # ---------------------------delete when production---------------------------

sb = CustomSkillBuilder(api_client=DefaultApiClient())  # required to use remiders

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

REQUIRED_PERMISSIONS = ["alexa::alerts:reminders:skill:readwrite"]
TIME_ZONE_ID = 'Asia/Hong_Kong'
HK_TZ = dateutil.tz.gettz(TIME_ZONE_ID)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input: HandlerInput) -> Response:
    """Handler for Skill Launch."""
    speech_text = "Welcome to the Medicine Notifier Application, you can say notify me eat medicine at while time and date."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Welcome", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("Medicine_Notifier_Intent"))
def Medicine_Notifier_Intent_handler(handler_input: HandlerInput) -> Response:
    """Handler for Notify Me Intent."""
    logging.info("running Medicine_Notifier_Intent_handler()")
    rb = handler_input.response_builder
    request_envelope = handler_input.request_envelope
    permissions = request_envelope.context.system.user.permissions
    reminder_service = handler_input.service_client_factory.get_reminder_management_service()

    if not (permissions and permissions.consent_token):
        logging.info("user hasn't granted reminder permissions")
        return rb.speak("Please give permissions to set reminders using the alexa app.") \
            .set_card(AskForPermissionsConsentCard(permissions=REQUIRED_PERMISSIONS)) \
            .response

    now = datetime.now(tz=HK_TZ)
    userId = get_user_id(handler_input)
    deviceId = get_device_id(handler_input)

    if userId == None:
        logging.info("can't get the userId")
    elif deviceId == None:
        logging.info("can't get the deviceId")

    try:
        reminder_date = get_slot_value(handler_input, "date")
        reminder_time = get_slot_value(handler_input, "time")
        reminder_repeat = get_slot_value(handler_input, "repeat")
        reminder_method = get_slot_value(handler_input, "method")
    except:
        logging.info("can't get the slot value")

    reminder_repeat, reminder_method = change_slot_value(reminder_repeat, reminder_method)
    put_item(userId, now.strftime("%Y-%m-%d %H:%M:%S"), deviceId, reminder_date, reminder_time, reminder_repeat,
             reminder_method)

    five_mins_from_now = now + timedelta(seconds=+5)
    notification_time = five_mins_from_now.strftime("%Y-%m-%dT%H:%M:%S")

    trigger = Trigger(TriggerType.SCHEDULED_ABSOLUTE, notification_time, time_zone_id=TIME_ZONE_ID)
    text = SpokenText(locale='en-US',
                      ssml='<speak>You need to eat medicine now.</speak>',
                      text='You need to eat medicine now.')
    alert_info = AlertInfo(SpokenInfo([text]))
    push_notification = PushNotification(PushNotificationStatus.ENABLED)
    reminder_request = ReminderRequest(notification_time, trigger, alert_info, push_notification)

    try:
        reminder_responce = reminder_service.create_reminder(reminder_request)
    except ServiceException as e:
        # see: https://developer.amazon.com/docs/smapi/alexa-reminders-api-reference.html#error-messages
        logger.error(e)
        raise e

    return rb.speak("reminder created") \
        .set_card(SimpleCard("Notify Me", "reminder created")) \
        .set_should_end_session(True) \
        .response


@sb.request_handler(
    can_handle_func=lambda handler_input:
    is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input: HandlerInput) -> Response:
    """Single handler for Cancel and Stop Intent."""
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Remindify", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input: HandlerInput) -> Response:
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    speech = (
        "The remindify skill can't help you with that.  "
        "You can say hello!!")
    reprompt = "You can say notify me to create a reminder."
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input: HandlerInput) -> Response:
    """Handler for Session End."""
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input: HandlerInput, exception: Exception) -> Response:
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()

# mark error to database, mark reminder record, kind of medicine, function to process data(repeat), time up to time zone, time and info to Class
# handle userId(can't get), DynamoDB(can't put_item -> try again).

# tmr do for hong kong time, combine date time, change to 0-7
