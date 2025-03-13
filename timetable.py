import datetime
from datetime import datetime, timedelta

def oeWeek(startWeek, endWeek, mode):
    allWeek = range(startWeek, endWeek + 1)
    oddWeek = []; evenWeek = []
    for w in allWeek:
        if w % 2 == 0: evenWeek.append(w)
        else: oddWeek.append(w)
    if mode: return oddWeek
    else: return evenWeek


def rgWeek(startWeek, endWeek): return list(range(startWeek, endWeek + 1))


def timetable(maxWeek, classTime, starterDay, classes, oneClassTime=45):
    maxWeek += 1

    weeks = [None]
    for i in range(1, maxWeek):
        singleWeek = [None]
        for d in range(0, 7):
            singleWeek.append(starterDay)
            starterDay = starterDay + timedelta(days = 1)
        weeks.append(singleWeek)

    iCalHeader = 'BEGIN:VCALENDAR\n' \
        + 'METHOD:PUBLISH\n' \
        + 'VERSION:2.0\n' \
        + 'X-WR-CALNAME:课表\n' \
        + 'PRODID:-//Apple Inc.//Mac OS X 10.15.6//EN\n' \
        + 'X-WR-TIMEZONE:Asia/Shanghai\n' \
        + 'CALSCALE:GREGORIAN\n' \
        + 'BEGIN:VTIMEZONE\n' \
        + 'TZID:Asia/Shanghai\n' \
        + 'END:VTIMEZONE\n'

    createNow = datetime.now() - timedelta(hours = 8)
    
    allvEvent = ""
    for Class in classes:
        [Name, Teacher, Location, classWeek, classWeekday, classOrder] = Class[:]
        Title = Name + "@" + Location
        for timeWeek in classWeek:
            classDate = weeks[timeWeek][classWeekday]
            startTime = classTime[classOrder[0]]; endTime = classTime[classOrder[-1]]
            classStartTime = classDate + timedelta(minutes = startTime[0] * 60 + startTime[1])
            classEndTime = classDate + timedelta(minutes = endTime[0] * 60 + endTime[1] + oneClassTime)
            Description = " 任课教师: " + Teacher + "。"
            vEvent = "\nBEGIN:VEVENT"
            vEvent += "\nDTEND;TZID=Asia/Shanghai:" + classEndTime.strftime('%Y%m%dT%H%M%S')
            vEvent += "\nSUMMARY:" + Title
            vEvent += "\nDTSTART;TZID=Asia/Shanghai:" + classStartTime.strftime('%Y%m%dT%H%M%S')
            vEvent += "\nDESCRIPTION:" + Description
            vEvent += "\nEND:VEVENT"
            allvEvent += vEvent
    allvEvent += "\nEND:VCALENDAR"
    return iCalHeader + allvEvent


def main():
    maxWeek = 100  # 可以设置更大的周数
    # 根据课表的时间设置
    classTime = [None, 
        (8, 0),   # Period 1
        (8, 50),  # Period 2
        (9, 40),  # Period 3
        (10, 30), # Period 4
        (11, 20), # Period 5
        (12, 10), # Period 6
        (13, 0),  # Period 7
        (13, 50), # Period 8
        (14, 40), # Period 9
        (15, 30)  # Period 10
    ]
    
    starterDay = datetime(2025, 3, 10)  # 设置为本学期第一周的星期一
    
    classes = [
        # Monday
        ['Chinese', 'Zoey Zhai', 'Boxue 514', rgWeek(1, 20), 1, [3]],
        ['Mathematics', 'Lexie Kong', 'Boxue 514', rgWeek(1, 20), 1, [7, 8]],
        ['English', 'Wang Yihan', 'Boxue 514', rgWeek(1, 20), 1, [9, 10]],
        
        # Tuesday
        ['Mathematics', 'Lexie Kong', 'Boxue 514', rgWeek(1, 20), 2, [1, 2]],
        ['Economics', 'Jonas Zhang', 'Boxue 514', rgWeek(1, 20), 2, [3, 4]],
        ['Music', 'Ye Teng', 'Boxue 708', rgWeek(1, 20), 2, [5]],
        ['Chinese', 'Zoey Zhai', 'Boxue 514', rgWeek(1, 20), 2, [7]],
        ['P.E.', 'Lucas Jin', 'Playground 2', rgWeek(1, 20), 2, [9]],
        
        # Wednesday
        ['English', 'Wang Yihan', 'Boxue 514', rgWeek(1, 20), 3, [1, 2]],
        ['Accounting', 'Cynthia Zhang', 'Boxue 511', rgWeek(1, 20), 3, [3]],
        ['Class Meeting', 'Wang Yihan', 'Boxue 514', rgWeek(1, 20), 3, [7]],
        ['Mathematics', 'Lexie Kong', 'Boxue 514', rgWeek(1, 20), 3, [8]],
        
        # Thursday
        ['Economics', 'Jonas Zhang', 'Boxue 514', rgWeek(1, 20), 4, [3]],
        ['English', 'Shawna Saari', 'Boxue 514', rgWeek(1, 20), 4, [4, 5]],
        ['Accounting', 'Cynthia Zhang', 'Boxue 511', rgWeek(1, 20), 4, [9, 10]],
        
        # Friday
        ['Economics', 'Jonas Zhang', 'Boxue 514', rgWeek(1, 20), 5, [1, 2]],
        ['P.E.', 'Lucas Jin', 'Playground 2', rgWeek(1, 20), 5, [3]],
        ['Mathematics', 'Lexie Kong', 'Boxue 514', rgWeek(1, 20), 5, [4, 5]],
        ['Accounting', 'Cynthia Zhang', 'Boxue 511', rgWeek(1, 20), 5, [8, 9]]
    ]
    
    filename = 'timetable.ics'
    with open(filename, 'w') as f:
        f.write(timetable(maxWeek, classTime, starterDay, classes))


if __name__ == '__main__':
    main()
