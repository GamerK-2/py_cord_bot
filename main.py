from typing import Optional

import discord
import os
import io
import asyncio
import time as t
import enum
from webcolors import CSS3_NAMES_TO_HEX

import py_d2.D2Shape
# import py-d2
from py_d2.D2Connection import D2Connection
from py_d2.D2Diagram import D2Diagram
from py_d2.D2Shape import D2Shape
from py_d2.D2Style import D2Style

# D2 setup
from py_d2.D2Shape import Shape

shape_str = [member.value for member in Shape]

# General Settings
bot = discord.Bot()
token = open("token", "r").readline()
shapes = []
connections = []
child_list = []
css_color_names = list(CSS3_NAMES_TO_HEX.keys())


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.command()
async def add_shape(ctx, name: discord.Option(str),
                    shape: discord.Option(choices=shape_str),
                    fill_color: str = "white",
                    stroke_color: str = "blue",
                    stroke_width: int = None,
                    container: str = None,
                    stroke_dash: int = None,
                    three_d: bool = False,
                    multiple: bool = None,
                    border_radius: int = None,
                    opacity: float = None,
                    shadow: bool = False,
                    double_border: bool = None,
                    font_size: int = None,
                    font_color: str = None,
                    bold: bool = None,
                    italic: bool = None,
                    underline: bool = None
                    ):
    global child_list, shapes
    if border_radius is None or 0 <= border_radius <= 20:
        if fill_color in css_color_names or stroke_color in css_color_names or font_color in css_color_names:
            if opacity is None or 0 <= opacity <= 1:
                if stroke_width is None or 1 <= stroke_width <= 15:
                    if stroke_dash is None or 0 <= stroke_dash <= 10:
                        if font_size is None or 8 <= font_size <= 100:
                            if ":" in name:
                                await ctx.respond("You should name shape without ':'")
                            else:
                                if shape == "rectangle" or "square":
                                    if container is not None:
                                        str_shape = list(map(str, shapes))
                                        matching = [s for s in str_shape if container in s]
                                        child_list = list(map(D2Shape, matching))
                                        for text in str_shape:
                                            if container in text:
                                                str_shape.remove(text)
                                                shapes.clear()
                                                shapes = list(map(D2Shape, str_shape))
                                                shapes.append(D2Shape(name=name, shape=Shape[f'{shape}'],
                                                                      style=D2Style(fill=fill_color,
                                                                                    stroke=stroke_color,
                                                                                    stroke_width=stroke_width,
                                                                                    stroke_dash=stroke_dash,
                                                                                    three_d=three_d, multiple=multiple,
                                                                                    border_radius=border_radius,
                                                                                    opacity=opacity, shadow=shadow,
                                                                                    double_border=double_border,
                                                                                    font_size=font_size,
                                                                                    font_color=font_color,
                                                                                    underline=underline, italic=italic,
                                                                                    bold=bold), shapes=child_list))
                                                await ctx.respond(f"A new shape called {name} has added")
                                                break
                                            else:
                                                await ctx.respond(
                                                    f"{container} is not exist\nTry again with other shape or make new one")
                                                break
                                    elif container is None:
                                        shapes.append(D2Shape(name=name, shape=Shape[f'{shape}'],
                                                              style=D2Style(fill=fill_color, stroke=stroke_color,
                                                                            stroke_width=stroke_width,
                                                                            stroke_dash=stroke_dash, three_d=three_d,
                                                                            multiple=multiple,
                                                                            border_radius=border_radius,
                                                                            opacity=opacity, shadow=shadow,
                                                                            double_border=double_border,
                                                                            font_size=font_size, font_color=font_color,
                                                                            underline=underline, italic=italic,
                                                                            bold=bold)))
                                        await ctx.respond(f"A new shape called {name} has added")
                                else:
                                    if three_d:
                                        await ctx.respond("You can make 3D style with only rectangle and square")
                                    else:
                                        if container is not None:
                                            str_shape = list(map(str, shapes))
                                            matching = [s for s in str_shape if container in s]
                                            child_list = list(map(D2Shape, matching))
                                            shapes.append(D2Shape(name=name, shape=Shape[f'{shape}'],
                                                                  style=D2Style(fill=fill_color, stroke=stroke_color,
                                                                                stroke_width=stroke_width,
                                                                                stroke_dash=stroke_dash, three_d=False,
                                                                                multiple=multiple,
                                                                                border_radius=border_radius,
                                                                                opacity=opacity, shadow=shadow,
                                                                                double_border=double_border,
                                                                                font_size=font_size,
                                                                                font_color=font_color,
                                                                                underline=underline, italic=italic,
                                                                                bold=bold),
                                                                  shapes=child_list))
                                            await ctx.respond(f"A new shape called {name} has added ")
                                        else:
                                            shapes.append(D2Shape(name=name, shape=Shape[f'{shape}'],
                                                                  style=D2Style(fill=fill_color, stroke=stroke_color,
                                                                                stroke_width=stroke_width,
                                                                                stroke_dash=stroke_dash, three_d=False,
                                                                                multiple=multiple,
                                                                                border_radius=border_radius,
                                                                                opacity=opacity, shadow=shadow,
                                                                                double_border=double_border,
                                                                                font_size=font_size,
                                                                                font_color=font_color,
                                                                                underline=underline, italic=italic,
                                                                                bold=bold)))

                                            await ctx.respond(f"A new shape called {name} has added")
                        else:
                            ctx.respond("Font Size value must be in between 8 and 100")
                    else:
                        ctx.respond("Stroke Dash value must be in between 0 and 10")
                else:
                    ctx.respond("Stroke Width value must be in between 1 and 15 ")
            else:
                ctx.respond("The Opacity value must be in between 0 and 10")
        else:
            await ctx.respond("Color you chose is not exist in css")
    else:
        await ctx.respond("Radius value must be in between 0 and 20")


