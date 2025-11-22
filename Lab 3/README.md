# Основы обработки данных с помощью R и Dplyr


## Цель работы

1.  Развить практические навыки использования языка программирования R
    для обработки данных
2.  Закрепить знания базовых типов данных языка R
3.  Развить практические навыки использования функций обработки данных
    пакета dplyr – функции select(), filter(), mutate(), arrange(),
    group_by()

## Исходные данные

1.  Rstudio Desktop
2.  Наше рабочее окружение

## План

1.  Проанализировать встроенный в пакет dplyr набор данных языка R
2.  Ответить на вопросы

## Шаги:

``` r
sessionInfo()
```

    R version 4.5.1 (2025-06-13 ucrt)
    Platform: x86_64-w64-mingw32/x64
    Running under: Windows 11 x64 (build 26100)

    Matrix products: default
      LAPACK version 3.12.1

    locale:
    [1] LC_COLLATE=Russian_Russia.utf8  LC_CTYPE=Russian_Russia.utf8   
    [3] LC_MONETARY=Russian_Russia.utf8 LC_NUMERIC=C                   
    [5] LC_TIME=Russian_Russia.utf8    

    time zone: Europe/Moscow
    tzcode source: internal

    attached base packages:
    [1] stats     graphics  grDevices utils     datasets  methods   base     

    loaded via a namespace (and not attached):
     [1] compiler_4.5.1    fastmap_1.2.0     cli_3.6.5         tools_4.5.1      
     [5] htmltools_0.5.8.1 yaml_2.3.10       rmarkdown_2.30    knitr_1.50       
     [9] jsonlite_2.0.0    xfun_0.53         digest_0.6.37     rlang_1.1.6      
    [13] evaluate_1.0.5   

Проанализировать встроенные в пакет nycflights13 наборы данных с помощью
языка R и ответить на вопросы:

1.  Сколько встроенных в пакет nycflights13 датафреймов?

> data(package = “nycflights13”)

Data sets in package ‘nycflights13’:

airlines Airline names. airports Airport metadata flights Flights data
planes Plane metadata. weather Hourly weather data

1.  Сколько строк в каждом датафрейме?

> nrow(airlines) \[1\] 16

> nrow(airports) \[1\] 1458

> nrow(flights) \[1\] 336776

> nrow(planes) \[1\] 3322

> nrow(weather) \[1\] 26115

1.  Сколько столбцов в каждом датафрейме?

> ncol(airlines) \[1\] 2

> ncol(airports) \[1\] 8

> ncol(flights) \[1\] 19

> ncol(planes) \[1\] 9

> ncol(weather) \[1\] 15

1.  Как просмотреть примерный вид датафрейма?

> airlines %\>% glimpse Rows: 16 Columns: 2 $ carrier <chr> “9E”, “AA”,
> “AS”, “B6”, “DL”, “EV”, “F9”, “FL”, “HA”, “MQ”, “OO”,… $ name <chr>
> “Endeavor Air Inc.”, “American Airlines Inc.”, “Alaska Airlines I…

1.  Сколько компаний-перевозчиков (carrier) учитывают эти наборы данных
    (представлено в наборах данных)?

> airlines %\>% distinct(carrier) %\>% nrow() \[1\] 16

1.  Сколько рейсов принял аэропорт John F Kennedy Intl в мае?

> flights %\>% filter(origin == “JFK”, month == 5) %\>% count() 1 9397

1.  Какой самый северный аэропорт?

> airports %\>% arrange(desc(lat)) %\>% select(name) %\>% head(1) 1
> Dillant Hopkins Airport

1.  Какой аэропорт самый высокогорный (находится выше всех над уровнем
    моря)?

> airports %\>% arrange(desc(alt)) %\>% select(name) %\>% head(1) 1
> Telluride

1.  Какие бортовые номера у самых старых самолетов?

> planes %\>% arrange(year) %\>% head(1) %\>% select(tailnum, year)
> tailnum year 1 N381AA 1956

1.  Какая средняя температура воздуха была в сентябре в аэропорту John
    FKennedy Intl (в градусах Цельсия).

> weather %\>% filter(origin == “JFK”, month == 9) %\>%
> summarise(avg_temp_c = mean((temp - 32) \* 5/9, na.rm = TRUE))
> avg_temp_c 1 19.4

1.  Самолеты какой авиакомпании совершили больше всего вылетов в
    июне?Данные i2z1.ddslab.ru 3

> flights %\>% filter(month == 6) %\>% count(carrier, sort = TRUE) %\>%
> left_join(airlines, by = “carrier”) %\>% head(1) carrier n name  
> 1 UA 4975 United Air Lines Inc.

1.  Самолеты какой авиакомпании задерживались чаще других в 2013 году?
