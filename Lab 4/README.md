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
     [5] htmltools_0.5.8.1 yaml_2.3.10       rmarkdown_2.30    knitr_1.50       
     [9] jsonlite_2.0.0    xfun_0.53         digest_0.6.37     rlang_1.1.6      
    [13] evaluate_1.0.5   

1.  Импортировать данные DNS –
    https://storage.yandexcloud.net/dataset.ctfsec/dns.zip

> url \<- “https://storage.yandexcloud.net/dataset.ctfsec/dns.zip”
> download.file(url, “dns.zip”) пробую URL
> ‘https://storage.yandexcloud.net/dataset.ctfsec/dns.zip’ Content type
> ‘application/zip’ length 6407934 bytes (6.1 MB) downloaded 6.1 MB

1.  Добавить пропущенные данные о структуре данных (назначении столбцов)

> zeek_dns_columns \<- c( + “ts”, “uid”, “id.orig_h”, “id.orig_p”,
> “id.resp_h”, “id.resp_p”, + “proto”, “trans_id”, “query”, “qclass”,
> “qclass_name”, “qtype”, + “qtype_name”, “rcode”, “rcode_name”, “AA”,
> “TC”, “RD”, “RA”, + “Z”, “answers”, “TTLs”, “rejected” + )
> colnames(dns_data) \<- zeek_dns_columns

1.  Преобразовать данные в столбцах в нужный формат

> dns_data \<- dns_data %\>% mutate(ts = as.POSIXct(ts, origin =
> “1970-01-01”), id.orig_p = as.integer(id.orig_p), id.resp_p =
> as.integer(id.resp_p), trans_id = as.integer(trans_id), qclass =
> as.integer(qclass), qtype = as.integer(qtype), rcode =
> as.integer(rcode), Z = as.integer(Z))

1.  Просмотреть общую структуру данных с помощью функции glimpse()

> glimpse(dns_data) Rows: 427,935 Columns: 23 $ ts <dttm> 2012-03-16
> 16:30:05, 2012-03-16 16:30:15, 2012-03-16 16:30:15, 2012-03-16 … $ uid
> <chr> “CWGtK431H9XuaTN4fi”, “C36a282Jljz7BsbGH”, “C36a282Jljz7BsbGH”,
> “C36a282Jlj… $ id.orig_h <chr>”192.168.202.100”, “192.168.202.76”,
> “192.168.202.76”, “192.168.202.76”, “1… $ id.orig_p <int> 45658, 137,
> 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 45658, 4… $
> id.resp_h <chr>”192.168.27.203”, “192.168.202.255”, “192.168.202.255”,
> “192.168.202.255”, … $ id.resp_p <int> 137, 137, 137, 137, 137, 137,
> 137, 137, 137, 137, 137, 137, 137, 5353, 5353… $ proto <chr> “udp”,
> “udp”, “udp”, “udp”, “udp”, “udp”, “udp”, “udp”, “udp”, “udp”, “udp”…
> $ trans_id <int> 33008, 57402, 57402, 57402, 57398, 57398, 57398,
> 62187, 62187, 62187, 62190… $ query <chr>
> “\*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00”, … $
> qclass <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
> 1, 1, 1, 1, 1, 1, … $ qclass_name <chr> “C_INTERNET”, “C_INTERNET”,
> “C_INTERNET”, “C_INTERNET”, “C_INTERNET”, “C_IN… $ qtype <int> 33, 32,
> 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 12, 12, 33, 32, 32, 32,… $
> qtype_name <chr>”SRV”, “NB”, “NB”, “NB”, “NB”, “NB”, “NB”, “NB”, “NB”,
> “NB”, “SRV”, “SRV”, … $ rcode <int> 0, NA, NA, NA, NA, NA, NA, NA, NA,
> NA, NA, NA, NA, NA, NA, 0, NA, NA, NA, N… $ rcode_name <chr>
> “NOERROR”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”,
> “-”,… $ AA <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE,
> FALSE, FALSE, FALSE, FALSE… $ TC <lgl> FALSE, FALSE, FALSE, FALSE,
> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE… $ RD <lgl> FALSE,
> TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, …
> $ RA <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE,
> FALSE, FALSE, FALSE… $ Z <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
> 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, … $ answers <chr> “-”, “-”, “-”,
> “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, … $ TTLs
> <chr> “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”, “-”,
> “-”, “-”, … $ rejected <lgl> FALSE, FALSE, FALSE, FALSE, FALSE, FALSE,
> FALSE, FALSE, FALSE, FALSE, FALSE…

