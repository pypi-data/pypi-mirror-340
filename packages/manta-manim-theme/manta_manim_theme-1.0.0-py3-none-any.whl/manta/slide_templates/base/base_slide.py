import manim as m

import os
import inspect
from pathlib import Path

from manta.padding_style.paddingABC import PaddingABC
from manta.banner import banner
from manta.logger import log


class BaseSlide(PaddingABC,
                # manim_slides.Slide,
                m.Scene
                ):
    print_banner_on_setup: bool = True

    scene_width: float = 14.22222222222222
    content_width: float


    def setup(self):
        super().setup()

        if self.print_banner_on_setup:
            print(banner)

        # init content width
        self.content_width = self.scene_width - 2 * self.med_large_buff

    def is_in_scene(self, mobj: m.Mobject) -> bool:
        if mobj is None:
            return False
        return mobj in self.mobjects

    def fade_out_scene(self):
        # don't use self.play(*[m.FadeOut(obj) for obj in self.mobjects])
        # because play method is overridden in subclasses
        # it causes troubles with slide index-objects (see IndexedSlide)
        m.Scene.play(self, *[m.FadeOut(obj) for obj in self.mobjects])

    def remove_everything(self):
        m.Scene.remove(self, *self.mobjects)

    def get_max_z_index(self) -> int:
        if not self.mobjects:
            return 0
        return max(mobj.z_index for mobj in self.mobjects)

    @classmethod
    def get_file_path(cls) -> Path:
        return Path(inspect.getfile(cls)).resolve()

    @classmethod
    def render_video_low(cls):
        flags = "-pql"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")

    @classmethod
    def render_video_medium(cls):
        flags = "-pqm"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")

    @classmethod
    def render_video_high(cls):
        flags = "-pqh"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")

    @classmethod
    def render_video_4k(cls):
        flags = "-pqk"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")

    @classmethod
    def save_sections(cls):
        file_path = cls.get_file_path()
        terminal_cmd = f"manim --save_sections -qk {file_path}"

        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")

    @classmethod
    def save_sections_without_cache(cls):
        file_path = cls.get_file_path()
        terminal_cmd = f"manim --disable_caching --save_sections -qk {file_path}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")


    @classmethod
    def show_last_frame(cls):
        file_path = cls.get_file_path()
        terminal_cmd = f"manim -pqm -s {file_path}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        os.system(f"{terminal_cmd}")

    @classmethod
    def rendering_test(cls):
        flags = "-ql"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        import subprocess

        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e



    @classmethod
    def manim_slides_html_medium(cls):
        flags = f"-qm"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim-slides render {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        import subprocess

        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e


        # run manim slides
        terminal_cmd = f"manim-slides convert {scene} slides.html --open"
        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e

    @classmethod
    def manim_slides_html_4k(cls):
        flags = f"-qk"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim-slides render {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        import subprocess

        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e

        # run manim slides
        terminal_cmd = f"manim-slides convert {scene} slides.html --open"
        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e

    @classmethod
    def manim_slides_4k(cls):
        flags = f"-qk"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim-slides render {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        import subprocess

        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e

    @classmethod
    def manim_slides_m(cls):
        flags = f"-qm"
        scene = cls.__name__
        file_path = cls.get_file_path()

        terminal_cmd = f"manim-slides render {file_path} {scene} {flags}"
        log.info(f"running command: \n\n\t{terminal_cmd}\n")
        import subprocess

        try:
            result = subprocess.run(terminal_cmd, shell=True, check=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(e.stderr.decode())
            raise e
