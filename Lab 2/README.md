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
     [5] htmltools_0.5.8.1 rstudioapi_0.17.1 yaml_2.3.10       rmarkdown_2.30   
     [9] knitr_1.50        jsonlite_2.0.0    xfun_0.53         digest_0.6.37    
    [13] rlang_1.1.6       evaluate_1.0.5   

Проанализировать встроенный в пакет dplyr набор данных starwars с
помощью языка R и ответить на вопросы:

``` r
library(dplyr)
```

    Warning: пакет 'dplyr' был собран под R версии 4.5.2


    Присоединяю пакет: 'dplyr'

    Следующие объекты скрыты от 'package:stats':

        filter, lag

    Следующие объекты скрыты от 'package:base':

        intersect, setdiff, setequal, union

1\. Сколько строк в датафрейме?

``` r
nrow(starwars)
```

    [1] 87

2\. Сколько столбцов в датафрейме?

``` r
starwars %>% ncol()
```

    [1] 14

3\. Как просмотреть примерный вид датафрейма?

``` r
starwars %>% glimpse()
```

    Rows: 87
    Columns: 14
    $ name       <chr> "Luke Skywalker", "C-3PO", "R2-D2", "Darth Vader", "Leia Or…
    $ height     <int> 172, 167, 96, 202, 150, 178, 165, 97, 183, 182, 188, 180, 2…
    $ mass       <dbl> 77.0, 75.0, 32.0, 136.0, 49.0, 120.0, 75.0, 32.0, 84.0, 77.…
    $ hair_color <chr> "blond", NA, NA, "none", "brown", "brown, grey", "brown", N…
    $ skin_color <chr> "fair", "gold", "white, blue", "white", "light", "light", "…
    $ eye_color  <chr> "blue", "yellow", "red", "yellow", "brown", "blue", "blue",…
    $ birth_year <dbl> 19.0, 112.0, 33.0, 41.9, 19.0, 52.0, 47.0, NA, 24.0, 57.0, …
    $ sex        <chr> "male", "none", "none", "male", "female", "male", "female",…
    $ gender     <chr> "masculine", "masculine", "masculine", "masculine", "femini…
    $ homeworld  <chr> "Tatooine", "Tatooine", "Naboo", "Tatooine", "Alderaan", "T…
    $ species    <chr> "Human", "Droid", "Droid", "Human", "Human", "Human", "Huma…
    $ films      <list> <"A New Hope", "The Empire Strikes Back", "Return of the J…
    $ vehicles   <list> <"Snowspeeder", "Imperial Speeder Bike">, <>, <>, <>, "Imp…
    $ starships  <list> <"X-wing", "Imperial shuttle">, <>, <>, "TIE Advanced x1",…

4\. Сколько уникальных рас персонажей (species) представлено в данных?

``` r
starwars %>%
  distinct(species) %>% nrow()
```

    [1] 38

5\. Найти самого высокого персонажа.

``` r
starwars %>%
  filter(height == max(height, na.rm = TRUE)) %>%
  select(name, height)
```

    # A tibble: 1 × 2
      name        height
      <chr>        <int>
    1 Yarael Poof    264

6\. Найти всех персонажей ниже 170

``` r
starwars %>%
  filter(height < 170) %>%
  select(name, height)
```

    # A tibble: 22 × 2
       name                  height
       <chr>                  <int>
     1 C-3PO                    167
     2 R2-D2                     96
     3 Leia Organa              150
     4 Beru Whitesun Lars       165
     5 R5-D4                     97
     6 Yoda                      66
     7 Mon Mothma               150
     8 Wicket Systri Warrick     88
     9 Nien Nunb                160
    10 Watto                    137
    # ℹ 12 more rows

7\. Подсчитать ИМТ (индекс массы тела) для всех персонажей. ИМТ
подсчитать по формуле.

``` r
starwars %>% 
  mutate(bmi = mass / (height / 100)^2) %>%
  select(name, height, mass, bmi) %>% head(10)
```

    # A tibble: 10 × 4
       name               height  mass   bmi
       <chr>               <int> <dbl> <dbl>
     1 Luke Skywalker        172    77  26.0
     2 C-3PO                 167    75  26.9
     3 R2-D2                  96    32  34.7
     4 Darth Vader           202   136  33.3
     5 Leia Organa           150    49  21.8
     6 Owen Lars             178   120  37.9
     7 Beru Whitesun Lars    165    75  27.5
     8 R5-D4                  97    32  34.0
     9 Biggs Darklighter     183    84  25.1
    10 Obi-Wan Kenobi        182    77  23.2

8\. Найти 10 самых “вытянутых” персонажей. “Вытянутость” оценить по
отношению массы (mass) к росту (height) персонажей.

``` r
starwars %>%
  mutate(stretch = mass / height) %>%
  arrange(desc(stretch)) %>%
  head(10) %>%
  select(name, mass, height, stretch)
```

    # A tibble: 10 × 4
       name                   mass height stretch
       <chr>                 <dbl>  <int>   <dbl>
     1 Jabba Desilijic Tiure  1358    175   7.76 
     2 Grievous                159    216   0.736
     3 IG-88                   140    200   0.7  
     4 Owen Lars               120    178   0.674
     5 Darth Vader             136    202   0.673
     6 Jek Tono Porkins        110    180   0.611
     7 Bossk                   113    190   0.595
     8 Tarfful                 136    234   0.581
     9 Dexter Jettster         102    198   0.515
    10 Chewbacca               112    228   0.491

9\. Найти средний возраст персонажей каждой расы вселенной Звездных
войн.

``` r
starwars %>%
  group_by(species) %>%
  summarise(avg_height = mean(height, na.rm = TRUE)) %>%
  head(10)
```

    # A tibble: 10 × 2
       species   avg_height
       <chr>          <dbl>
     1 Aleena           79 
     2 Besalisk        198 
     3 Cerean          198 
     4 Chagrian        196 
     5 Clawdite        168 
     6 Droid           131.
     7 Dug             112 
     8 Ewok             88 
     9 Geonosian       183 
    10 Gungan          209.

10\. Найти самый распространенный цвет глаз персонажей вселенной
Звездных войн.

``` r
starwars %>%
  count(eye_color, sort = TRUE) %>%
  head(1)
```

    # A tibble: 1 × 2
      eye_color     n
      <chr>     <int>
    1 brown        21

11\. Подсчитать среднюю длину имени в каждой расе вселенной Звездных
войн

``` r
starwars %>%
  group_by(species) %>%
  summarise(avg_name_length = mean(nchar(name), na.rm = TRUE)) %>%
  head(10)
```

    # A tibble: 10 × 2
       species   avg_name_length
       <chr>               <dbl>
     1 Aleena              12   
     2 Besalisk            15   
     3 Cerean              12   
     4 Chagrian            10   
     5 Clawdite            10   
     6 Droid                4.83
     7 Dug                  7   
     8 Ewok                21   
     9 Geonosian           17   
    10 Gungan              11.7 
