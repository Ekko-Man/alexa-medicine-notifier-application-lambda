import logging

reminder_repeat_day_dic = {'no': 0,
                           'every day': 1}

reminder_repeat_time_dic = {'no': 0,
                            'once a day': 1,
                            'twice a day': 2,
                            'thrice a day': 3}

reminder_method_dic = {'alexa reminder': 0,
                       'reminder': 0,
                       'phone call': 1}


def key_word_in_slot(string, dic):
    for key_word in dic:
        if string in key_word:
            return (dic[string])


def change_slot_value(repeat_day, repeat_time, method):
    print('hi hi')
    try:
        reminder_repeat_day = key_word_in_slot(repeat_day, reminder_repeat_day_dic)
        reminder_repeat_time = key_word_in_slot(repeat_time, reminder_repeat_time_dic)
        reminder_method = key_word_in_slot(method, reminder_method_dic)

        # reminder_repeat_day = reminder_repeat_day_dic[reminder_repeat_day]
        # reminder_repeat_time = reminder_repeat_time_dic[reminder_reminder_repeat_timerepeat]
        # reminder_method = reminder_method_dic[reminder_method]

        print('return----------------------------------------------')
        return reminder_repeat_day, reminder_repeat_time, reminder_method
    except:
        logging.info("slot value have some problem")
