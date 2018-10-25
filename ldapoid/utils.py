# -*- coding: utf-8 -*-
from StringIO import StringIO
import jinja2


def gen_from_tpl(tpl_dir, tpl, out_file=None, **kwargs):
    """
    Формирование файлов из шаблона.
    В шаблон tpl подставляются значения переменных, указанных в словаре kwargs
    и формируется конфигурационный файл или скрип, который записывается в файл указанный в качестве аргумента out_file.
    Если out_file не указан, то функция возвращает текст, сформированный из шаблона.
    :param tpl_dir: директория, где находятся файлы скриптов
    :param tpl: шаблон из которого нужно сформировать конфигурационный файл, скрипт и т.д.
    :param kwargs: это словарь параметров, которые будут подставлены в шаблон
    :param out_file: файл, который будет сформирован из шаблона
    :return: возвращает текст с подставленными переменными , если out_file=None
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(tpl_dir))
    template = env.get_template(tpl)
    if out_file is not None:
        with open(out_file, 'w') as f:
            f.write(template.render(**kwargs))
    else:
        return StringIO(template.render(**kwargs))
