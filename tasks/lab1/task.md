# 1. Подготовка

Пропишите `python manage.py migrate` (для создания начальных таблиц в базе данных)

Создайте пользователя администратора `python manage.py createsuperuser` (email не обязателен, 
помните, что пароль не отображается)


# 2. Работа с формой регистрации

Скопируйте форму регистрации `signup.html` из `files/lab1` в `app_login/templates/login`

В `views.py` приложения `app_login` создайте представление `SignUpView` (в этот раз воспользуемся классовым представлением, 
для разнообразия) 

```python
from django.views import View

class SignUpView(View):
    def get(self, request):
        return render(request, "login/signup.html")
```

В `urls.py` приложения `app_login` зарегистрируйте представление (name оставьте как в примере)

```python
from .views import SignUpView

path('signup/', SignUpView.as_view(), name="signup_view")
```

Теперь форма регистрации будет отображаться

## 2.1 Использование форм в Django 

Сначала немного модифицируйте `signup.html` необходимо добавить атрибут 
`action="." method="post"` в html форму. Также не забываем про `{% csrf_token %}`

![img.png](pic_for_task/img.png)

Теперь приступим к созданию формы в Django, чтобы обрабатывать данные с формы.

Из стандартных форм мы можем использовать `UserCreationForm` однако, там нет проверки по email, 
поэтому создадим свою форму на базе стандартной.

Ниже приведён кусок стандартной формы в Django для ознакомления

![img_1.png](pic_for_task/img_1.png)

Реализуем свою форму на базе `UserCreationForm`, ввиду того, что в стандартной форме нет обработчика для email

Создадим файл `forms.py` в приложении `app_login` и заполните следующим кодом. Здесь на
базе пользователя (модели User) создаётся форма. Так как UserCreationForm наследуется от 
`forms.ModelForm` (форм автоматически подстраивающие названия полей из моделей).

```python
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField
from django.forms import EmailField


class CustomUserCreationForm(UserCreationForm):
   email = EmailField()

   class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']
       field_classes = {"username": UsernameField}
```
В представления `view.py` приложения app_login добавим наши формы, а SignUpView и его
post метод допишем следующим кодом:

```python
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User


class SignUpView(View):


   def get(self, request):
       ...

   def post(self, request):
       form = CustomUserCreationForm(data=request.POST)
       if form.is_valid():
           username = form.cleaned_data.get('username')
           email = form.cleaned_data.get('email')
           password = form.cleaned_data.get('password1')
           # Создаём нового пользователя (подробнее на практике с ORM)
           user = User.objects.create_user(username=username, email=email, password=password)
           user.save() 
           login(request, user)  # Авторизируем пользователя
           return redirect('/')
       return redirect('login:signup_view')
```

Теперь можно будет создавать пользователей через форму регистрации

## 2.2 Вывод ошибок в форму

Однако скорее всего с первого раза пользователь не создатся, так как могут быть ошибки, 
которые не видны

Добавим возможные ошибки в форме для вывода.

Заменим `redirect` на `render` в классе `SignUpView` в методе `post`

```python
return render(request, "login/signup.html", context={'errors': form.errors})
```
![img_2.png](pic_for_task/img_2.png)

Затем в шаблоне `signup.html` внесем правки, чтобы ошибки отображались (для каждого поля)

```html
{% if errors.username%}
<span class="txt1">
  {{errors.username}}
</span>
{% endif %}
```

![img_3.png](pic_for_task/img_3.png)

![img_4.png](pic_for_task/img_4.png)

Теперь в случае ошибок, эти ошибки будут отображаться в форме

![img_5.png](pic_for_task/img_5.png)


## 2.3 Форма для авторизации

Ранее писали форму для авторизации, так как они типовые, если авторизироваться по login, то используем стандартную форму авторизации
Django

post метод функции `login_view` во `views.py` теперь будет таким

```python
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            add_user_to_cart(request, user.username)
            add_user_to_wishlist(request, user.username)
            return redirect("/")
        return render(request, "login/login.html", context={"error": "Неверные данные"})
```