@bot.command()
async def remove_shape(ctx, name: discord.Option(str)):
    global shapes
    removing_shape = name
    str_shape = list(map(str, shapes))
    for text in str_shape:
        if removing_shape in text:
            str_shape.remove(text)
            shapes.clear()
            shapes = list(map(D2Shape, str_shape))
            await ctx.respond(f"A shape called {name} has deleted")
        else:
            await ctx.respond(f"There is no Shape on D2 Code")


@bot.command()
async def add_connection(ctx, shape_from: discord.Option(str), shape_to: discord.Option(str),
                         direction: discord.Option(choices=["To", "From", "Both", "None"]),
                         label: Optional[str] = None, stroke_color: str = None):
    global connections
    from py_d2.D2Connection import Direction
    if stroke_color in css_color_names or stroke_color is None:
        if label is None or ":" not in label:
            if direction == "To":
                shape_direction = Direction.TO
                await ctx.respond(f"Connected {shape_from} to {shape_to}")
            elif direction == "From":
                shape_direction = Direction.FROM
                await ctx.respond(f"Connected {shape_from} from {shape_to}")
            elif direction == "Both":
                shape_direction = Direction.BOTH
                await ctx.respond(f"Connected both {shape_from} and {shape_to}")
            else:
                shape_direction = Direction.NONE
                await ctx.respond(f"Connected {shape_from} and {shape_to} with None direction")
            connections.append(
                D2Connection(shape_1=shape_from, shape_2=shape_to, direction=shape_direction, label=label,
                             stroke_color=stroke_color))
        elif ":" in label:
            await ctx.respond("You should name connection without ':'")
    else:
        await ctx.respond("Color you chose is not exist in css")


@bot.command()
async def make_image(ctx, file_name: discord.Option(str), sketch_mode: bool = None):
    global shapes
    diagram = D2Diagram(shapes=shapes, connections=connections)
    await ctx.respond("Writing graph to file...")
    t.sleep(3)
    await ctx.respond("Writing Complete\nYou can use '/send_graph <file name>' for sending image")
    if sketch_mode is None or sketch_mode is False:
        with open(f"{file_name}.d2", "w") as f1:
            f1.write(str(diagram))
            print(f"Done! ({file_name}.d2)\n")
        os.popen(f"d2 {file_name}.d2 {file_name}.png")
        shapes.clear()
        connections.clear()
    else:
        with open(f"{file_name}.d2", "w") as f2:
            f2.write(str(diagram))
            print(f"Done! ({file_name}.d2)\n")
        os.popen(f"d2 --sketch=true {file_name}.d2 {file_name}.png")
        shapes.clear()
        connections.clear()


@bot.command()
async def send_graph(ctx, file_name: discord.Option(str)):
    with open(f"D:/Users/user/Desktop/py_cord_bot/{file_name}.png", "rb") as f:
        image_data = f.read()
        file = discord.File(io.BytesIO(image_data), filename=f"{file_name}.png")
        await ctx.respond(file=file)


bot.run(token)  # run the bot with the token
