# -*- coding: utf-8 -*-

# This is a simple Reminder Alexa Skill, built using
# the decorators approach in skill builder.
import sys

sys.path.append("/opt/")

import logging

from datetime import datetime, timedelta, timezone
import dateutil.tz

from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.skill_builder import SkillBuilder, CustomSkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value, get_user_id, get_device_id
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.services import ServiceException
from ask_sdk_model.services.reminder_management import Trigger, TriggerType, AlertInfo, SpokenInfo, SpokenText, \
    PushNotification, PushNotificationStatus, ReminderRequest, RecurrenceFreq, RecurrenceDay, Recurrence

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
    # speech_text = "Welcome to the Medicine Notifier Application, you can say notify me eat medicine at while time and date."
    speech_text = "Welcome."

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

    userId = get_user_id(handler_input)
    deviceId = get_device_id(handler_input)

    if userId == None:
        logging.info("can't get the userId")
    elif deviceId == None:
        logging.info("can't get the deviceId")

    try:
        reminder_date = get_slot_value(handler_input, "date")
        reminder_time = get_slot_value(handler_input, "time")
        frequency_everyday = get_slot_value(handler_input, "repeat_day")
        frequency_time_perday = get_slot_value(handler_input, "repeat_time")
        reminder_method = get_slot_value(handler_input, "notify_method")
        print(reminder_date, reminder_time, frequency_everyday, frequency_time_perday, reminder_method)
        print(type(reminder_date))
        print(type(reminder_time))
        print(type(frequency_everyday))
        print(type(frequency_time_perday))
        print(type(reminder_method))
        print(reminder_method + '----------------------------------------------')
    except:
        logging.info("can't get the slot value")

    print('change datetime----------------------------------------------')
    reminder_datetime = reminder_date + ' ' + reminder_time
    reminder_datetime = datetime.strptime(reminder_datetime, '%Y-%m-%d %H:%M')
    reminder_datetime.replace(tzinfo=timezone.utc).astimezone(HK_TZ)

    print('change slot value----------------------------------------------')
    frequency_everyday, frequency_time_perday, reminder_method = change_slot_value(frequency_everyday,
                                                                                   frequency_time_perday,
                                                                                   reminder_method)
    if (frequency_everyday == 999) or (frequency_time_perday == 999) or (reminder_method == 999):
        speech_text = "Your answer has no relation to the question. Please try again."
        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Welcome", speech_text)).set_should_end_session(
            False).response

    create_time = datetime.now(tz=HK_TZ)
    create_time = str(datetime.timestamp(create_time)).split(".")[0]
    reminder_datetime_ts = str(datetime.timestamp(reminder_datetime)).split(".")[0]

    put_item(userId, create_time, deviceId, reminder_datetime_ts, frequency_everyday,
             frequency_time_perday, reminder_method)

    if reminder_method == 1:
        speech_text = "We will remind you with the phone. Goodbye"
        return handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Welcome", speech_text)).set_should_end_session(
            False).response

    # -----reminder
    notification_time = reminder_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    if frequency_everyday == 1:
        recurrence = Recurrence(freq=RecurrenceFreq.DAILY)
        trigger = Trigger(TriggerType.SCHEDULED_ABSOLUTE, notification_time, recurrence=recurrence,
                          time_zone_id=TIME_ZONE_ID)
    else:
        trigger = Trigger(TriggerType.SCHEDULED_ABSOLUTE, notification_time, time_zone_id=TIME_ZONE_ID)

    print('seted trigger----------------------------------------------')

    text = SpokenText(locale='en-US', ssml='<speak>Please take medicine now</speak>', text='Please take medicine now')
    alert_info = AlertInfo(SpokenInfo([text]))
    push_notification = PushNotification(PushNotificationStatus.ENABLED)
    reminder_request = ReminderRequest(notification_time, trigger, alert_info, push_notification)
    print('before create reminder----------------------------------------------')

    try:
        if frequency_time_perday == 2:
            # first
            notification_time = reminder_datetime.replace(minute=0, hour=8, second=0).strftime("%Y-%m-%dT%H:%M:%S")
            trigger = Trigger(TriggerType.SCHEDULED_ABSOLUTE, notification_time, time_zone_id=TIME_ZONE_ID)
            alert_info = AlertInfo(SpokenInfo([text]))
            push_notification = PushNotification(PushNotificationStatus.ENABLED)
            reminder_request = ReminderRequest(notification_time, trigger, alert_info, push_notification)
            print('First reminder request')
            print(reminder_request)
            reminder_responce = reminder_service.create_reminder(reminder_request)
            # second
            notification_time = reminder_datetime.replace(minute=0, hour=19, second=0).strftime("%Y-%m-%dT%H:%M:%S")
            trigger = Trigger(TriggerType.SCHEDULED_ABSOLUTE, notification_time, time_zone_id=TIME_ZONE_ID)
            alert_info = AlertInfo(SpokenInfo([text]))
            push_notification = PushNotification(PushNotificationStatus.ENABLED)
            reminder_request = ReminderRequest(notification_time, trigger, alert_info, push_notification)
            print('First reminder request')
            print(reminder_request)
            reminder_responce = reminder_service.create_reminder(reminder_request)
        else:
            print('fuck my life -----------------')
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

# mark error handler, kind of medicine
# make reminder function