Теперь авторизация работает как и раньше, но мы использовали форму для проверки данных пришедших на сервер.

# 3. Авторизация через github

Теперь подключим авторизацию через github для этого установим библиотеку 

`pip install social-auth-app-django`

Настроим приложение Django. В `settings.py` пропишем

```python
INSTALLED_APPS = [
    ...
    'social_django',
    ...
]


AUTHENTICATION_BACKENDS = (
   'social_core.backends.github.GithubOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/' # Чтобы после авторизации перенаправлялось на стартовую страницу

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email', 'read:user']
```

Далее необходимо создание приложение на Github, для этого перейдите на страницу настроек вашей учетной записи на 
Github и выберите вкладку "Developer settings". 

![img_6.png](pic_for_task/img_6.png)


Затем нажмите кнопку "New OAuth App" и заполните необходимые поля. (`Важное замечание! 
Использование Github тем и хорошо для авторизации, что позволяет работать с локальным хостом, 
большинство авторизационных сервисов требует доступ к работающему домену (нужно будет поменять ссылку при деплое)`)

```python
http://127.0.0.1:8000  # Homepage URL

http://127.0.0.1:8000/auth/complete/github/  # Authorization callback URL
```

![img_7.png](pic_for_task/img_7.png)

После создания приложения скопируйте "Client ID" и "Client Secret"(необходимо его 
создать, секретный ключ лучше сразу скопировать в `settings.py` об этом чуть ниже), 
эти данные будут использоваться для авторизации в вашем приложении Django.

![img_8.png](pic_for_task/img_8.png)

Далее копируем эти данные в `SOCIAL_AUTH_GITHUB_KEY` и `SOCIAL_AUTH_GITHUB_SECRET` 
в `settings.py` соответственно (скопировать свои данные)

![img_9.png](pic_for_task/img_9.png)

Добавьте следующие URL-адреса в корневой файл urls.py:

```python
path('auth/', include('social_django.urls', namespace='social'))
```

![img_10.png](pic_for_task/img_10.png)

Далее пропишем ссылку на авторизацию через github в шаблоне `login.html`

```python
href="{% url 'social:begin' 'github' %}"
```

![img_11.png](pic_for_task/img_11.png)

Произведем миграцию в БД, так как для хранения данных об авторизации необходимы таблицы.

`python manage.py migrate`


Теперь при нажатии на авторизацию через github перебрасывает на github, а затем при удачной 
авторизации - на стартовую страницу.

![img_12.png](pic_for_task/img_12.png)

![img_13.png](pic_for_task/img_13.png)

![img_14.png](pic_for_task/img_14.png)

Теперь на сервис можно заходить под аккаунтом github.

Единственное, что нужно будет дописать, это передать в функцию login при регистрации во views.py приложения 
app_login

```python
login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Авторизируем пользователя
```

Это необходимо, чтобы избежать непонимания Django как именно производить регистрацию, так как теперь у нас 2 подхода к регистрации пользователей
классический(через форму) и через сервис github.

![img_69.png](pic_for_task/img_69.png)

# 4. Развертывание проекта на сервис pythonanywhere

## 4.1 Скрываем всю чувствительную информацию

Устанавливаем модуль `python-dotenv` - пакет для работы удобной работы с переменными среды

`pip install python-dotenv`

Cоздайте шаблон `template.env` в корне проекта, где будем хранить переменные окружения. 
Этот файл не будет содержать самих значений, а только названия переменных.

```env
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
SOCIAL_AUTH_GITHUB_KEY=
SOCIAL_AUTH_GITHUB_SECRET=
```

![img_15.png](pic_for_task/img_15.png)

Создайте файл `.env` м по тем же ключам добавьте значения

```python
SECRET_KEY=<ваши значения>
DEBUG=true
ALLOWED_HOSTS='localhost,127.0.0.1'
SOCIAL_AUTH_GITHUB_KEY=<ваши значения>
SOCIAL_AUTH_GITHUB_SECRET=<ваши значения>
```

