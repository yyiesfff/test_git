### 扣掉午休時間 1 hr,行政部認定一天上限是8 hrs


from datetime import datetime, timedelta
WeeklyTime = timedelta()
DayTime = timedelta(hours = 9)
WeekTime = timedelta(hours = 27)

file_path = "Time.txt"
with open(file_path, "r", encoding="utf-8") as file:
    data = file.read()

lines = data.splitlines()
results = {}
current_date = None

def InOfficeTime(entries):
    total_time = timedelta()
    for i in range(1, len(entries)):
        start = datetime.strptime(entries[i - 1], "%H:%M:%S")
        end = datetime.strptime(entries[i], "%H:%M:%S")
        #print(type(start))
        total_time += end - start
    # print("total_time", total_time)
    return total_time

attendance_times = []
for i, line in enumerate(lines):
    # print("i:", i)
    # print("line:", line)
    if line in "Check Date:":
        if current_date and attendance_times:
            total_time = InOfficeTime(attendance_times)
            if total_time >= DayTime:
                total_time = DayTime
            results[current_date] = total_time
        current_date = lines[i + 1].strip()  # 取得下一行作為日期
        attendance_times = []
    elif "In Office" in line:
        time_part = line.split("\t")[0]
        # print("time_part", time_part)
        attendance_times.append(time_part)

# 最後一組資料
if current_date and attendance_times:
    total_time = InOfficeTime(attendance_times)
    if total_time >= DayTime:
        total_time = DayTime
    results[current_date] = total_time

# print(results)

# output
for date, time in results.items():
    #print("time: ", time)
    WeeklyTime += time
    if time < DayTime:
        NeedTime = DayTime - time
        EnoughTime = 'need on line time'
    else:
        NeedTime = ''
        EnoughTime = 'enough 9hr'
    print(f"{date}#### in office time: {time}, {EnoughTime} {NeedTime}")


total_seconds = int(WeeklyTime.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60


formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

if WeeklyTime < WeekTime:
    print(f"Weekly Time: {formatted_time}, still need {WeekTime - WeeklyTime}")
else:
    print(f"Weekly Time: {formatted_time}, enough 27hr")