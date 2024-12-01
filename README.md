# Практическая работа 2: Базовая 2D-игра «Инопланетное вторжение» с использованием Pygame
### Цель работы: Разработать игру «Инопланетное вторжение», в которой игрок управляет кораблём и должен уничтожить флот инопланетян. Работа позволит вам познакомиться с основами разработки игр на Python с помощью библиотеки pygame и позволит применить эти знания о компьютерной графике, анимации и управлении событиями в дальнейшем

### 1. Настройка окружения  
Для запуска игры требуется библиотека Pygame, обеспечивающая графический интерфейс и основные игровые механики.  
Установка выполняется командой:

```
pip install pygame
```

### 2. Создание игрового окна  
Игровое окно формируется методом pygame.display.set_mode(). Его параметры задаются объектом ai_settings, содержащим:  
Размеры экрана (ширина и высота).  
Цвет фона в формате RGB (ai_settings.bg_color).  

Экран обновляется в каждом цикле игры для обеспечения корректного отображения изменений.

### 3. Основной цикл игры
Игровой процесс организован в цикле while True, выполняющем следующие функции:  
Обработка пользовательских событий (движение корабля, стрельба).  
Обновление состояния объектов (корабль, пули, пришельцы).  
Проверка столкновений (пули с пришельцами, корабль с пришельцами).  
Перерисовка экрана для отображения актуального состояния.  

### 4. Класс Ship
Класс Ship описывает управляемый игроком корабль. 

Основные характеристики:  
Начальная позиция: центр нижней части экрана.  
Движение: вправо и влево с ограничением в пределах экрана, управляется стрелками клавиатуры.  
Обновление координат выполняется при обработке событий.  

### 5. Реализация стрельбы
Класс Bullet отвечает за создание и управление пулями. 

Его функциональность включает:  
Создание пули при нажатии пробела.  
Перемещение пули вверх по экрану с каждым обновлением.  
Удаление пуль, покидающих границы экрана.  


### 6. Генерация флота пришельцев
Флот пришельцев создаётся функцией create_alien. Каждый объект пришельца реализуется через класс Alien. 

Характеристики:  
Ряды пришельцев располагаются равномерно в зависимости от размеров экрана и объектов.  
Флот движется горизонтально. При достижении края экрана направление движения изменяется.  


### 7. Добавление конца игры и ограничения
Механика сложности и завершения включает:  

Жизни игрока: при столкновении с пришельцем или достижении нижней границы экрана игрок теряет одну жизнь. Игра завершается, если количество жизней равно нулю.  
Увеличение сложности: с каждым новым уровнем повышается скорость движения объектов и частота появления врагов.  
