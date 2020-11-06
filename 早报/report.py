from login import Longin, TimeTable

zspt = Longin("1708010127", "193728abC")
response_cookies = zspt.Longin_Home()
table = TimeTable(response_cookies)
