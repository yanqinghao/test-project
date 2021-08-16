# coding=utf-8
import copy
import json
import random
from datetime import datetime, timedelta

case_num = 10000000


def choose(l, n=1):
    l = list(l)
    if n == 1:
        return [random.choice(l)]
    else:
        value = random.choice(l)
        m = n - 1
        l.remove(value)
        return [value] + choose(l, n=m)


def gen_fake_routes(events, routes, num):
    res = []
    while len(res) < num:
        keys = copy.deepcopy(events)
        if random.random() > 0.3:
            steps = choose(range(1, 10))[0]
            keys.remove("收到订单")
            values = ["收到订单"] + choose(keys, steps)
        else:
            steps = choose(range(1, 10))[0]
            keys.remove("发送报价")
            keys.remove("收到订单")
            values = ["发送报价", "收到订单"] + choose(keys, steps)
        if values not in res and values not in routes:
            res.append(values)
    return res


with open("private/events.json", "r") as f:
    log_config = json.load(f)

routes = log_config["routes"]
events = log_config["events"]
routes_weight = log_config["routes_weight"]

fake_routes = gen_fake_routes(events, routes, 480)

org = ["北京", "上海", "广州", "深圳"]
org_weight = [0.8, 0.08, 0.07, 0.05]

customer = ["张三", "李四", "王五", "赵六", "冯七", "沈八", "孙九", "周十", "吴十一", "郑十二"]
cus_weight = [0.2, 0.1, 0.03, 0.07, 0.08, 0.02, 0.2, 0.1, 0.05, 0.15]

net_value = [[100, 3000], [3000, 10000]]
net_value_weight = [0.7, 0.3]

time_start = datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
time_random_days = [0, 365]
time_random_seconds = [0, 24 * 60 * 60]

step_duration = [[1800, 1 * 24 * 60 * 60], [1 * 24 * 60 * 60, 7 * 24 * 60 * 60],
                 [7 * 24 * 60 * 60, 30 * 24 * 60 * 60]]
step_duration_weight = [0.55, 0.35, 0.1]

with open("log.csv", "w") as f:
    f.writelines(["id,caseid,time,activity,customer,net_value,org\n"])
    count = 0
    for case_id in range(case_num):
        customer_selected = random.choices(customer, weights=cus_weight, k=1)[0]
        org_selected = random.choices(org, weights=org_weight, k=1)[0]
        time_step = time_start + timedelta(days=random.randint(*time_random_days),
                                           seconds=random.randint(*time_random_seconds))
        net_value_selected = random.randint(
            *random.choices(net_value, weights=net_value_weight, k=1)[0])
        route = random.choices(routes, weights=routes_weight,
                               k=1)[0] if random.random() <= 0.8 else random.choice(fake_routes)
        logs = []
        for e in route:
            step_seconds = random.randint(
                *random.choices(step_duration, weights=step_duration_weight, k=1)[0])
            log = f"{count},{case_id},{str(time_step)},{e},{customer_selected},{net_value_selected},{org_selected}\n"
            logs.append(log)
            time_step += timedelta(seconds=step_seconds)
            count += 1
        f.writelines(logs)
