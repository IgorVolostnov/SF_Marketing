import random
from database_requests import Execute


class KeyBoardBot:
    def __init__(self):
        self.execute = Execute()

    @staticmethod
    async def get_first_keyboard() -> dict:
        button_first_keyboard = {'goal': 'Поставить цель 🎯',
                                 'outlay': 'Расходы 🧮',
                                 'income': 'Доходы 💰,',
                                 'category': 'Категории расходов 📋'}
        return button_first_keyboard

    @staticmethod
    async def get_outlay(known_category: bool) -> dict:
        if known_category:
            button_outlay_keyboard = {'goal': 'Изменить категорию 📋',
                                      'outlay': 'Аналитика расходов 📊',
                                      'back': 'Назад 🔙'}
        else:
            button_outlay_keyboard = {'auto': 'Автомобиль 📋',
                                      'business': 'Бизнес  📋',
                                      'souvenir': 'Благотворительность, помощь, подарки 📋',
                                      'home_appliances': 'Бытовая техника и расходные материалы 📋',
                                      'children': 'Дети 📋',
                                      'pets': 'Домашние животные 📋',
                                      'health ': 'Здоровье и красота 📋',
                                      'loans': 'Ипотека, долги, кредиты 📋',
                                      'communal': 'Коммунальные платежи 📋',
                                      'taxes': 'Налоги и страхование 📋',
                                      'education': 'Образование 📋',
                                      'clothes': 'Одежда и аксессуары 📋',
                                      'relax': 'Отдых и развлечение 📋',
                                      'food': 'Питание 📋',
                                      'repair': 'Ремонт и мебель 📋',
                                      'household ': 'Товары для дома 📋',
                                      'transport': 'Транспорт 📋',
                                      'hobby': 'Хобби 📋',
                                      'connection': 'Связь и интернет ',
                                      'goal': 'Добавить категорию 📋',
                                      'outlay': 'Аналитика расходов 📊',
                                      'back': 'Назад 🔙'}
        return button_outlay_keyboard

    @staticmethod
    async def text_for_timer() -> str:
        text = ['Не бывает статей расходов, которые не были бы важны для вас. Чтобы тратить меньше следует '
                'сокращать каждую статью пропорционально друг другу, т.е. вычитывать средства из каждой статьи '
                'в одинаковом процентном соотношении.',
                'Наибольшей оптимизации подлежат те статьи расходов, на которые уходит наибольшее количество '
                'средств из вашего бюджета, т.к. расходы по ним, скорее всего, можно сократить.',
                'Не нужно стремиться к покупкам вещей, разрекламированных как экономные, или оптовым закупкам. '
                'Психика человека устроена таким образом, что за счёт кажущейся дешевизны или предполагаемой '
                'скидки он будет неосознанно стремиться к тому, чтобы взять больше, а это означает, что и '
                'тратить он будет больше.',
                'Финансовое планирование – залог материального благополучия, наличия «подушки безопасности» в '
                'непредвиденных жизненных ситуациях, возможность достичь многих материальных целей, и даже стать '
                'финансово независимым человеком.',
                'Чтобы иметь возможность быть готовым, если уж не ко всему, то ко многому, нужно иметь чёткое '
                'представление о том, что вы будете делать в той или иной ситуации, а также разработать свою '
                'стратегию по достижению целей. Всё это и включает в себя финансовое планирование.',
                'Лучшим временем для приведения в порядок своего бюджета и планирования является начало года. '
                'Но, конечно же, ждать его наступления ни в коем случае не нужно. Приступайте к делу сразу же: '
                'определяйте свои цели, просчитывайте действия, ищите новые возможности и варианты. '
                'Это станет вашим первым шагом к процветанию и финансовому благополучию.',
                'Грамотное отношение к своему бюджету должно стать частью образа жизни, стимулом к профессиональному, '
                'карьерному и личностному росту; навыком, который сделает достаток вашим верным спутником и гарантом '
                'уверенности в любой жизненной ситуации.',
                'Вместо того, чтобы придерживаться жестких правил, лучше проанализировать свои финансы и определить '
                'процент, который получится комфортно откладывать каждый месяц. Без ущерба для уровня жизни.',
                'Иногда мелкие траты на удовольствия — стаканчик кофе или кино — играют важную роль в нашем '
                'психоэмоциональном состоянии, да и просто помогают расслабиться. '
                'Вместо полного исключения мелких трат, лучше установить лимит на них и следить за своими '
                'расходами в целом.',
                'Иногда покупка товара по цене на 50% дешевле оказывается «мусором», который вскоре придется '
                'заменить или даже выбросить. Последнее касается продуктов, которые по уценке первой свежести '
                'точно не будут. Вместо тотальной экономии на здоровье лучше действовать с умом и анализировать, '
                'действительно ли вам нужен продукт и стоит ли он своих денег.',
                'Лучше ограничиться одной кредитной картой, которую вы сможете обслуживать, и использовать ее не '
                'для набора бонусных баллов, а для удобства в оплате и контроля расходов.',
                'Инвестирование — это важная часть финансового планирования, но не стоит рисковать всей своей '
                'свободной наличностью. Всегда существует риск потери финансов при неудачном инвестировании. '
                'Лучше разумно распределить деньги между различными активами и инструментами с разным уровнем риска. '
                'Такой подход поможет сбалансировать доход и минимизировать потери.']
        return random.choice(text)
