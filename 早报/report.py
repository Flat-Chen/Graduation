from login import Longin, TimeTable


class report():
    def __init__(self):
        pass

    def jwxt(self):
        zspt = Longin("1708010127", "193728abC")
        response_cookies = zspt.Longin_Home()
        table = TimeTable(response_cookies)
        class_schedule = table.get_class_schedule()
        print(class_schedule)


if __name__ == '__main__':
    report().jwxt()
