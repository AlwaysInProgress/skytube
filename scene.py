from aifeynman import run_aifeynman
from manim import *
import numpy as np
from skytubesim import *
import math

sim = SkyTubeSim()

config.window_size = (300, 130)
config.background_color = "#87CEEB"

class AnimateExample(Scene):
    def construct(self):
        circle = Circle(radius=.1).set_fill(RED, opacity=1.0 )

        self.add(circle)

        sim.run()

        image = ImageMobject("./assets/img/fallman")
        image.scale(0.5)
        arrow_up = Arrow(ORIGIN, [0, 2, 0], max_stroke_width_to_length_ratio=1, buff=0)

        free_body_group = Group(image, arrow_up).move_to(LEFT * 3)

        self.add(free_body_group)

        # map [-4, 4] to [50, 0]
        def convert_world_height_to_screen_height(y: float) -> float:
            return 8./50.*y - 4.

        oHeight = convert_world_height_to_screen_height(sim.height[0])
        circle.move_to(RIGHT + [0, oHeight, 0])

        for i in range(sim.currentIndex):
            yPos = convert_world_height_to_screen_height(sim.height[i])

            acc_arrow_scale = (sim.acceleration[i]/sim.acceleration[i - 1])
            gs = sim.acceleration[i]/9.81

            acc_txt = Text('a = ' + str(round(gs, 2)) + " Gs")
            acc_txt.next_to(arrow_up.get_tip(), UP)
            free_body_group.add(acc_txt)

            if not math.isnan(acc_arrow_scale) and not math.isinf(acc_arrow_scale):
                arrow_up.scale(acc_arrow_scale, scale_tips=True)
                yDel = abs(1 - acc_arrow_scale) * arrow_up.height * -0.5
                arrow_up.shift([0, yDel, 0])

            self.play(
                circle.animate.move_to(RIGHT + [0, yPos, 0]), run_time=0.025
            )
            free_body_group.remove(acc_txt)



class Graph(Scene):
 def construct(self):
        ax = Axes(
            x_range=[0, 40, 5],
            y_range=[-8, 32, 5],
            x_length=9,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 40, 5)},
            y_axis_config={"numbers_to_include": np.arange(-5, 34, 5)},
            tips=False,
        )
        labels = ax.get_axis_labels(
            # x_label=Tex("$\Delta Q$"), y_label=Tex("T[$^\circ C$]")
            x_label="Delta Q", y_label="circle"

        )

        x_vals = [0, 8, 38, 39]
        y_vals = [20, 0, 0, -5]
        graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals, line_color="#FFFFFF")

        self.add(ax, labels, graph)