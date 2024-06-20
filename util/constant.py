# This file mainly helps to define some constant, so that we can easily change them.

FLASK_SERVER = ("0.0.0.0",5000)


# configurations for the user.
INITIAL_DRAGON_EYE = 100
INITIAL_PHONEIX_FEATURE = 100
INITIAL_EXPERIENCE = 100

TASK_DISTRIBUTION = {
    "互动任务":0.20,
    "助人任务":0.20,
    "好汉任务":0.25,
    "豪杰任务":0.20,
    "英雄任务":0.15,
    "救世主任务":0.00
}

assert sum(TASK_DISTRIBUTION.values()) == 1.00, "The distribution of task type is rather not valid."