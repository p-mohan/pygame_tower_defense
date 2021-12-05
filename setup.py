from cx_Freeze import setup, Executable
import pygame
executables = [Executable("run.py")]

setup(
    name="Pygame Tower Defense",
    options={"build_exe":{"packages":["pygame"],"include_files":['game_assets/']}},
    executables = executables
)