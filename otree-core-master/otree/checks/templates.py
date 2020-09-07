from collections import namedtuple
from django.template.base import TextNode
from django.template.loader_tags import ExtendsNode, BlockNode
from django.utils.encoding import force_text
from itertools import chain
import unicodedata
import io

from otree.templatetags.otree_tags import NextButtonNode


class TemplateCheckContent(object):
    def __init__(self, root):
        self.root = root

    def node_is_empty(self, node):
        if isinstance(node, TextNode):
            return node.s.isspace()
        return False

    def is_extending(self, root):
        return any(
            isinstance(node, ExtendsNode)
            for node in root.nodelist)

    def is_content_node(self, node):
        """
        Returns if the node is an unempty text node.
        """
        if isinstance(node, TextNode):
            return not self.node_is_empty(node)
        return False

    def get_toplevel_content_nodes(self, root):
        nodes = []
        for node in root.nodelist:
            if isinstance(node, ExtendsNode):
                new_child_nodes = self.get_toplevel_content_nodes(node)
                nodes.extend(new_child_nodes)
            if self.is_content_node(node):
                nodes.append(node)
        return nodes

    def get_unreachable_content(self):
        """
        Return all top-level text nodes when the template is extending another
        template. Those text nodes won't be displayed during rendering since
        only content inside of blocks is considered in inheritance.
        """
        if not self.is_extending(self.root):
            return []

        textnodes = self.get_toplevel_content_nodes(self.root)
        return [node.s for node in textnodes]


def get_unreachable_content(root):
    check = TemplateCheckContent(root)
    return check.get_unreachable_content()


class TemplateCheckNextButton(object):
    def __init__(self, root):
        self.root = root

    def get_next_button_nodes(self, root):
        nodes = []
        for node in root.nodelist:
            if isinstance(node, (ExtendsNode, BlockNode)):
                new_child_nodes = self.get_next_button_nodes(node)
                nodes.extend(new_child_nodes)
            elif isinstance(node, NextButtonNode):
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


def format_source_snippet(source, arrow_position, context=5):
    """
    Display parts of a source file with an arrow pointing at an exact location.
    Will display ``context`` number of lines before and after the arrow
    position.

    Example::

          15 |     <p>
          16 |         Please provide your information in the form below.
          17 |     </p>
          18 |
          19 |     {% formrow form.my_field with label = "foo" %}
        -----------^
          20 |
          21 |     {% next_button %}
          22 | {% endblock %}
    """
    lines = split_source_lines(source)
    error_line = 0
    for line in lines:
        if line.start <= arrow_position < line.end:
            error_line = line
            break
    start_context = max(error_line.lineno - 1 - context, 0)
    end_context = min(error_line.lineno + context, len(lines))
    before = lines[start_context:error_line.lineno]
    after = lines[error_line.lineno:end_context]

    error_prefix = max(len(str(error_line.lineno)), 4) + len(' | ')
    error_length = max(arrow_position - error_line.start, 0)
    error_arrow = ('-' * (error_prefix + error_length)) + '^'
    return '\n'.join(chain(
        [format_error_line(line) for line in before],
        [error_arrow],
        [format_error_line(line) for line in after],
    ))