![img_16.png](pic_for_task/img_16.png)

`SECRET_KEY`, `SOCIAL_AUTH_GITHUB_KEY`, `SOCIAL_AUTH_GITHUB_SECRET` 
получаем из соответствующих переменных файла `settings.py`

В файле `settings.py` выполняем загрузку переменных среды из файла `.env` с помощью 
установленного пакета, также в `settings.py` на нужных местах необходимо выгрузить 
значения из окружения:

```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()  # здесь загружаются данные из .env и отправляются в переменные окружения

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG') == 'true'

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS').split(',')]

SOCIAL_AUTH_GITHUB_KEY=os.getenv('SOCIAL_AUTH_GITHUB_KEY')

SOCIAL_AUTH_GITHUB_SECRET=os.getenv('SOCIAL_AUTH_GITHUB_SECRET')
```

![img_17.png](pic_for_task/img_17.png)

![img_18.png](pic_for_task/img_18.png)

В `.gitignore` добавьте `.env`, чтобы на `github` не залилась чувствительная информация

![img_19.png](pic_for_task/img_19.png)

Затем в `settings.py` рядом со `STATIC_URL = 'static/'` пропишите

```python
STATIC_URL = "static/"  # Папка в корне проекта, где будут собираться статические файлы
if 'localhost' in ALLOWED_HOSTS:
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Папка для локального проекта
else:
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # Папка для сервера
```

Используя параметр `STATICFILES_DIRS` вы можете указать, где Django будет искать статические файлы помимо папки `static` в каждом приложении

Конструкция if - else поможет в будущем и работать на сервере и на локальном проекте.
Так как параметр `STATICFILES_DIRS` нужен в режиме работы с локальным проектом (если вы решите собрать 
все статические файлы в одну корневую папку static, но даже если она указана, но её нет физически, 
то никакой ошибки не будет), 
а `STATIC_ROOT` с сервером (на сервере чаще всего присутствует условие, что вся статика должна быть в отдельной корневой папке static). 
Одновременно `STATICFILES_DIRS` и `STATIC_ROOT` не могут существовать в одном файле

Перезапустите сервер и проверьте, что переменные окружения правильно подтянулись и всё работоспособно.

Обновите файл `requirements.txt`, чтобы внести в него новые модули и была возможность восстановить окружение

`pip freeze > requirements.txt`

Сделайте коммит ваших изменений (`не включайте в коммит файл .env. 
Так как чтобы .gitignore заработал сначала нужно его закоммитить, иначе если закоммитить в одном коммите и .gitignore и .env,
то .env отправится на github, чего мы не хотим`) и отправьте всё на сервер github. 

## 4.2 Деплой на сервис pythonanywhere

Зарегистрируйтесь на https://www.pythonanywhere.com/

Создайте Web приложение нажав `“Add a new app”`

![img_20.png](pic_for_task/img_20.png)

Ваш бесплатный домен, по которому вы можете получать доступ к вашему приложению. 
Сохраните название этого домена, он понадобится чуть позже. Нажимаем Next

![img_21.png](pic_for_task/img_21.png)

Выбираем “Manual configuration”.

![img_22.png](pic_for_task/img_22.png)

Чтобы избежать непредвиденных ситуаций при развертывании выберите ту версию интерпретатора, которая была у вас на локальной машине.
На текущий момент сервис ограничен python 3.10, поэтому если использовали python 3.11 и 3.12, то в теории проблем не должно быть
если выберете 3.10.

![img_23.png](pic_for_task/img_23.png)

Нажимаем Next и ждем пока создастся приложение

![img_24.png](pic_for_task/img_24.png)

![img_25.png](pic_for_task/img_25.png)

В pythonanywhere выбираем Consoles и Bash

![img_26.png](pic_for_task/img_26.png)

Перед вами откроется консоль, через которую вы сможете настроить удаленный сервер и загрузить туда ваш Django проект

