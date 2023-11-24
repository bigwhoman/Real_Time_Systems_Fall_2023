from pprint import *
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

failed = []
example_table = {
    'A': {
        "Release_time": 4,
        "Computation_time": 2,
        "Relative_deadline": 7,
        "Deadline": 7
    },
    'B': {
        "Release_time": 1,
        "Computation_time": 1,
        "Relative_deadline": 5,
        "Deadline": 5
    },
    'C': {
        "Release_time": 1,
        "Computation_time": 2,
        "Relative_deadline": 6,
        "Deadline": 6
    },
    'D': {
        "Release_time": 0,
        "Computation_time": 2,
        "Relative_deadline": 4,
        "Deadline": 4
    }
}

example_table2 = {
    'J1': {
        "Release_time": 2,
        "Computation_time": 5,
        "Relative_deadline": 12,
        "Deadline": 12
    },
    'J2': {
        "Release_time": 3,
        "Computation_time": 4,
        "Relative_deadline": 8,
        "Deadline": 8
    },
    'J3': {
        "Release_time": 1,
        "Computation_time": 2,
        "Relative_deadline": 7,
        "Deadline": 7
    },
    'J4': {
        "Release_time": 4,
        "Computation_time": 3,
        "Relative_deadline": 10,
        "Deadline": 10
    },
    'J5': {
        "Release_time": 5,
        "Computation_time": 6,
        "Relative_deadline": 9,
        "Deadline": 9
    },
    'J6': {
        "Release_time": 6,
        "Computation_time": 1,
        "Relative_deadline": 6,
        "Deadline": 6
    }
}


def fix_absoulute_deadlines(table: dict):
    for key in table:
        table[key]["Deadline"] = table[key]["Relative_deadline"] + \
            table[key]["Release_time"]


def get_deep(root: str, table: dict, total_time: int, chain: list) -> bool:
    table[root]["Visited"] = True
    time = max(total_time+table[root]["Computation_time"],
               table[root]["Release_time"]+table[root]["Computation_time"])
    if time > table[root]["Deadline"]:
        # print(chain, time, table[root]["Deadline"])
        return False
    for child in table:
        if not table[child]["Visited"]:
            if time + table[child]["Computation_time"] > table[child]["Deadline"]:
                read_fail = chain.copy()
                read_fail.append(child)
                failed.append(read_fail)
                return False
    for child in table:
        if not table[child]["Visited"]:
            chain.append(child)
            if get_deep(root=child, table=table, total_time=time, chain=chain):
                table[root]["Child"] = child
                table[root]["Schedule"] = []
                table[root]["Schedule"].append(
                    [time-table[root]["Computation_time"], time])
                return True
            else:
                table[child]["Visited"] = False
                chain.pop()
    for child in table:
        if not table[child]["Visited"]:
            # print(chain, time, table[root]["Deadline"])
            return False
    table[root]["Schedule"] = []
    table[root]["Schedule"].append(
        [time-table[root]["Computation_time"], time])
    return True


def bratley_schedule(table: dict):
    for node in table:
        if get_deep(root=node, table=table, total_time=0, chain=[node]):
            return table
        else:
            table[node]["Visited"] = False


def draw_chart(tasks: dict):
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


def update_node_names(data):
    updated_data = []
    for path in data:
        updated_path = []
        for i, node in enumerate(path):
            updated_path.append(f"{node}_{i}")
        updated_data.append(updated_path)
    return updated_data


def append_previous(data):
    updated_data = []
    for path in data:
        updated_path = []
        prev_nodes = []
        for node in path:
            updated_node = node
            if prev_nodes:
                updated_node += "_" + "_".join(prev_nodes)
            prev_nodes.append(node)
            updated_path.append(updated_node)
        updated_data.append(updated_path)

    return updated_data


def print_failed(data: list):

    updated_data = append_previous(data)
    G = nx.Graph()

    G.add_node('root')
    pos = {'root': (-12, 3)}   # fix root position

    x = 0
    y_offset = 0
    for path in updated_data:
        current_node = "root"
        y_offset = -len(path)/2  

        for i, node in enumerate(path):
            name = node
            G.add_node(name)
            G.add_edge(current_node, name)
            y = -y_offset - i
            pos[name] = (x, y)  # layout left to right and descending
            current_node = name
        x -= 1

    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 12)) 
    nx.draw(G, pos, with_labels=True)
    plt.savefig("tree.png")
    plt.show()


if __name__ == "__main__":

    table = example_table2
    for key in table:
        table[key]["Visited"] = False
    fix_absoulute_deadlines(table=table)
    bratley_schedule(table=table)
    if 'Schedule' in table[list(table.keys())[0]]:
        draw_chart(table)
    else:
        pprint(failed)
        print_failed(failed)
    # pprint(table)
