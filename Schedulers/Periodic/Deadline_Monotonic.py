from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np


example_table = {
    'T1': {
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 3,
        "New_deadline": 3,
        "Period": 4
    },
    'T2': {
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 4,
        "New_deadline": 4,
        "Period": 5
    },
    'T3': {
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 5,
        "New_deadline": 5,
        "Period": 6
    },
    'T4': {
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 10,
        "New_deadline": 10,
        "Period": 11
    },
}


def check_schedulable(table: dict) -> bool:
    sorted_list = sorted(table, key=lambda x: table[x]["Deadline"])
    for task_indx in range(len(sorted_list)):
        I = 0
        for k in range(task_indx):
            I += table[sorted_list[k]]["Computation_time"]
        # print("first I --->", I)
        while True:
            R = I + table[sorted_list[task_indx]]["Computation_time"]
            if R > table[sorted_list[task_indx]]["Deadline"]:
                return False
            I = 0
            for k in range(task_indx):
                I += np.ceil(R/table[sorted_list[k]]["Period"]
                             ) * table[sorted_list[k]]["Computation_time"]
            if I + table[sorted_list[task_indx]]["Computation_time"] \
                    <= R:
                # print(R)
                break
    return True


def schedule_DM(table: dict):
    done_list = []
    time = 0
    time_epoch = 1
    max_schedule_time = np.lcm.reduce(
        list(map(lambda x: table[x]["Deadline"], table)))
    for task in table.keys():
        table[task]["Schedule"] = []
        table[task]["Computed"] = 0

    while time < max_schedule_time:
        appendable_tasks = []
        min_deadline = 100000000000000000000000000
        to_be_done = None
        for task in table.keys():
            if time % table[task]["Deadline"] == 0 and task in done_list:
                done_list.remove(task)
                table[task]["Computed"] = 0
                table[task]["New_deadline"] += table[task]["Deadline"]

            if task in done_list or \
               time < table[task]["Release_time"]:
                continue
            else:
                if table[task]["Deadline"] < min_deadline:
                    to_be_done = task
                    min_deadline = table[task]["Deadline"]
                appendable_tasks.append(task)

        if to_be_done == None:
            time += time_epoch
            continue
        computing_time = min(
            time_epoch, table[to_be_done]["Computation_time"]-table[to_be_done]["Computed"])

        table[to_be_done]["Computed"] += computing_time
        if table[to_be_done]["Computed"] >= table[to_be_done]["Computation_time"]:
            done_list.append(to_be_done)
        table[to_be_done]["Schedule"].append([time, time+computing_time])

        time += computing_time

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
    table = schedule_DM(table=table)
    draw_chart(table)


if __name__ == "__main__":
    table = example_table
    schedule(table)