![img_27.png](pic_for_task/img_27.png)

Далее необходимо склонировать `Ваш репозиторий` с github, что недавно пушили. 
Возьмём ссылку с вашего репозитория

![img_28.png](pic_for_task/img_28.png)

А затем с помощью команды загрузим проект на сервер:

`git clone <url вашего репозитория>`

Как пример `git clone https://github.com/EgorOb/pythonPy110_part2_dev.git`

![img_29.png](pic_for_task/img_29.png)

Дальше идёт информация для тех, кто может столкнуться с данной проблемой

### Возможная проблема доступа

Если ваш репозиторий открытый, то проблем скорее всего не возникнет. Если он закрытый, 
то попросит ввести логин и пароль от github, который будет заблокирован, так как сервис сменил политику авторизации

![img_30.png](pic_for_task/img_30.png)

Данная ошибка возникнет при любом исходе, если будете взаимодействовать с github на правах выше чтения данных,
допустим запушите изменения с сервера прямо на github, то возникнет данная ошибка

Это всё решается при помощи использования токена доступа при клонировании 

`git clone https://username:token@github.com/your_username/your_repository.git` 

или установлении ссылки, когда репозиторий склонирован 

`git remote set-url origin https://username:token@github.com/your_username/your_repository.git` 

Для этого необходимо для начала получить токен доступа, в общем нужно повторить тоже самое, что и получение токена для связи с PyCharm. 
Заходим на свой аккаунт github, далее идём в настройки.

![img_31.png](pic_for_task/img_31.png)

Листаем вниз до вкладки Developer settings

![img_32.png](pic_for_task/img_32.png)

Далее заходим в Personal access tokens -> Token (classic)

![img_33.png](pic_for_task/img_33.png)

Создадим новый токен Generate new token -> Generate new token (classic)

![img_34.png](pic_for_task/img_34.png)

Далее необходимо дать название токена и установить время жизни токена. 
Токен выдаётся по стандарту OAuth, и при каждом запросе на добавление и изменение 
данных в репозитории из сторонних источников (допустим IDE) будет проверять возможность 
данных изменений от конкретного пользователя в соответствии с выданным токеном и 
параметрами (правами) устанавливаемыми при регистрации токена.

GitHub рекомендует не устанаваливать бессрочный срок жизни токена для безопасности.

В правах можно дать `repo`, `workflow` и `gist`, можно и меньше, но нужно точно 
знать что вы будете делать используя данный токен.

![img_35.png](pic_for_task/img_35.png)

После выбора необходимых параметров внизу нужно создать токен нажав на Generate token

![img_36.png](pic_for_task/img_36.png)

После создания токена появится окно и предупреждение, в котором говорится о необходимости копирования токена сейчас и невозможности увидеть текст токена в будущем. Если не сохранить его где-нибудь или не вставить в форму требуемую для IDE, то токен придётся создавать заново.

![img_37.png](pic_for_task/img_37.png)

Теперь осталось только вставить данный токен в `git clone`

`git clone https://EgorOb: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@github.com/EgorOb/pythonPy110_part2_dev.git` 

Теперь закрытый репозиторий можно склонировать

![img_38.png](pic_for_task/img_38.png)

### Продолжение деплоя

С помощью команды ls убедимся что в директории существует папка с названием нашего проекта и перейдём в нее с помощью команды

`cd <название вашего репозитория>`

![img_39.png](pic_for_task/img_39.png)

Далее нужно настроить виртуальное окружение, чтобы установить все зависимости, которые были установлены на вашей локальной машине. Создать виртуальное окружение можно с помощью команды

`python -m venv <название виртульного окружения>`

Создание окружения может занимать значительное время

![img_40.png](pic_for_task/img_40.png)

Теперь следует активировать виртуальное окружение с помощью следующей команды

`source <название виртуального окружения>/bin/activate`

![img_41.png](pic_for_task/img_41.png)

Установим все зависимости из файла `requirements.txt`

`pip install -r requirements.txt`

