from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np


periodic_table = {
    'T1': {
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 4,
        "New_deadline": 4,
        "Period": 4
    },
    'T2': {
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 6,
        "New_deadline": 6,
        "Period": 6
    },
    'Server' : {
        "Release_time" : 0,
        "Computation_time" : 3,
        "Deadline" : 5,
        "New_deadline" : 5,
        "Period" : 5,
        "Charge" : 0,
        "Original_Charge" : 2,
        "Aperiodic_tasks"  : [

        ]
    }
}

periodic_table2 = {
    'T1': {
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 5,
        "New_deadline": 5,
        "Period": 5
    },
    'T2': {
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 7,
        "New_deadline": 7,
        "Period": 7
    },
    'Server' : {
        "Release_time" : 0,
        "Computation_time" : 1,
        "Deadline" : 7,
        "New_deadline" : 7,
        "Period" : 7,
        "Charge" : 0,
        "Original_Charge" : 1,
        "Aperiodic_tasks"  : [

        ]
    }
}

Aperiodic_Tasks = [{
                "Arival" : 2,
                "Computation_time" : 2,
                "Computed" : 0
            },{
                "Arival" : 8,
                "Computation_time" : 1,
                "Computed" : 0
            },{
                "Arival" : 12,
                "Computation_time" : 2,
                "Computed" : 0
            },{
                "Arival" : 19,
                "Computation_time" : 1,
                "Computed" : 0
            }]


def dbf(t: float, table: dict) -> float:
    answer = 0
    for task in table:
        T = table[task]["Period"]
        D = table[task]["Deadline"]
        answer += np.floor((t + T - D)/T) * table[task]["Computation_time"]
    # print(t, answer)
    return answer


def check_schedulable(table: dict) -> bool:
    n = len(table.keys()) - 1
    Up = 0
    for inp in table.keys() :
        if inp != "Server" : 
            Up += table[inp]["Computation_time"] / table[inp]["Period"]

    Us = table["Server"]["Computation_time"] / table["Server"]["Period"]
    return (Up <= n * ((2/(Us + 1)) ** (1/n) - 1 ))


def schedule_EDF(table: dict):
    done_list = []
    time = 0
    time_epoch = 1
    max_schedule_time = np.lcm.reduce(
        list(map(lambda x: table[x]["Deadline"], table)))
    for task in table.keys():
        table[task]["Schedule"] = []
        table[task]["Computed"] = 0
        if task == "Server" :
            for sub_task in table[task]["Aperiodic_tasks"] :
                sub_task["Computed"] = 0

    while time < max_schedule_time:
        appendable_tasks = []
        min_deadline = 100000000000000000000000000
        to_be_done = None
        for task in Aperiodic_Tasks :
            if task["Arival"] <= time :
                table["Server"]["Aperiodic_tasks"].append(task)
                Aperiodic_Tasks.remove(task)
        if len(table["Server"]["Aperiodic_tasks"]) == 0 :
            table["Server"]["Charge"] = 0
        for task in table.keys():
            if time % table[task]["Deadline"] == 0 :
                if task == "Server" and len(table["Server"]["Aperiodic_tasks"]) > 0:
                    table[task]["Charge"] = table[task]["Original_Charge"]
                if task in done_list :
                    done_list.remove(task)
                    table[task]["Computed"] = 0
                    table[task]["New_deadline"] += table[task]["Deadline"]

            if task in done_list or \
               time < table[task]["Release_time"] or \
                (task == "Server" and 
                                (len(table[task]["Aperiodic_tasks"]) == 0  or  
                                    table[task]["Charge"] == 0)):
                continue
            else:
                if table[task]["Period"] < min_deadline:
                    to_be_done = task
                    min_deadline = table[task]["Period"]
                appendable_tasks.append(task)

        if to_be_done == None:
            time += time_epoch
            continue
        if to_be_done != "Server" :
            computing_time = min(
                time_epoch, table[to_be_done]["Computation_time"]-table[to_be_done]["Computed"])

            table[to_be_done]["Computed"] += computing_time
            if table[to_be_done]["Computed"] >= table[to_be_done]["Computation_time"]:
                done_list.append(to_be_done)
            table[to_be_done]["Schedule"].append([time, time+computing_time])
        else :
            # pprint(table["Server"])
            computing_time = min(
                time_epoch, table["Server"]["Aperiodic_tasks"][0]["Computation_time"]
                                                    -table["Server"]["Aperiodic_tasks"][0]["Computed"])
            table[task]["Charge"] -= computing_time
            table["Server"]["Aperiodic_tasks"][0]["Computed"] += computing_time
            if table["Server"]["Aperiodic_tasks"][0]["Computed"] >= table["Server"]["Aperiodic_tasks"][0]["Computation_time"]:
                table["Server"]["Aperiodic_tasks"].pop(0)
            table["Server"]["Schedule"].append([time, time+computing_time])
        time += computing_time
    pprint(table)
    return table


def draw_chart(tasks):
    colors = np.random.rand(len(tasks), 3)
    all_schedules = [task['Schedule'] for task in tasks.values()]

    max_end = max([max(sched[-1][-1] for sched in all_schedules)])

    fig, ax = plt.subplots(1, figsize=(8, 4))
    for i, task in enumerate(tasks):

        schedules = tasks[task]['Schedule']
        for start, end in schedules:
            ax.broken_barh([(start, end-start)],
                           (i-0.4, 0.8), facecolors=colors[i])

        ax.text(-0.1, i, task, ha='right', va='center')

    ax.set_xlim(0, max_end)
    ax.set_xticks(np.arange(0, max_end + 1, 1))
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    ax.set_yticklabels([])
    ax.set_title('Gantt Chart')

    plt.show()


def schedule(table: dict):
    if not check_schedulable(table):
        print("Tasks not schedulable !!!!!")
        exit(1)
    table = schedule_EDF(table=table)
    draw_chart(table)


if __name__ == "__main__":
    table = periodic_table2
    schedule(table)
