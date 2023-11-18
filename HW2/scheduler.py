from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

example_tree = {
    'A': {
        "Fathers": [],
        "Children": ["C"],
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 25,
    },
    'B': {
        "Fathers": [],
        "Children": ["C", "D"],
        "Release_time": 0,
        "Computation_time": 3,
        "Deadline": 25,
    },
    'C': {
        "Fathers": ["A", "B"],
        "Children": ["E", "F"],
        "Release_time": 0,
        "Computation_time": 3,
        "Deadline": 25,
    },
    'D': {
        "Fathers": ["B"],
        "Children": ["F", "G"],
        "Release_time": 0,
        "Computation_time": 5,
        "Deadline": 25,
    },
    'E': {
        "Fathers": ["C"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 25,
    },
    'F': {
        "Fathers": ["C", "D"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 25,
    },
    'G': {
        "Fathers": ["D"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 5,
        "Deadline": 25,
    }
}

example_tree2 = {
    't1': {
        "Fathers": [],
        "Children": ["t2","t3","t4","t5","t6"],
        "Release_time": 0,
        "Computation_time": 3,
        "Deadline": 20,
    },
    't2': {
        "Fathers": ["t1"],
        "Children": ["t8", "t9"],
        "Release_time": 0,
        "Computation_time": 18,
        "Deadline": 50,
    },
    't3': {
        "Fathers": ["t1"],
        "Children": ["t7"],
        "Release_time": 0,
        "Computation_time": 12,
        "Deadline": 50,
    },
    't4': {
        "Fathers": ["t1"],
        "Children": ["t8"],
        "Release_time": 0,
        "Computation_time": 9,
        "Deadline": 50,
    },
    't5': {
        "Fathers": ["t1"],
        "Children": ["t9"],
        "Release_time": 0,
        "Computation_time": 11,
        "Deadline": 50,
    },
    't6': {
        "Fathers": ["t1"],
        "Children": ["t8"],
        "Release_time": 0,
        "Computation_time": 12,
        "Deadline": 50,
    },
    't7': {
        "Fathers": ["t3"],
        "Children": ["t10"],
        "Release_time": 0,
        "Computation_time": 19,
        "Deadline": 70,
    },
    't8': {
        "Fathers": ["t2","t4","t6"],
        "Children": ["t10"],
        "Release_time": 0,
        "Computation_time": 3,
        "Deadline": 70,
    },
    't9': {
        "Fathers": ["t2","t5"],
        "Children": ["t10"],
        "Release_time": 0,
        "Computation_time": 8,
        "Deadline": 70,
    },
    't10': {
        "Fathers": ["t7","t8","t9"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 110,
    }
}

example_tree3 = {
    'A': {
        "Fathers": [],
        "Children": ["C"],
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 25,
    },
    'B': {
        "Fathers": [],
        "Children": ["C", "D"],
        "Release_time": 0,
        "Computation_time": 3,
        "Deadline": 25,
    },
    'C': {
        "Fathers": ["A", "B"],
        "Children": ["E", "F"],
        "Release_time": 0,
        "Computation_time": 3,
        "Deadline": 25,
    },
    'D': {
        "Fathers": ["B"],
        "Children": ["F", "G"],
        "Release_time": 0,
        "Computation_time": 5,
        "Deadline": 25,
    },
    'E': {
        "Fathers": ["C"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 1,
        "Deadline": 25,
    },
    'F': {
        "Fathers": ["C", "D"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 2,
        "Deadline": 25,
    },
    'G': {
        "Fathers": ["D"],
        "Children": [],
        "Release_time": 0,
        "Computation_time": 5,
        "Deadline": 25,
    }
}


def modify_deadlines(tree: dict):
    stack = list({k: v for k, v in tree.items() if not v['Children']}.keys())
    visited_list = []
    while len(stack) > 0:
        node = stack.pop(0)
        new_deadline = tree[node]["Deadline"]
        for child_node in tree[node]["Children"]:
            new_deadline = min(new_deadline, tree[child_node]["Deadline"]
                               - tree[child_node]["Computation_time"])
        tree[node]["Deadline"] = new_deadline
        visited_list.append(node)
        for father in tree[node]["Fathers"]:
            add = True
            for child in tree[father]["Children"]:
                if child not in visited_list:
                    add = False
                    break
            if add:
                stack.append(father)


def modify_release_times(tree: dict):
    stack = list({k: v for k, v in tree.items() if not v['Fathers']}.keys())
    visited_list = []
    while len(stack) > 0:
        node = stack.pop(0)
        new_release_time = tree[node]["Release_time"]
        for father_node in tree[node]["Fathers"]:
            new_release_time = max(new_release_time, tree[father_node]["Release_time"]
                                   + tree[father_node]["Computation_time"])
        tree[node]["Release_time"] = new_release_time
        visited_list.append(node)
        for child in tree[node]["Children"]:
            add = True
            for father in tree[child]["Fathers"]:
                if father not in visited_list:
                    add = False
                    break
            if add:
                stack.append(child)


def turn_to_EDF(tree: dict) -> dict:
    modify_release_times(tree)
    modify_deadlines(tree)


# TODO: When tree turned to EDF, schedule the EDF
def schedule_EDF(table: dict):
    done_list = []
    time = 0
    time_epoch = 1
    max_schedule_time = max(list(map(lambda x:table[x]["Deadline"],table)))
    for task in table.keys():
        table[task]["Schedule"] = []
        table[task]["Computed"] = 0

    while time < max_schedule_time:
        appendable_tasks = []
        min_deadline = 100000000000000000000000000
        to_be_done = None
        for task in table.keys():
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
        table[to_be_done]["Schedule"].append([time,time+computing_time])

        time += computing_time

    return table

def draw_chart(tasks):
    colors = np.random.rand(len(tasks), 3)
    all_schedules = [task['Schedule'] for task in tasks.values()]

    max_end = max([max(sched[-1][-1] for sched in all_schedules)])


    fig, ax = plt.subplots(1, figsize=(8,4))
    for i, task in enumerate(tasks):
        
        schedules = tasks[task]['Schedule']
        for start, end in schedules:
            ax.broken_barh([(start, end-start)], (i-0.4,0.8), facecolors=colors[i])
            
        ax.text(-0.1, i, task, ha='right', va='center')

    ax.set_xlim(0, max_end)
    ax.set_xticks(np.arange(0, max_end + 1, 1))
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    ax.set_yticklabels([])
    ax.set_title('Gantt Chart')

    plt.show()

    

def schedule_tree(tree: dict):
    turn_to_EDF(tree=tree)
    table = schedule_EDF(table=tree)
    draw_chart(table)

if __name__ == "__main__":
    tree = example_tree
    schedule_tree(tree)