Далее создайте файл `.env` и заполните его необходимыми данными:

`cp template.env .env`

Любым удобным способом заполнить файл .env на удаленной машине (например, через графический интерфейс) Files -> <папка с вашим проектом> -> .env

![img_42.png](pic_for_task/img_42.png)

Скопируйте данные из вашего локального .env (все ключи) в .env на сервере 

![img_43.png](pic_for_task/img_43.png)

Обратите внимание, SECRET_KEY как на локальной машине, ALLOWED_HOSTS согласно вашему домену, 
полученному на 3 шаге (если вдруг не сохранили этот адрес, то он есть на вкладке Web)

Зеленая кнопка, чтобы сохранить результат

![img_44.png](pic_for_task/img_44.png)

Возвращаемся в консоль и прописываем команду для сбора всех статических файлов в одном месте (это условие сервера)

`python manage.py collectstatic`

![img_45.png](pic_for_task/img_45.png)

Подготовка среды закончена теперь, нужно настроить приложение. Переходим во вкладку Web

![img_46.png](pic_for_task/img_46.png)

Находим блок “Code”, настраиваем папку с исходным кодом вашего проекта и рабочей директорией. Не обращаем внимание, что написано VegetableStore, это прошлый проект, в вашем случае будет папка с которой работаете на сервере 
(будет называться как ваш репозиторий)

![img_47.png](pic_for_task/img_47.png)

Далее нужно настроить “WSGI configuration file”: нажимаем на синюю ссылку

![img_48.png](pic_for_task/img_48.png)

В wsgi файле комментируем (работает комбинация Ctrl+/) 19-47 строки

![img_49.png](pic_for_task/img_49.png)

Раскомментируем 76-89 строки отвечающие за wsgi для Django

![img_50.png](pic_for_task/img_50.png)

Далее нужно настроить путь до файлов с настройками вашего приложения (файл settings.py) и файла, который управляет вашим приложением (manage.py). Переменная path должна быть равна пути до вашего проекта

Было

![img_51.png](pic_for_task/img_51.png)

Стало

![img_52.png](pic_for_task/img_52.png)

Переменная окружения на ваш модуль с настройками проекта должна быть изменена в соответствии с названием вашего проекта. Подсмотреть её значение можно в файле wsgi.py вашего Django проекта

![img_53.png](pic_for_task/img_53.png)

Было

![img_54.png](pic_for_task/img_54.png)

Стало

![img_55.png](pic_for_task/img_55.png)

Также нужно подгрузить переменные среды, находящиеся в файле .env

```python
from dotenv import load_dotenv

load_dotenv(os.path.join(path, '.env'))
```

![img_56.png](pic_for_task/img_56.png)

Сохраняем файл. Кнопка Save

![img_57.png](pic_for_task/img_57.png)

Настраиваем путь до вашего виртуального окружения во вкладке Web

`<путь до проекта>/<названием виртуального окружения>`

![img_58.png](pic_for_task/img_58.png)


Во вкладке Web настраиваем раздел “Static files”:

* URL = STATIC_URL из settings.py
* Directory = <путь до проекта>/<название папки со статическими файлами>

![img_59.png](pic_for_task/img_59.png)

В данном сервисе проблематично указывать статические файлы для каждого приложения, придётся делать это вручную. 
Выход вынести все статические файлы в одну папку, что мы и сделали при вынесении папки со статическими файлами в корень проекта (collectstatic)

Перезапускаем приложение (зеленая кнопка, нужно будет подождать определенное время) и переходим по ссылке выше (доменное имя)

![img_60.png](pic_for_task/img_60.png)

В результате, если всё сделано верно теперь на сервисе развернуто приложение с аналогичным функционалом как на локальной машине и можно будет его проверить через любой браузер по вашему доменному имени.

![img_61.png](pic_for_task/img_61.png)

