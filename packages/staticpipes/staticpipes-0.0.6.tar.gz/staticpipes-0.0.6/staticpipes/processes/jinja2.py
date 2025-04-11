import jinja2

from staticpipes.process_base import BaseProcessor


class ProcessJinja2(BaseProcessor):
    """
    Renders Jinja2.

    The current contents of the file are put in the "content" variable in the context.

    Pass:

    - template - the path to the template in the source directory to render.

    """

    def __init__(self, template):
        self._template = template

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):
        """"""

        # TODO cache this
        jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.source_directory.dir),
            autoescape=jinja2.select_autoescape(),
        )

        template = jinja2_env.get_template(self._template)
        process_current_info.context["content"] = process_current_info.contents
        contents = template.render(process_current_info.context)
        process_current_info.contents = contents
