from collections import namedtuple
from django.template.base import TextNode
from django.template.library import InclusionNode
from django.template.loader_tags import ExtendsNode, BlockNode
from django.utils.encoding import force_text
from itertools import chain
import unicodedata
import io

from otree.templatetags.otree import NEXT_BUTTON_TEMPLATE_PATH




class TemplateCheckNextButton(object):
    def __init__(self, root):
        self.root = root

    def get_next_button_nodes(self, root):
        nodes = []
        for node in root.nodelist:
            if isinstance(node, (ExtendsNode, BlockNode)):
                new_child_nodes = self.get_next_button_nodes(node)
                nodes.extend(new_child_nodes)
            elif isinstance(node, InclusionNode) and node.filename == NEXT_BUTTON_TEMPLATE_PATH:
                nodes.append(node)
        return nodes

    def check_next_button(self):
        next_button_nodes = self.get_next_button_nodes(self.root)
        return len(next_button_nodes) > 0


def check_next_button(root):
    check = TemplateCheckNextButton(root)
    return check.check_next_button()


def has_valid_encoding(file_name):
    try:
        # need to open the file with an explicit encoding='utf8'
        # otherwise Windows may use another encoding if.
        # io.open provides the encoding= arg and is Py2/Py3 compatible
        with io.open(file_name, 'r', encoding='utf8') as f:
            template_string = f.read()
        force_text(template_string)
    except UnicodeDecodeError:
        return False
    return True


Line = namedtuple('Line', ('source', 'lineno', 'start', 'end'))


def format_error_line(line):
    # We need to make sure here that the output does not contain any unicode
    # characters. Django's check framework cannot print errors that contain
    # unicode.
    source = line.source
    source = unicodedata.normalize('NFKD', source).encode('ascii', 'replace')
    return '{line.lineno:4d} | {source}'.format(line=line, source=source)


def split_source_lines(source):
    """
    Split source string into a list of ``Line`` objects. They contain
    contextual information like line number, start position, end position.
    """
    lines = source.splitlines(True)
    start = 0
    annotated_lines = []
    for i, line in enumerate(lines):
        # Windows line endings end with '\r\n'.
        if line.endswith('\r\n'):
            ending_length = 2
        # In case of '\n' or '\r' ending the line.
        else:
            ending_length = 1
        end = start + len(line)
        annotated_lines.append(Line(
            # Don't include line endings in snippet source.
            source=line[:-ending_length],
            lineno=i + 1,
            start=start,
            end=end))
        start = end
    return annotated_lines