Обычно на практике никто не сохраняет БД на github, 
так как базы данных не должны также храниться в открытом месте, но в качестве упрощения себе жизни в .gitignore 
не стоит строчка с игнорированием базы данных Django (которая по умолчанию SQLite). 
Если база не перенеслась или поставили игнорирование базы в .gitignore, то необходимо создать таблицы в БД
командой в консоле сервиса (обратите внимание, что в консоле должно быть активировано виртуальное окружение)

`python manage.py migrate`

Ну а затем можно создать администратора, как на локальном проекте

`python manage.py createsuperuser`

Если требуется, чтобы на вашем сервисе также поддерживалась авторизация через github, то нужно теперь на github указать домен на pythonanywhere.
Одновременно нельзя указать и локалхост и pythonanywhere. Но можно сделать 2 приложения на github 
для работы одного с локалхост, а второго с сервером на pythonanywhere

![img_65.png](pic_for_task/img_65.png)

Но учите, что есть разница какое соединение http или https вы используете через pythonanywhere для авторизации через github.
Если используете http, на github должен быть указан этот протокол (как на картинке выше). Если https, то htpps.

Теперь ваш проект развернут и к нему можно обратиться из вне, он такой же работоспособный как и ваш локальный проект, 
за исключением некоторых моментов с данными из БД (нет данных о корзине, избранном и т.д., так как нет связи с какой-то удаленной БД). 
Главным минусом данного сервиса является то, то он блокирует все внешние соединения TCP на бесплатном режиме,
поэтому не получится подключиться к своей базе данных, допустим PostgreSQL на другом сервисе и придется работать с БД SQLite, что есть на сервисе. Поэтому данный сервис хорош для создания малонагруженных прототипов,
другие задачи необходимо решать с помощью более функциональных сервисов.

## 4.3. Частые вопросы после развертки первого приложения на pythonanywhere

* Как быстро перейти в консоль с виртуальным окружением?

> Можно зайти во вкладку Consoles и выбрать там вашу рабочую консоль. 
> На бесплатном аккаунте можно создать и поддерживать только 2 консоли. Закрыть консоль можно
> на крестик.

![img_66.png](pic_for_task/img_66.png)

> Если вдруг нет той консоли в которой работали, то через вкладку 
> Web можно зайти в консоль под виртуальной средой

![img_67.png](pic_for_task/img_67.png)

* Где посмотреть, если что-то упало и сайт не отображается?

> В логе ошибок на вкладке Web

![img_62.png](pic_for_task/img_62.png)

* Я реализовал новый функционал в локальном проекте! Как это перенести на сервис?

> Перенос на сервис идёт по этапам получения изменений с github. Поэтому что необходимо:
> 1. Запуште ваши изменения на github (Если скачивали и использовали новые модули, 
> то перед отправлением на гитхаб сначала обновите requirements.txt.)
> 2. Подтяните ваши изменения с github на сервис используя команду `git pull`
>    * Есть определенная вероятность, что произойдет конфликт при слиянии(так как на гитхабе и на сервисе 
>    вы можете работать и изменять одни и теже файлы и нужно будет выбрать что с этим делать). Один из способов это 
>    откатить определенные изменения до последнего известного коммита на сервере, а затем снова сделать `git pull`.
>    Допустим часто такое бывает когда база данных не записана в .gitignore и на локальном проекте и на сервере отличается, так как они должны находиться там,
>    где используются, и соответственно могут иметь различия. Тогда можно попробовать откатить изменения до последнего известного коммита на сервере
>    при помощи команды  `git reset`, `git restore`, `git rm`, однако если данные что есть на сервере нужны, то придётся решать конфликт слияния (что для обычных файлов не так сложно, но бывает проблематично для баз данных).
> 3. Если после подтягивания ваших изменений вы использовали новые статические файлы или делали новые таблицы в базе данных, то можно использовать команды
> `python manage.py collectstatic` или `python manage.py migrate`
> 4. Перезапустите ваш сервер и теперь сервис будет с актуальными изменениями.

Пример ошибки при подтягивании изменений

![img_68.png](pic_for_task/img_68.png)

