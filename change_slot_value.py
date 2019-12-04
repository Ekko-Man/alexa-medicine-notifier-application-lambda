import logging

reminder_repeat_dic = {'no': 0,
                       'yes every monday': 1,
                       'yes every week': 8}

reminder_method_dic = {'alexa reminder': 0,
                       'phone call': 1}


def change_slot_value(reminder_repeat, reminder_method):
    try:
        reminder_repeat = reminder_repeat_dic[reminder_repeat]
        reminder_method = reminder_method_dic[reminder_method]
        return reminder_repeat, reminder_method
    except:
        logging.info("slot value have some problem")
