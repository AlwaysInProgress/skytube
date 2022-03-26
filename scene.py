from aifeynman import run_aifeynman
from manim import *
from matplotlib import image
import numpy as np
from skytubesim import *
import math

sim = SkyTubeSim()

config.window_size = (300, 130)
config.background_color = "#87CEEB"

def make_arrow(base_element: Mobject, magnitude: float, max_value: float, label: str, offset=[0,0,0]):
    arrow_length = np.interp(abs(magnitude), [0, max_value], [.3, 2]) * (-1 if magnitude < 0 else 1)
    start_point = base_element.get_center() + offset
    end_point = base_element.get_center() + offset + [0, arrow_length, 0]
    vel_arrow = Arrow(start_point, end_point, max_stroke_width_to_length_ratio=1, buff=0)
    txt_offset = DOWN if magnitude < 0 else UP
    vel_txt = Text(label).next_to(vel_arrow.get_tip(), txt_offset, buff=0)
    return Group(vel_arrow, vel_txt)

class AnimateExample(Scene):
    def construct(self):
        circle = Circle(radius=.1).set_fill(RED, opacity=1.0 )

        self.add(circle)

        sim.run()

        fallman = ImageMobject("./assets/img/fallman")
        fallman.scale(0.5)
        free_body_group = Group(fallman).move_to(LEFT * 3)

        self.add(free_body_group)

        # map [-4, 4] to [50, 0]
        def convert_world_height_to_screen_height(y: float) -> float:
            return 8./50.*y - 4.

        oHeight = convert_world_height_to_screen_height(sim.height[0])
        circle.move_to(RIGHT + [0, oHeight, 0])

        for i in range(sim.currentIndex):
            yPos = convert_world_height_to_screen_height(sim.height[i])

            vel_arrow_group = make_arrow(fallman, sim.velocity[i], np.max(np.abs(sim.velocity)), "V", offset=[0, -.7, 0])
            pd_arrow_group = make_arrow(fallman, sim.pressureDrag[i], max(sim.pressureDrag), "P", offset=[.7, 0, 0])
            by_arrow_group = make_arrow(fallman, sim.buoyancyForce[i], max(sim.buoyancyForce), "B", offset=[-.7, 0, 0])
            acc_arrow_group = make_arrow(fallman, sim.acceleration[i], max(sim.acceleration), "A")
            free_body_group.add(vel_arrow_group, acc_arrow_group, pd_arrow_group, by_arrow_group)

            self.play(
                circle.animate.move_to(RIGHT + [0, yPos, 0]), run_time=0.025
            )

            free_body_group.remove(acc_arrow_group, vel_arrow_group, pd_arrow_group, by_arrow_group)



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