1.  Сколько участников информационного обмена в сети Доброй Организации?

> all_ips \<-
> unique(c(dns_data*i**d*.*o**r**i**g*<sub>*h*</sub>, *d**n**s*<sub>*d*</sub>*a**t**a*id.resp_h))
> length(all_ips) \[1\] 1359

1.  Какое соотношение участников обмена внутри сети и участников
    обращений к внешним ресурсам?

> internal_ips \<- all_ips\[grepl(“^192\\168\\”, all_ips)\] external_ips
> \<- setdiff(all_ips, internal_ips) r \<- length(internal_ips) /
> length(external_ips) r \[1\] 10.2314

1.  Найдите топ-10 участников сети, проявляющих наибольшую сетевую
    активность.

> dns_data %\>% count(id.orig_h) %\>% arrange(desc(n)) %\>% head(10)
> id.orig_h n 1 10.10.117.210 75943 2 192.168.202.93 26522 3
> 192.168.202.103 18121 4 192.168.202.76 16978 5 192.168.202.97 16176 6
> 192.168.202.141 14967 7 10.10.117.209 14222 8 192.168.202.110 13372 9
> 192.168.203.63 12148 10 192.168.202.106 10784

1.  Найдите топ-10 доменов, к которым обращаются пользователи сети и
    соответственное количество обращений.

> dns_data %\>% count(query) %\>% arrange(desc(n)) %\>% head(10) query n
> 1 teredo.ipv6.microsoft.com 39273 2 tools.google.com 14057 3
> www.apple.com 13390 4 time.apple.com 13109 5
> safebrowsing.clients.google.com 11658 6
> \*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 10401 7
> WPAD 9134 8 44.206.168.192.in-addr.arpa 7248 9 HPE8AA67 6929 10 ISATAP
> 6569

1.  Опеределите базовые статистические характеристики (функция summary()
    ) интервала времени между последовательными обращениями к топ-10
    доменам.

> top_times \<- dns_data %\>% filter(query %in% top_10_domains) %\>%
> pull(ts) %\>% sort() time_diffs \<- diff(top_times)
> summary(time_diffs) Min. 1st Qu. Median Mean 3rd Qu. Max. 0.000 0.000
> 0.140 0.888 0.570 49677.590

1.  Часто вредоносное программное обеспечение использует DNS канал в
    качестве канала управления, периодически отправляя запросы на
    подконтрольный злоумышленникам DNS сервер. По периодическим запросам
    на один и тот же домен можно выявить скрытый DNS канал. Есть ли
    такие IP адреса в исследуемом датасете?

> top_repeaters \<- dns_data %\>% count(id.orig_h, query) %\>% filter(n
> \> 50) %\>% arrange(desc(n)) head(top_repeaters, 20) id.orig_h query n
> 1 10.10.117.210 teredo.ipv6.microsoft.com 27425 2 192.168.202.93
> www.apple.com 10852 3 10.10.117.210 tools.google.com 10179 4
> 192.168.202.83 44.206.168.192.in-addr.arpa 7248 5 192.168.202.76
> HPE8AA67 6929 6 192.168.202.93 time.apple.com 6038 7 192.168.203.63
> imap.gmail.com 5543 8 192.168.202.76 WPAD 5175 9 192.168.202.103
> api.twitter.com 4163 10 192.168.202.103 api.facebook.com 4137 11
> 10.10.117.210 stats.norton.com 3976 12 192.168.202.87
> safebrowsing.clients.google.com 3908 13 192.168.202.113
> teredo.ipv6.microsoft.com 3110 14 192.168.202.85
> teredo.ipv6.microsoft.com 2980 15 192.168.204.60 time.apple.com 2875
> 16 10.10.117.210 ratings-wrs.symantec.com 2824 17 192.168.202.97
> www.comodo.com 2470 18 192.168.202.102 API.EYE.FI 2405 19
> 192.168.202.141 ISATAP 2385 20 10.10.117.209 teredo.ipv6.microsoft.com
> 2354

1.  Определите местоположение (страну, город) и организацию-провайдера
    для топ-10 доменов. Для этого можно использовать сторонние сервисы,
    например http://ip-api.com (API-эндпоинт http://ip-api.com/json).
