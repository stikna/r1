# Основы обработки данных с помощью R и Dplyr


## Цель работы

1.  Зекрепить практические навыки использования языка программирования R
    для обработки данных
2.  Закрепить знания основных функций обработки данных экосистемы
    tidyverse языка R
3.  Закрепить навыки исследования метаданных DNS трафика

## Исходные данные

1.  Rstudio Desktop
2.  Наше рабочее окружение

## План

1.  Импортировать данные DNS –
    https://storage.yandexcloud.net/dataset.ctfsec/dns.zip
2.  Добавить пропущенные данные о структуре данных (назначении столбцов)
3.  Преобразовать данные в столбцах в нужный формат
4.  Просмотреть общую структуру данных с помощью функции glimpse()
5.  Ответить на вопросы

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

1.  Импортировать данные DNS –
    https://storage.yandexcloud.net/dataset.ctfsec/dns.zip

``` r
 url <- "https://storage.yandexcloud.net/dataset.ctfsec/dns.zip"
 download.file(url, "dns.zip")
 unzip("dns.zip")
 dns_data <- read.csv("dns.log", sep = "\t", header = FALSE)
```

1.  Добавить пропущенные данные о структуре данных (назначении столбцов)

``` r
zeek_dns_columns <- c(
    "ts", "uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p",
    "proto", "trans_id", "query", "qclass", "qclass_name", "qtype",
    "qtype_name", "rcode", "rcode_name", "AA", "TC", "RD", "RA",
    "Z", "answers", "TTLs", "rejected"
)
colnames(dns_data) <- zeek_dns_columns
```

3\. Преобразовать данные в столбцах в нужный формат

``` r
library(dplyr)
```

    Warning: пакет 'dplyr' был собран под R версии 4.5.2


    Присоединяю пакет: 'dplyr'

    Следующие объекты скрыты от 'package:stats':

        filter, lag

    Следующие объекты скрыты от 'package:base':

        intersect, setdiff, setequal, union

``` r
dns_data <- dns_data %>% 
  mutate(ts = as.POSIXct(ts, origin = "1970-01-01"),
    id.orig_p = as.integer(id.orig_p),
    id.resp_p = as.integer(id.resp_p),
    trans_id = as.integer(trans_id),
    qclass = as.integer(qclass),
    qtype = as.integer(qtype),
    rcode = as.integer(rcode),
    Z = as.integer(Z)
  )
```

    Warning: There were 3 warnings in `mutate()`.
    The first warning was:
    ℹ In argument: `qclass = as.integer(qclass)`.
    Caused by warning:
    ! в результате преобразования созданы NA
    ℹ Run `dplyr::last_dplyr_warnings()` to see the 2 remaining warnings.

4\. Просмотреть общую структуру данных с помощью функции glimpse()

``` r
glimpse(dns_data)
```

    Rows: 427,935
    Columns: 23
    $ ts          <dttm> 2012-03-16 16:30:05, 2012-03-16 16:30:15, 2012-03-16 16:3…
    $ uid         <chr> "CWGtK431H9XuaTN4fi", "C36a282Jljz7BsbGH", "C36a282Jljz7Bs…
    $ id.orig_h   <chr> "192.168.202.100", "192.168.202.76", "192.168.202.76", "19…
    $ id.orig_p   <int> 45658, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 1…
    $ id.resp_h   <chr> "192.168.27.203", "192.168.202.255", "192.168.202.255", "1…
    $ id.resp_p   <int> 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137…
    $ proto       <chr> "udp", "udp", "udp", "udp", "udp", "udp", "udp", "udp", "u…
    $ trans_id    <int> 33008, 57402, 57402, 57402, 57398, 57398, 57398, 62187, 62…
    $ query       <chr> "*\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\…
    $ qclass      <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
    $ qclass_name <chr> "C_INTERNET", "C_INTERNET", "C_INTERNET", "C_INTERNET", "C…
    $ qtype       <int> 33, 32, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 12, 12…
    $ qtype_name  <chr> "SRV", "NB", "NB", "NB", "NB", "NB", "NB", "NB", "NB", "NB…
    $ rcode       <int> 0, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
    $ rcode_name  <chr> "NOERROR", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-…
    $ AA          <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FA…
    $ TC          <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FA…
    $ RD          <lgl> FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRU…
    $ RA          <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FA…
    $ Z           <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0…
    $ answers     <chr> "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"…
    $ TTLs        <chr> "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"…
    $ rejected    <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FA…

5\. Сколько участников информационного обмена в сети Доброй Организации?

``` r
all_ips <- unique(c(dns_data$id.orig_h, dns_data$id.resp_h))
length(all_ips)
```

    [1] 1359

6\. Какое соотношение участников обмена внутри сети и участников
обращений к внешним ресурсам?

``` r
internal_ips <- all_ips[grepl("^192\\.168\\.", all_ips)]
external_ips <- setdiff(all_ips, internal_ips)
r <- length(internal_ips) / length(external_ips)
r
```

    [1] 10.2314

7\. Найдите топ-10 участников сети, проявляющих наибольшую сетевую
активность.

``` r
dns_data %>% 
  count(id.orig_h) %>% 
  arrange(desc(n)) %>% 
  head(10)
```

             id.orig_h     n
    1    10.10.117.210 75943
    2   192.168.202.93 26522
    3  192.168.202.103 18121
    4   192.168.202.76 16978
    5   192.168.202.97 16176
    6  192.168.202.141 14967
    7    10.10.117.209 14222
    8  192.168.202.110 13372
    9   192.168.203.63 12148
    10 192.168.202.106 10784