Сообщение об ошибке говорит о том, что у вас есть непроиндексированные (untracked) 
файлы в рабочем каталоге, которые перезапишутся при слиянии (merge). 
Прежде чем продолжить, вам нужно решить проблему с этими файлами. 

Вот несколько шагов, которые вы можете предпринять:

1. Если файлы на сервере просто не нужны, то можно их удалить, `rm cart.json wishlist.json`, а 
затем сделать `git pull`

2. Если пока не известно нужны они и нет, то можно их добавить в систему контроля версий `git add cart.json wishlist.json`
сделать временное сохранения изменений без фиксации (commit) `git stash`, затем сделать `git pull`, 
и уже решить что делать с теми файлами или их применять `git stash apply` и решать что оставлять что на сервере или на github 
или удалить эти файлы из временных  `git stash drop`.

3. Также можно добавить файлы в систему индексации `git add cart.json wishlist.json`, сделать коммит `git commit -m 'текст описания коммита'`,
а уже затем при `git pull` разбираться с коммитом слияния.

Для примера рассмотрю второй вариант.

![img_70.png](pic_for_task/img_70.png)

* Полезные команды git для работы с терминалом pythonanywhere

> 1. `git restore <file>` - откатить файл до последнего известного коммита. 
Без изменения истории коммитов.
Применяется только к файлам которые есть в системе индексации. 
Откатывает до последнего известного состояния в системе индексации. 
Т.е. если файл до этого не был в системе индексации, то откатить его не получится, даже если добавить в систему индексации).

> 2. `git revert <commit>` - создает новый коммит, который отменяет изменения, внесенные предыдущим коммитом.
Удобно когда нужно откатиться к определенному коммиту в ветке, без потери всей истории, что была после этого коммита.

> 3. `git stash` - используется для временного сохранения изменений, 
чтобы вы могли переключиться на другую ветку без фиксации (commit) изменений. 
После git stash можно безопасно сделать git pull, затем нужно решить, что делать с данными временными файлами.
> * `git stash apply`: Эта команда применяет последний stash к вашему текущему рабочему дереву, но не удаляет stash.
> * `git stash pop`: Эта команда также применяет последний stash, но при этом удаляет его из списка stash.
> * `git stash drop`: Эта команда удаляет последний stash без его применения к текущему рабочему дереву.

> 4. `git reset` - используется для сброса текущей ветки к определенному коммиту. 
> По умолчанию сбрасывает до последнего коммита, но можно явно указать до какого.
> Есть 3 варианта сброса:

> * `git reset --soft <commit>` - Этот вариант устанавливает указатель HEAD и текущую ветку на определенный коммит, но оставляет изменения в индексе. 
> Это полезно, если вы хотите объединить несколько коммитов в один.

> * `git reset --mixed <commit>` (стоит по умолчанию `git reset <commit>`) - Этот вариант по умолчанию, 
> и он устанавливает указатель HEAD и текущую ветку на определенный коммит, 
> а также сбрасывает изменения в индексе. Рабочий каталог остается неизменным. Файлы выходят из системы контроля версий, но при это не удаляются.

> * `git reset --hard <commit>` - Этот вариант устанавливает указатель HEAD и текущую ветку на определенный коммит. 
> Все изменения в вашем рабочем каталоге и индексе будут потеряны. Будьте осторожны с этой командой, так как она изменяет историю и может привести к потере данных.

> 5. `git rm <file>` - удаляет файл из индекса и из рабочего каталога.


* Можно ли включить защищенное соединение?

> Да, сервис pythonanywhere позволяет работать с протоколом https. Forse HTTPS перевести в Enable. 
> Необходимо перезагрузить сервер

![img_63.png](pic_for_task/img_63.png)

![img_64.png](pic_for_task/img_64.png)


* Как перевести сервис из режима дебага?

> В параметрах DEBUG в `.env` на вашем сервисе с `true` поменяйте на `false` (необходимо сохранить, 
> а затем перезапустить сервер)