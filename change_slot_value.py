import logging

frequency_everyday_dic = {'no': 0,
                          'every day': 1}

frequency_time_perday_dic = {'no': 0,
                             'once a day': 1,
                             'twice a day': 2,
                             'thrice a day': 3}

reminder_method_dic = {'alexa reminder': 0,
                       'remind': 0,
                       'reminder': 0,
                       'phone call': 1}


def key_word_in_slot(string, dic):
    for key_word in dic:
        if string in key_word:
            return (dic[string])


def change_slot_value(frequency_everyday, frequency_time_perday, reminder_method):
    print('hi hi')
    try:
        reminder_repeat_day = key_word_in_slot(frequency_everyday, frequency_everyday_dic)
        reminder_repeat_time = key_word_in_slot(frequency_time_perday, frequency_time_perday_dic)
        reminder_method = key_word_in_slot(reminder_method, reminder_method_dic)
        print('return----------------------------------------------')
        return reminder_repeat_day, reminder_repeat_time, reminder_method
    except:
        logging.info("slot value have some problem")
