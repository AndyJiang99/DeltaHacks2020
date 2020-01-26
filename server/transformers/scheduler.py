import functools


class Scheduler:
    WEIGHTS = [4.25, 3.5, -2, -1.5, 1]

    def get_heuristic_value(self, task, max_diff, max_dur):
        return (Scheduler.WEIGHTS[0] + Scheduler.WEIGHTS[1] * task['deadline'] +
                Scheduler.WEIGHTS[2] * task['difficulty'] / max_diff +
                Scheduler.WEIGHTS[3] * task['est_duration'] / max_dur +
                Scheduler.WEIGHTS[4] * task['deadline'] * task['difficulty'] / max_diff)

    def create_optimized_ordering(self, schedule_events):
        schedule_events = sorted(schedule_events,
                                 key=functools.cmp_to_key(lambda task_a, task_b:
                                                          task_a['deadline'] - task_b['deadline']))
        for i in range(len(schedule_events)):
            schedule_events[i]['deadline'] = i + 1
        max_diff = max([task['difficulty'] for task in schedule_events]) or 1
        max_dur = max([task['est_duration'] for task in schedule_events]) or 1

        def comparer(task_a, task_b):
            return self.get_heuristic_value(task_a, max_diff, max_dur) - self.get_heuristic_value(task_b, max_diff, max_dur)
        return sorted(schedule_events, key=functools.cmp_to_key(comparer))