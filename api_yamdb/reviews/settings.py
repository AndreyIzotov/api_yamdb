# Настройки для строковых методов моделей
FACTOR_FOR_REVIEW = 15  # Ограничитель для Review
FACTOR_FOR_COMMENT = 20  # Ограничитель для Comment


# Выбор оценки к отзыву, для формирования рейтинга

begin_rate = 1  # Начало диапазона оценок
end_rate = 10  # Конец диапазона оценок


def append_choice():
    """Функция для наполнения списка выбора оценок."""
    grade_choices = []
    for i in range(begin_rate, end_rate + 1):
        choice = (i, str(i))
        grade_choices.append(choice)
    return grade_choices


GRADE_CHOICES = append_choice()  # Список для выбора оценок
