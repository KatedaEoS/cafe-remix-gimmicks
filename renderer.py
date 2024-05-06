from jinja2 import Environment, FileSystemLoader
import pandas as pd
import numpy as np

STAGE_COUNT = 2400
GIMMICK_TYPE_COUNT = 38
CATEGORY_NUM = {
    "Drinks": 0,
    "Sweets": 1,
    "Small plates": 2,
    "Entrées": 3,
}
CATEGORY_STR = {
    0: "drinks",
    1: "sweets",
    2: "smallplates",
    3: "entrees",
}


def parse_int(input) -> int:
    res = 0
    if isinstance(input, str):
        if input[-1] == "+":
            try:
                res = round(float(input[:-1]))
            except:
                pass
    else:
        try:
            res = round(input)
        except:
            pass
    return res


class Stage:
    def __init__(self) -> None:
        self.reset()

    def __init__(self, input: list) -> None:
        self.reset()
        self.parse_from_list(input)

    def reset(self) -> None:
        self.index = None
        self.require_level = None
        self.category = None
        self.moves = None
        self.megaphones = None
        self.gimmick_amounts = np.ndarray((GIMMICK_TYPE_COUNT), dtype=int)

    def parse_from_list(self, input: list) -> None:
        if len(input) < 5:
            print(f"Error: input list too short")
            return
        self.index = parse_int(input[0])
        self.require_level = parse_int(input[1])
        self.category = CATEGORY_NUM.get(input[2], 0)
        self.moves = parse_int(input[3])
        self.megaphones = parse_int(input[4])

        for i in range(GIMMICK_TYPE_COUNT):
            if i + 5 < len(input):
                self.gimmick_amounts[i] = parse_int(input[i + 5])
            else:
                self.gimmick_amounts[i] = 0


class SolutionStage:
    def __init__(self) -> None:
        self.index = None
        self.category_str = None
        self.amount = None


class GimmickSolution:
    def __init__(self) -> None:
        self.gimmick_id = None
        self.solution = []


df = pd.read_excel("cafe-db.xlsx", sheet_name=3, skiprows=1)

if df.shape[0] != STAGE_COUNT:
    print(f"Error: Stage count not equal to {STAGE_COUNT}")
    raise

if df.shape[1] != GIMMICK_TYPE_COUNT + 5:
    print(f"Warning: Gimmick type count not equal to {GIMMICK_TYPE_COUNT}")

stage = []
for i in range(STAGE_COUNT):
    stage.append(Stage(df.loc[i].tolist()))

solutions_list = []

for gimmick in range(GIMMICK_TYPE_COUNT):
    gs = GimmickSolution()
    gs.gimmick_id = gimmick
    max_count = 0
    for idx in range(STAGE_COUNT):
        if stage[idx].gimmick_amounts[gimmick] > max_count:
            max_count = stage[idx].gimmick_amounts[gimmick]
            s = SolutionStage()
            s.index = stage[idx].index
            s.category_str = CATEGORY_STR.get(stage[idx].category, "drinks")
            s.amount = max_count
            gs.solution.append(s)
    gs.solution = gs.solution[::-1]
    solutions_list.append(gs)

env = Environment(loader=FileSystemLoader("."))
languages = ["zh-CN", "en-US"]

for lang in languages:
    template = env.get_template(f"template/{lang}.html")
    with open(f"gimmicks_{lang}.html", "w", encoding="utf-8") as f:
        f.write(template.render(solutions=solutions_list))
