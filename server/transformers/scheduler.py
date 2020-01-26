from datetime import datetime, timedelta


class Scheduler:
    WEIGHTS = [4.25, 3.5, -2, -1.5, 1]

    def get_heuristic_value(self, task, max_diff, max_dur):
        return (Scheduler.WEIGHTS[0] + Scheduler.WEIGHTS[1] * task['deadline'] +
                Scheduler.WEIGHTS[2] * task['difficulty'] / max_diff +
                Scheduler.WEIGHTS[3] * task['est_duration'] / max_dur +
                Scheduler.WEIGHTS[4] * task['deadline'] * task['difficulty'] / max_diff)
    
    def apply_sentiment_transformation(self, events, sentiment_value):
        if not sentiment_value:
            return events
        new_order = []
        if sentiment_value < -0.25:
            hi_diff = list(filter(lambda task: task['difficulty'] > 5, events))
            low_diff = list(filter(lambda task: task['difficulty'] <= 5, events))
            overlap = min(len(low_diff), len(hi_diff))
            if len(low_diff) > len(hi_diff):
                new_order += low_diff[:len(low_diff) - overlap]
                for task_a, task_b in zip(low_diff[len(low_diff) - overlap:], hi_diff):
                    new_order += [task_b, task_a]
            elif len(hi_diff) > len(low_diff):
                for i in range(overlap):
                    new_order += [low_diff[i], hi_diff[i]]
                new_order += hi_diff[overlap:]
            else:
                for i in range(overlap):
                    new_order += [low_diff[i], hi_diff[i]]
            return new_order
        elif -0.25 <= sentiment_value and sentiment_value <= 0.25:
            return events
        elif 0.25 < sentiment_value:
            hi_diff = list(filter(lambda task: task['difficulty'] > 5, events))
            low_diff = list(filter(lambda task: task['difficulty'] <= 5, events))
            overlap = min(len(low_diff), len(hi_diff))
            for i in range(overlap):
                new_order += [hi_diff[i], low_diff[i]]
            if len(low_diff) > len(hi_diff):
                new_order += low_diff[overlap:]
            elif len(hi_diff) > len(low_diff):
                new_order += hi_diff[overlap:]
            return new_order

    def create_optimized_ordering(self, schedule_events, sentiment_value):
        events = sorted(schedule_events, key=lambda task: task['deadline'])
        temp_deadlines = {}
        for i in range(len(events)):
            temp_deadlines[events[i]['id']] = events[i]['deadline']
            events[i]['deadline'] = i + 1
        max_diff = max([task['difficulty'] for task in events]) or 1
        max_dur = max([task['est_duration'] for task in events]) or 1
        events = sorted(events, key=lambda task: self.get_heuristic_value(task, max_diff, max_dur))
        events = self.apply_sentiment_transformation(events, sentiment_value)
        for event in events:
            event['deadline'] = temp_deadlines[event['id']]
        return events

    def determine_schedule(self, schedulable_events, fixed_events, cur_time):
        class LLNode:
            def __init__(self, begin_time, end_time):
                self.next_node = None
                self.prev_node = None
                self.begin_time = begin_time
                self.end_time = end_time

            def time_diff(self):
                return self.end_time - self.begin_time

        final_schedule = []
        unschedulable = []
        next_day_time = cur_time + timedelta(days=1)
        next_day_time = datetime(next_day_time.year, next_day_time.month, next_day_time.day)
        cur_node = LLNode(cur_time, next_day_time)
        fixed_events = reversed(sorted(fixed_events, key=lambda task: task['end_time']))
        for event in fixed_events:
            if cur_node is None:
                unschedulable.append(event.copy())
            if event['end_time'] == cur_node.end_time:
                cur_node.end_time = event['begin_time']
                final_schedule.append(event.copy())
                if event['start_time'] == cur_time:
                    cur_node = None
            elif event['end_time'] < cur_node.end_time:
                if event['start_time'] == cur_time:
                    cur_node.begin_time = event['end_time']
                else:
                    cur_node.prev_node = LLNode(cur_node.begin_time, event['start_time'])
                    cur_node.begin_time = event['end_time']
                    cur_node.prev_node.next_node = cur_node
                    cur_node = cur_node.prev_node
                final_schedule.append(event.copy())
            else:
                unschedulable.append(event.copy())
        event_iter = iter(schedulable_events)
        pending_event = None
        while (True):
            event = pending_event if pending_event else next(event_iter, None)
            if event is None:
                break
            if cur_node is None:
                unschedulable.append(event)
                pending_event = None
                continue
            if event['est_duration'] < cur_node.time_diff():
                event['start_time'] = cur_node.begin_time
                event['end_time'] = cur_node.begin_time + event['est_duration']
                cur_node.begin_time += event['est_duration']
                final_schedule.append(event.copy())
                pending_event = None
            elif event['est_duration'] == cur_node.time_diff():
                event['start_time'] = cur_node.begin_time
                event['end_time'] = cur_node.end_time
                cur_node = cur_node.next_node
                final_schedule.append(event.copy())
                pending_event = None
            elif event['est_duration'] > cur_node.time_diff():
                pending_event = event.copy()
                pending_event['est_duration'] -= cur_node.time_diff()
                event['start_time'] = cur_node.begin_time
                event['end_time'] = cur_node.end_time
                cur_node = cur_node.next_node
                final_schedule.append(event.copy())
        return final_schedule, unschedulable
