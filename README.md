# alexa-medicine-notifier-application-lambda
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "medicine notifier application",
            "intents": [
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": [
                        "fuck off"
                    ]
                },
                {
                    "name": "AMAZON.HelpIntent",
                    "samples": [
                        "please help me",
                        "help me"
                    ]
                },
                {
                    "name": "AMAZON.StopIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.NavigateHomeIntent",
                    "samples": []
                },
                {
                    "name": "Medicine_Notifier_Intent",
                    "slots": [
                        {
                            "name": "time",
                            "type": "AMAZON.TIME"
                        },
                        {
                            "name": "date",
                            "type": "AMAZON.DATE",
                            "samples": [
                                "{date}"
                            ]
                        },
                        {
                            "name": "repeat_day",
                            "type": "repeat_day",
                            "samples": [
                                "{repeat_day}"
                            ]
                        },
                        {
                            "name": "repeat_time",
                            "type": "repeat_time",
                            "samples": [
                                "{repeat_time}"
                            ]
                        },
                        {
                            "name": "notify_method",
                            "type": "notify_method",
                            "samples": [
                                "{notify_method}"
                            ]
                        }
                    ],
                    "samples": [
                        "notify me eat medicine at {time} {date}"
                    ]
                }
            ],
            "types": [
                {
                    "name": "repeat_day",
                    "values": [
                        {
                            "name": {
                                "value": "every day"
                            }
                        },
                        {
                            "name": {
                                "value": "no"
                            }
                        }
                    ]
                },
                {
                    "name": "repeat_time",
                    "values": [
                        {
                            "name": {
                                "value": "thrice a day"
                            }
                        },
                        {
                            "name": {
                                "value": "twice a day"
                            }
                        },
                        {
                            "name": {
                                "value": "once a day"
                            }
                        },
                        {
                            "name": {
                                "value": "no"
                            }
                        }
                    ]
                },
                {
                    "name": "notify_method",
                    "values": [
                        {
                            "name": {
                                "value": "phone call"
                            }
                        },
                        {
                            "name": {
                                "value": "remidner"
                            }
                        },
                        {
                            "name": {
                                "value": "alexa reminder"
                            }
                        }
                    ]
                }
            ]
        },
        "dialog": {
            "intents": [
                {
                    "name": "Medicine_Notifier_Intent",
                    "confirmationRequired": false,
                    "prompts": {},
                    "slots": [
                        {
                            "name": "time",
                            "type": "AMAZON.TIME",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.126171916837.1036692089107"
                            }
                        },
                        {
                            "name": "date",
                            "type": "AMAZON.DATE",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.126171916837.1545111519270"
                            }
                        },
                        {
                            "name": "repeat_day",
                            "type": "repeat_day",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.126171916837.1522888857677"
                            }
                        },
                        {
                            "name": "repeat_time",
                            "type": "repeat_time",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.171195881837.1188978649079"
                            }
                        },
                        {
                            "name": "notify_method",
                            "type": "notify_method",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.10117583864.660009768598"
                            }
                        }
                    ]
                }
            ],
            "delegationStrategy": "ALWAYS"
        },
        "prompts": [
            {
                "id": "Elicit.Slot.1355977295201.1562547913077",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "please tell me the time you want to wake up"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.1197284259548.1405918606682",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "do you want to repeat the alarm   if yes please say  yes every monday  else please say no"
                    }
                ]
            },
            {
                "id": "Confirm.Slot.1197284259548.1405918606682",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "I heard {repeat} , is that correct?"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.126171916837.1036692089107",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "please tell me the time you want to notify"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.126171916837.1545111519270",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "please tell me the date you want to notify"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.126171916837.1522888857677",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "do you want to repeat the alarm   if want please say every day or no"
                    }
                ]
            },
            {
                "id": "Confirm.Slot.126171916837.1522888857677",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "I heard {repeat_day} , is that correct?"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.382177143787.1229693384892",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "please tell me the date you want me to reminde you"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.283084357716.629794268854",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "what kind of method you want me notify you, alexa reminder or phone call"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.171195881837.1188978649079",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "do you want to repeat in the same day   if yes please say once a day or twice a day or thrice  a day or no"
                    }
                ]
            },
            {
                "id": "Elicit.Slot.10117583864.660009768598",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "what kind of method you want me notify you, alexa reminder or phone call"
                    }
                ]
            }
        ]
    }
}
