import pandas as pd


class Scheduler:
    WEIGHTS = [4.25, 3.5, -2, -1.5, 1]

    def get_heuristic_order_column(self, event_df):
        order_column =\
            [col * weight for (col, weight) in zip(
                [event_df['deadline'], event_df['difficulty'],
                 event_df['est_duration'], (event_df['deadline'] * event_df['difficulty'])],
                Scheduler.WEIGHTS[1:])]
        return map(sum, order_column) + Scheduler.WEIGHTS[0]

    def create_optimized_ordering(self, schedule_events):
        event_df = pd.DataFrame(schedule_events)
        event_df.sort_values(by=['deadline'], inplace=True)
        event_df['deadline'] = list(range(len(event_df.index)))
        event_df['difficulty'] = event_df['difficulty'] / (event_df['difficulty'].max() or 1)
        event_df['est_duration'] = event_df['est_duration'] / (event_df['est_duration'].max() or 1)
        event_df['order_value'] = self.get_heuristic_order_column(event_df)
        event_df.sort_values(by=['order_value'])
        columns = schedule_events.columns
        schedule_events.index = schedule_events['id']
        return pd.DataFrame([schedule_events.loc[id] for id in event_df['id']],
                            columns=columns).to_dict('records')