8\. Найдите топ-10 доменов, к которым обращаются пользователи сети и
соответственное количество обращений.

``` r
dns_data %>% count(query) %>% arrange(desc(n)) %>% head(10)
```

                                                                         query
    1                                                teredo.ipv6.microsoft.com
    2                                                         tools.google.com
    3                                                            www.apple.com
    4                                                           time.apple.com
    5                                          safebrowsing.clients.google.com
    6  *\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00
    7                                                                     WPAD
    8                                              44.206.168.192.in-addr.arpa
    9                                                                 HPE8AA67
    10                                                                  ISATAP
           n
    1  39273
    2  14057
    3  13390
    4  13109
    5  11658
    6  10401
    7   9134
    8   7248
    9   6929
    10  6569

9\. Опеределите базовые статистические характеристики (функция summary()
) интервала времени между последовательными обращениями к топ-10
доменам.

``` r
top_10_domains <- dns_data %>% count(query) %>% arrange(desc(n)) %>% head(10) %>% pull(query)
top_times <- dns_data %>% filter(query %in% top_10_domains) %>% pull(ts) %>% sort()
```

10\. Часто вредоносное программное обеспечение использует DNS канал в
качестве канала управления, периодически отправляя запросы на
подконтрольный злоумышленникам DNS сервер. По периодическим запросам на
один и тот же домен можно выявить скрытый DNS канал. Есть ли такие IP
адреса в исследуемом датасете?

``` r
top_repeaters <- dns_data %>% count(id.orig_h, query) %>% filter(n > 50) %>% arrange(desc(n))
head(top_repeaters, 20)
```

             id.orig_h                           query     n
    1    10.10.117.210       teredo.ipv6.microsoft.com 27425
    2   192.168.202.93                   www.apple.com 10852
    3    10.10.117.210                tools.google.com 10179
    4   192.168.202.83     44.206.168.192.in-addr.arpa  7248
    5   192.168.202.76                        HPE8AA67  6929
    6   192.168.202.93                  time.apple.com  6038
    7   192.168.203.63                  imap.gmail.com  5543
    8   192.168.202.76                            WPAD  5175
    9  192.168.202.103                 api.twitter.com  4163
    10 192.168.202.103                api.facebook.com  4137
    11   10.10.117.210                stats.norton.com  3976
    12  192.168.202.87 safebrowsing.clients.google.com  3908
    13 192.168.202.113       teredo.ipv6.microsoft.com  3110
    14  192.168.202.85       teredo.ipv6.microsoft.com  2980
    15  192.168.204.60                  time.apple.com  2875
    16   10.10.117.210        ratings-wrs.symantec.com  2824
    17  192.168.202.97                  www.comodo.com  2470
    18 192.168.202.102                      API.EYE.FI  2405
    19 192.168.202.141                          ISATAP  2385
    20   10.10.117.209       teredo.ipv6.microsoft.com  2354

11\. Определите местоположение (страну, город) и организацию-провайдера
для топ-10 доменов. Для этого можно использовать сторонние сервисы,
например http://ip-api.com (API-эндпоинт http://ip-api.com/json).

``` r
library(httr)
library(purrr)
```

    Warning: пакет 'purrr' был собран под R версии 4.5.2

``` r
top_10_dom <- dns_data |> 
  count(query, sort = TRUE) |> 
  head(10) |> 
  pull(query)

get_geo <- function(domain) {
  tryCatch({
    ip <- try(nslookup(domain, server="8.8.8.8"), silent=TRUE)
    
    if(inherits(ip, "try-error") || is.null(ip)) {
      return(data.frame(
        domain = domain,
        ip = NA,
        country = NA,
        city = NA,
        isp = NA
      ))
    }
    
    response <- GET(paste0("http://ip-api.com/json/", ip[[1]]))
    data <- content(response, "parsed")
    
    if(data$status == "success") {
      data.frame(
        domain = domain,
        ip = data$query,
        country = data$country,
        city = data$city,
        isp = data$isp
      )
    } else {
      data.frame(
        domain = domain,
        ip = ip[[1]],
        country = NA,
        city = NA,
        isp = NA
      )
    }
  }, error = function(e) {
    data.frame(
      domain = domain,
      ip = NA,
      country = NA,
      city = NA,
      isp = NA
    )
  })
}

results <- map_dfr(top_10_dom, get_geo)
results
```

                                                                        domain ip
    1                                                teredo.ipv6.microsoft.com NA
    2                                                         tools.google.com NA
    3                                                            www.apple.com NA
    4                                                           time.apple.com NA
    5                                          safebrowsing.clients.google.com NA
    6  *\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00 NA
    7                                                                     WPAD NA
    8                                              44.206.168.192.in-addr.arpa NA
    9                                                                 HPE8AA67 NA
    10                                                                  ISATAP NA
       country city isp
    1       NA   NA  NA
    2       NA   NA  NA
    3       NA   NA  NA
    4       NA   NA  NA
    5       NA   NA  NA
    6       NA   NA  NA
    7       NA   NA  NA
    8       NA   NA  NA
    9       NA   NA  NA
    10      NA   NA  NA
