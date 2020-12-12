from core.models import Pool, PoolAnswer, UserAnswer, AnswerOption, Question
from core.teams_utils import TeamsMetadata


def save_answers(data: dict[str, str], pool: Pool , pool_answer: PoolAnswer,
        metadata: TeamsMetadata) -> None:
    
    answers_to_save = []

    for question in pool.questions.all():
        answer = data.get(f'question_{question.id}')
    
        if not answer:
            continue

        answers_to_save.append(
            _create_answer_mapping[question.category](
                question, answer, metadata.user, pool_answer
            )
        )
        
    UserAnswer.objects.bulk_create(answers_to_save)
    return

def _create_closed_answer(question, answer, user, pool_answer):
    return UserAnswer(
        question=question, option_id=answer, pool_answer=pool_answer, user=user
    )

def _create_open_answer(question, answer, user, pool_answer):
    answer_option, _ = AnswerOption.objects.get_or_create(
        question=question, text=answer.lower()
    )
    return UserAnswer(
        question=question, pool_answer=pool_answer, option_id=answer_option.id,
        user=user
    )

_create_answer_mapping = {
    Question.CLOSED: _create_closed_answer,
    Question.OPEN: _create_open_answer
}
