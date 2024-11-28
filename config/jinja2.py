from collections import Counter

from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext, ngettext
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from jinja2 import Environment


def count_answered(request, topic_id):
    answers = request.session.get("answers", {})
    questions = answers.get(str(topic_id), {})
    return len(questions)


def sorted_answers(answers):
    return list(sorted(answers, key=lambda x: x.code))


def join_answer_contents(answers):
    answers = sorted_answers(answers)

    all_ps = []
    for answer in answers:
        for p in answer.content.content:
            all_ps.append(p)
    ps_count = Counter(all_ps)

    blocks, common_ps = [], []
    for answer in answers:
        for p in answer.content.content:
            if ps_count[p] > 1 and p not in common_ps:
                common_ps.append(p)

        ps = [p for p in answer.content.content if ps_count[p] <= 1]
        if len(ps) == 0:
            q_index = answer.question.index
            t_index = answer.question.topic.index
            raise Exception(
                f"Empty content for answer {answer.code} of question {t_index}.{q_index}"
            )

        blocks.append(
            {
                "description": answer.content.description,
                "code": answer.code,
                "ps": add_full_stops(ps),
            }
        )

    if len(common_ps) > 0:
        blocks.append(
            {"description": "Recomanacions comunes", "ps": add_full_stops(common_ps)}
        )

    return blocks


def add_full_stops(ps):
    return [add_full_stop(p) for p in ps]


def add_full_stop(p):
    if not p.endswith("."):
        p += "."
    return p


def environment(**options):
    env = Environment(extensions=[], **options)
    env = Environment(extensions=["jinja2.ext.i18n"], **options)
    env.install_gettext_callables(gettext=gettext, ngettext=ngettext, newstyle=True)
    env.globals.update(
        {
            "url": reverse,
            "len": len,
            "static": static,
            "settings": settings,
            "sorted_answers": sorted_answers,
            "count_answered": count_answered,
            "join_answer_contents": join_answer_contents,
        }
    )
    return env