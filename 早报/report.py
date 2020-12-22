from login import Longin, TimeTable
from datetime import datetime


class report:
    # 初始化 需要先定义的可以先写到这里
    def __init__(self):
        # 定义一个字典用作和isoweekday()获取到的星期几做匹配
        self.week_dict = {1: '星期一', 2: '星期二', 3: '星期三', 4: '星期四', 5: '星期五', 6: '星期六', 7: '星期天'}

    def jwxt(self):
        zspt = Longin("1708010127", "193728abC")
        response_cookies = zspt.Longin_Home()
        table = TimeTable(response_cookies)
        class_schedule = table.get_class_schedule()
        # print(class_schedule)
        dayOfWeek = datetime.now().isoweekday()
        # print(dayOfWeek)
        print('今天是:', self.week_dict[dayOfWeek])
        print('今天的课程是:', class_schedule[self.week_dict[dayOfWeek]])
        for i in class_schedule[self.week_dict[dayOfWeek]].keys():
            print(i, (6 - len(i)) * ' ', ':  ', class_schedule[self.week_dict[dayOfWeek]][i])


if __name__ == '__main__':
    report().jwxt()
