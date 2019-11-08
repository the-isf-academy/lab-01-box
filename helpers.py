# -*- coding: utf-8 -*-
# helpers.py
# by Jacob Wolf, Chris Proctor, Jenny Han, and Krate Ng
# Functions which support box and whisker plot drawing

# =============================================================================
# ☕️ More-Than-You-Need-To-Know Lounge ☕️
# =============================================================================
# Welcome to the More-Than-You-Need-To-Know Lounge, a chill place for code that
# you don't need to understand.

# Thanks for stopping by, we hope you find something that catches your eye.
# But don't worry if this stuff doesn't make sense yet -- as long as we know
# how to use code, we don't have to understand everything about it.

# Of course, if you really like this place, stay a while. You can ask a
# teacher about it if you're interested.
# =============================================================================

from turtle import tracer, delay, update, position, heading, penup, pendown, forward, backward, write, goto, setheading, setposition, right, left, hideturtle
import pandas as pd

TICK_SIZE = 4

plot_settings = {}

def clamp_point(x, domain):
    if x < domain[0]:
        return domain[0]
    if x > domain[1]:
        return domain[1]
    return x

def clamp_database(df, x_domain):
    """
    Takes the values in df and clamps them to the specified x_domain. For example, let's say x_domain = (0, 100).
    If 4424 was in the df, it would be rewritten as 100. If -2 was in the df, it would be rewritten as 0.
    input: dataframe, tuple
    output: dataframe
    """
    for i in range(len(df)):
        x_clamp = clamp_point(df.iloc[i][0], x_domain)
        df.iloc[i, 0] = x_clamp
    return df

def get_database_as_list(filepath, column, values_domain):
    """
    Takes the values from the specified column from the csv file specified in filepath.
    The values are clamped to the specified values_domain.
    Returns the values as a list.
    input: string, string, tuple
    output: list
    """
    df = pd.read_csv(filepath)
    df_one_col = df[[column]]
    df_one_col = df_one_col.dropna()
    df_one_col_clamp = clamp_database(df_one_col, values_domain)
    return list(df_one_col_clamp[column])

class no_delay:
    "A context manager which causes drawing code to run instantly"

    def __enter__(self):
        self.n = tracer()
        self.delay = delay()
        tracer(0, 0)

    def __exit__(self, exc_type, exc_value, traceback):
        update()
        tracer(self.n, self.delay)

class restore_state_when_finished:
    """
    A context manager which records the turtle's position and heading
    at the beginning and restores them at the end of the code block.
    For example:

        from turtle import forward, right
        from helpers import restore_state_when_finished

        for angle in range(0, 360, 15):
            with restore_state_when_finished():
                right(angle)
                forward(100)
    """

    def __enter__(self):
        self.position = position()
        self.heading = heading()

    def __exit__(self, *args):
        penup()
        setposition(self.position)
        setheading(self.heading)
        pendown()

def scale(x, old_domain, new_domain):
    """
    Takes a value from the old domain and returns what the value would be in the new domain
    input: an integer/float, a tuple that represents the start and end of the old domain, and a tuple that represents the start and end of the new domain
    output: an integer/float
    """
    old_ldiff = x - old_domain[0]
    total_old_diff = old_domain[1] - old_domain[0]
    old_percent_pos = old_ldiff/total_old_diff
    total_new_diff = new_domain[1] - new_domain[0]
    new_ldiff = old_percent_pos * total_new_diff
    new_x = new_ldiff + new_domain[0]
    return new_x

def draw_tick():
    """
    Draws a tick (the mark, not the bug) at the current position and heading of the turtle
    """
    pendown()
    forward(TICK_SIZE/2)
    backward(TICK_SIZE)
    forward(TICK_SIZE/2)
    penup()

def label_tick(num):
    """
    Writes the number slightly below the current position and heading of the turtle
    input: an integer/float
    """
    forward(TICK_SIZE*5)
    write("{}".format(num), move=False, align="center", font=("Arial", 8, "normal"))
    backward(TICK_SIZE*5)

def draw_axis():
    """
    Draws the x-axis using the turtle domain, data domain, increment (for the data domain), and label specified in the plot_settings dictionary.
    """
    with restore_state_when_finished():
        penup()
        goto(plot_settings['turtle_axis_domain'][0], -150)
        setheading(0)
        pendown()

        start = int(plot_settings['data_domain'][0])
        end = int(plot_settings['data_domain'][1])
        length = plot_settings['turtle_axis_domain'][1] - plot_settings['turtle_axis_domain'][0]
        increment = plot_settings['axis_increment']
        num_increments = (end-start)/increment
        scaled_increment = (length-0)/num_increments
        for i in range(start, end, increment):
            right(90)
            draw_tick()
            label_tick(i)
            left(90)
            pendown()
            forward(scaled_increment)
        right(90)
        draw_tick()
        label_tick(plot_settings['data_domain'][1])

        penup()
        goto(0, -200)
        write(plot_settings['turtle_axis_label'], move=False, align="center", font=("Arial", 10, "normal"))

def plot(data_list, axis_label, turtle_axis_domain = (-200,200), axis_increment = 10):
    """
    Using the parameters, generates and returns a dictionary that contains the settings for turtle_axis_label, turtle_axis_domain, data_domain, and axis_increment
    input: list, string, tuple, int/float
    output: dictionary with key string
    """
    with restore_state_when_finished():
        plot_settings['turtle_axis_label'] = axis_label
        plot_settings['turtle_axis_domain'] = turtle_axis_domain
        plot_settings['data_domain'] = (min(data_list), max(data_list))
        plot_settings['axis_increment'] = axis_increment
        draw_axis()
        hideturtle()
        return plot_settings
