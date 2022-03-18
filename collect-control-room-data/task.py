from collections import Counter
from datetime import datetime
import os
from time import sleep
from RPA.Robocorp.Process import Process
from RPA.Robocorp.Vault import Vault

BOTS = [
    {
        "NAME": "236",  # used as identification in the collected stats
        "LINE_ITEMS_DETAILS": True,  # related to work item payload information of interest if True
        "MINIMUM_RUN_TIME": 200,  # minimum process run time for a process to be "collected"
    },
    {
        "NAME": "22",  # used as identification in the collected stats
        "LINE_ITEMS_DETAILS": False,  # related to work item payload information of interest if True
        "MINIMUM_RUN_TIME": 0,  # minimum process run time for a process to be "collected"
    },
]


def flush_print(message: str):
    print(message, flush=True)


class ControlRoomCollector:
    def __init__(self, runs_to_collect: int = 1):
        self.stats = {}
        self.bot = None
        self.runs_to_collect = runs_to_collect
        self.process = Process()
        self.output_dir = os.getenv("ROBOT_ARTIFACTS", "output")
        self.check_line_items = False

    def set_bot(self, bot):
        self.bot = bot
        self.stats = {}
        secrets = Vault().get_secret(f"control_room_process_{self.bot['NAME']}")
        self.process.set_apikey(secrets["api_key"])
        self.process.set_workspace_id(secrets["workspace_id"])
        self.process.set_process_id(secrets["process_id"])
        self.check_line_items = (
            self.bot["LINE_ITEMS_DETAILS"]
            if "LINE_ITEMS_DETAILS" in self.bot.keys()
            else False
        )
        flush_print(f"Bot set: {self.bot['NAME']}")

    def collect_ok_runs_over_x_duration(self):
        if not self.bot:
            raise ValueError("Bot has not been set")
        collect = []
        runs = self.process.list_process_runs(limit=self.runs_to_collect)
        for run in runs:
            # Collect only runs which have state COMPL or PENDING
            if run["state"] in ["COMPL", "PENDING"]:
                # Collect only runs which have duration same or longer than MINIMUM_RUN_TIME
                if run["duration"] >= self.bot["MINIMUM_RUN_TIME"]:
                    collect.append(run)
                else:
                    flush_print(
                        f"Run {run['runNo']} duration {run['duration']} under limit"
                    )
            else:
                flush_print(run)
                flush_print(f"Run {run['runNo']} result is not OK")
        return collect

    def add_stats_for_date(self, date, stat):
        """Used for grouping stats by date"""
        if date not in self.stats.keys():
            self.stats[date] = [stat]
        else:
            self.stats[date].append(stat)

    def collect_data(self):
        if not self.bot:
            raise ValueError("Bot has not been set")
        runs = self.collect_ok_runs_over_x_duration()
        total_output = ""
        for run in runs:
            run_output = ""
            run_id = run["id"]
            run_no = run["runNo"]
            duration = 0  # run['duration']
            total_line_items = 0
            run_status = self.process.get_process_run_status(run_id)
            step_runs = run_status["robotRuns"]
            real_start = None
            real_end = None
            for step_run in step_runs:
                one_step_run = self.process.get_process_run_status(
                    run_id, step_run_id=step_run["id"]
                )
                step_run_start = datetime.strptime(
                    one_step_run["startTs"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                step_run_end = datetime.strptime(
                    one_step_run["endTs"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                if real_start == None or real_start > step_run_start:
                    real_start = step_run_start
                if real_end == None or real_end < step_run_end:
                    real_end = step_run_end
                duration += one_step_run["duration"]
                sleep(0.5)

            real_duration = real_end - real_start

            run_output += f"Run no {run_no}\n"
            items = self.process.list_process_run_work_items(run_id, include_data=True)
            run_output += f"\tnumber of step runs            : {len(step_runs)}\n"
            run_output += f"\tnumber work items              : {len(items)}\n"

            item_types = []
            if self.check_line_items:
                for item in items:
                    if item["payload"]:
                        line_items = item["payload"]["items"]
                        total_line_items += len(line_items)
                        if "item_type_code" in line_items[0].keys():
                            item_types.extend(
                                [item["item_type_code"] for item in line_items]
                            )

            if total_line_items > 0:
                run_output += (
                    f"\ttotal line items               : {total_line_items} \n"
                )
                run_output += f"\taverage line item run duration : {round(duration/total_line_items,1)}s\n"
            run_output += f"\taverage step run duration      : {round(duration/len(step_runs), 1)}s\n"
            run_output += f"\treal start                     : {real_start}\n"
            run_output += f"\treal end                       : {real_end}\n"
            run_output += (
                f"\treal duration                  : {real_duration.seconds}s\n"
            )
            run_output += f"\ttotal step run duration        : {duration}s\n"
            run_output += "\n"
            flush_print(run_output)
            total_output += run_output

            date = datetime.strptime(items[0]["createTs"], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.add_stats_for_date(
                date.strftime("%d/%b/%y"),
                {
                    "runNo": run_no,
                    "item_types": Counter(item_types),
                    "real_duration": real_duration.seconds,
                    "duration": duration,
                    "step_runs": len(step_runs),
                    "total_line_items": total_line_items,
                },
            )
        self.write_report("details", total_output)

    def write_report(self, report_type, content):
        output_filename = os.path.join(
            self.output_dir, f"bot_{self.bot['NAME']}_{report_type}_report.txt"
        )
        with open(output_filename, "w") as fout:
            fout.write(content)

    def print_collected_stats(self):
        if not self.bot:
            raise ValueError("Bot has not been set")
        output_string = ""
        for date in self.stats.keys():
            output_string += f"Day: {date}\n"
            total_duration = sum([s["duration"] for s in self.stats[date]])
            total_step_runs = sum([s["step_runs"] for s in self.stats[date]])
            if self.check_line_items:
                total_line_items = sum(
                    [s["total_line_items"] for s in self.stats[date]]
                )
                total_item_types = sum(
                    [s["item_types"] for s in self.stats[date]], Counter()
                )
            total_real_duration = sum([s["real_duration"] for s in self.stats[date]])
            output_string += (
                f"Duration (sum of step runs)              : {total_duration}s\n"
            )
            output_string += (
                f"Effective runtime duration               : {total_real_duration}s\n"
            )
            output_string += (
                f"Total step runs                          : {total_step_runs}\n"
            )
            if self.check_line_items:
                output_string += (
                    f"Total line items                         : {total_line_items}\n"
                )
                output_string += "Line types                               : \n"
                for key, val in total_item_types.items():
                    output_string += f"\t{key} = {val}\n"
            output_string += f"Average step run duration                : {round(total_duration/total_step_runs,1)}s\n"
            output_string += f"Average step run real time duration      : {round(total_real_duration/total_step_runs,1)}s\n"
            if self.check_line_items:
                output_string += f"Average line item duration               : {round(total_duration/total_line_items,1)}s\n"
                output_string += f"Average line item real time duration     : {round(total_real_duration/total_line_items,1)}s\n"

            output_string += "\n"
        self.write_report("summary", output_string)


def main():
    collector = ControlRoomCollector()
    for bot in BOTS:
        collector.set_bot(bot)
        collector.collect_data()
        collector.print_collected_stats()


if __name__ == "__main__":
    main()
